from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from .models import Post, Comment, Like


class LeaderboardTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="alice")
        self.user2 = User.objects.create_user(username="bob")

        self.post = Post.objects.create(author=self.user1, content="Hello")

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            content="Nice post"
        )

    def test_leaderboard_last_24h(self):
        # Bob likes Alice's post (+5 to Alice)
        Like.objects.create(user=self.user2, post=self.post)

        # Alice likes Bob's comment (+1 to Bob)
        Like.objects.create(user=self.user1, comment=self.comment)

        # OLD like (should NOT count)
        old_like = Like.objects.create(user=self.user2, comment=self.comment)
        old_like.created_at = timezone.now() - timedelta(days=2)
        old_like.save()

        last_24h = timezone.now() - timedelta(hours=24)
        likes = Like.objects.filter(created_at__gte=last_24h)

        scores = {}

        for like in likes:
            if like.post:
                user = like.post.author
                points = 5
            else:
                user = like.comment.author
                points = 1

            scores[user.username] = scores.get(user.username, 0) + points

        # Alice should have 5 points
        self.assertEqual(scores["alice"], 5)

        # Bob should have 1 point
        self.assertEqual(scores["bob"], 1)
