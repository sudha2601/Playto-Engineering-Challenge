# Playto Engineering Challenge — Technical Explanation

A concise technical explanation of the architecture, database modeling, leaderboard aggregation, and AI usage for the Playto challenge. This README explains the nested comment model, how we avoid N+1 queries when serializing comments, how the rolling 24-hour leaderboard is computed, and how concurrency/double-likes are handled.

## Table of Contents

- [Overview](#overview)
- [Nested Comments (The Tree)](#nested-comments-the-tree)
  - [Database Modeling](#database-modeling)
  - [Serialization Without N+1 Queries](#serialization-without-n1-queries)
  - [In-memory Tree Assembly](#in-memory-tree-assembly)
- [Leaderboard — Last 24 Hours (The Math)](#leaderboard--last-24-hours-the-math)
  - [Scoring Rules](#scoring-rules)
  - [Query Logic](#query-logic)
- [Concurrency & Double Likes](#concurrency--double-likes)
- [AI Audit](#ai-audit)
  - [Bug Introduced by AI and Fix](#bug-introduced-by-ai-and-fix)
- [Why This Works / Design Rationale](#why-this-works--design-rationale)
- [Author](#author)

---

## Overview

This project implements:
- Nested comments using a self-referencing foreign key for unlimited nesting.
- Efficient comment serialization that avoids N+1 queries by fetching all comments for a post in a single query and assembling the tree in memory.
- A dynamic "last 24-hour" leaderboard computed from the `Like` history (no cached karma field).
- Database constraints and transactions to prevent duplicate likes and handle race conditions.
- AI-assisted scaffolding with an audit and a fix for an introduced N+1 pattern.

---

## Nested Comments (The Tree)

### Database Modeling

We model nested comments with a self-referencing foreign key. Top-level comments have `parent = NULL`; replies point to the parent comment.

```python
# models.py
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

This allows unlimited nesting of replies while keeping the schema simple and queryable.

---

### Serialization Without N+1 Queries

To avoid an N+1 problem when rendering a post with its comments, we fetch all comments for the post in a single query, serialize them into a flat list, and then assemble the nested tree in memory.

Example flat serializer:

```python
# serializers.py
class FlatCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    author_id = serializers.IntegerField(source="author.id")
    like_count = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ["id", "author", "author_id", "content", "parent_id", "like_count"]
```

We pass all comments for the set of posts into the serializer context (e.g., `comments_by_post`) so the serializer can assemble trees without extra DB hits.

---

### In-memory Tree Assembly

Assembling the tree in Python requires only one additional pass over the already-fetched comment list.

```python
def get_comments(self, post):
    all_comments = self.context["comments_by_post"].get(post.id, [])

    lookup = {}
    roots = []

    for c in all_comments:
        c["children"] = []
        lookup[c["id"]] = c

    for c in all_comments:
        if c["parent_id"]:
            lookup[c["parent_id"]]["children"].append(c)
        else:
            roots.append(c)

    return roots
```

Why this is efficient:
- One query to fetch posts.
- One query to fetch ALL comments for those posts.
- Tree construction is O(n) in Python memory; no recursive DB queries and no N+1.

---

## Leaderboard — Last 24 Hours (The Math)

### Scoring Rules

- Post like → +5 to the post author
- Comment like → +1 to the comment author

Karma is not stored on the user; it is derived dynamically from the `Like` table and computed on-demand for the rolling 24-hour window.

### Query Logic (example)

Only likes from the last 24 hours are considered:

```python
from django.utils import timezone
from datetime import timedelta

last_24h = timezone.now() - timedelta(hours=24)
likes = Like.objects.filter(created_at__gte=last_24h)
```

Map each `Like` to the content owner and accumulate points:

```python
user_scores = defaultdict(lambda: {"user_id": None, "total": 0})

for like in likes.select_related("post__author", "comment__author"):
    if like.post:
        user = like.post.author
        points = 5
    elif like.comment:
        user = like.comment.author
        points = 1
    user_scores[user.id]["user_id"] = user.id
    user_scores[user.id]["total"] += points

leaderboard = sorted(user_scores.values(), key=lambda x: x["total"], reverse=True)[:5]
```

Notes:
- `select_related` helps avoid extra queries when iterating likes.
- The leaderboard is recalculated in real time from likes in the last 24 hours, which matches requirements for a rolling window and no cached karma fields.

---

## Concurrency & Double Likes

Duplicate likes are prevented at the database level with unique constraints. Example:

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_like"),
            models.UniqueConstraint(fields=["user", "comment"], name="unique_user_comment_like"),
        ]
```

When creating likes, wrap writes in a transaction to avoid race conditions:

```python
from django.db import transaction, IntegrityError

try:
    with transaction.atomic():
        Like.objects.create(user=user, post=post)  # or comment=comment
except IntegrityError:
    # handle duplicate like attempt (already liked)
    pass
```

This guarantees a single like per (user, post) and per (user, comment), and ensures consistent behavior under concurrent requests.

---

## AI Audit

ChatGPT was used to scaffold initial components and UI. During the audit we discovered an example bug introduced by AI scaffolding:

Bad pattern (causes N+1):

```python
# naive recursive access inside serializer
children = obj.children.all()
```

This triggers additional queries for each comment node and leads to O(n) extra queries for deep trees.

### Fix

Replace recursive child fetching with:
- One query to fetch all comments for a post
- Flat serialization
- In-memory tree assembly (see "In-memory Tree Assembly" above)

This change reduces comment-related DB queries from O(n) to O(1) (one query for all comments per post set).

---

## Why This Works / Design Rationale

- Nested comments via a self-FK are simple, flexible, and indexable.
- Fetching all comments and assembling the tree in memory eliminates N+1 query problems and performs well for typical thread sizes.
- Leaderboard is always correct and derived from authoritative like history — no stale cached “karma” fields.
- Database uniqueness constraints + transactional writes protect data integrity under concurrency.
- Minimal and auditable AI usage; issues introduced by AI were identified and fixed.

---

## Author

Sudhanshu Songire

---
