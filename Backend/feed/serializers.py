from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    author_id = serializers.IntegerField(source="author.id")
    like_count = serializers.IntegerField()
    comments = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_id",
            "content",
            "created_at",
            "like_count",
            "comments",
        ]

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
