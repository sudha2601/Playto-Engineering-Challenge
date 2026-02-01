from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Case, When, IntegerField, F
from django.db import transaction, IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Value
from django.db.models import Count



from .models import Post, Like, Comment
from .serializers import PostSerializer

# Import socket events
try:
    from .socket_events import broadcast_feed_update, broadcast_like_update, broadcast_comment_update, emit_sync
except ImportError:
    def broadcast_feed_update(): pass
    def broadcast_like_update(post_id): pass
    def broadcast_comment_update(post_id): pass
    def emit_sync(func): pass

@api_view(["GET"])
def feed(request):
    posts = Post.objects.annotate(
        like_count=Count("like")
    ).order_by("-created_at")

    comments = Comment.objects.annotate(
        like_count=Count("like")
    ).values(
        "id",
        "author__username",
        "author_id",
        "content",
        "parent_id",
        "post_id",
        "created_at",
        "like_count",
    )

    comments_by_post = {}
    for c in comments:
        c["author"] = c.pop("author__username")
        comments_by_post.setdefault(c["post_id"], []).append(c)

    serializer = PostSerializer(
        posts,
        many=True,
        context={"comments_by_post": comments_by_post},
    )

    return Response(serializer.data)



@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def like_post(request, post_id):
    try:
        with transaction.atomic():
            Like.objects.create(user=request.user, post_id=post_id)
        emit_sync(lambda: broadcast_like_update(post_id))
        return Response({"status": "liked"})
    except IntegrityError:
        return Response({"error": "already liked"}, status=400)

@api_view(["POST"])
def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    Like.objects.create(user=request.user, comment=comment)

    emit_sync(lambda: broadcast_comment_update(comment.post_id))

    return Response({"ok": True})





@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def add_comment(request, post_id):
    """
    Body:
    {
        "content": "hello",
        "parent": optional_comment_id
    }
    """
    content = request.data.get("content")
    parent_id = request.data.get("parent")

    if not content:
        return Response({"error": "content required"}, status=400)

    comment = Comment.objects.create(
        post_id=post_id,
        author=request.user,
        content=content,
        parent_id=parent_id
    )
    
    emit_sync(lambda: broadcast_comment_update(post_id))
    
    return Response({
        "status": "comment added",
        "comment": {
            "id": comment.id,
            "author": comment.author.username,
            "content": comment.content,
            "children": []
        }
    })
@api_view(["GET"])
def leaderboard(request):
    last_24h = timezone.now() - timedelta(hours=24)

    scores = (
        Like.objects.filter(created_at__gte=last_24h)
        .annotate(
            owner=Case(
                When(post__isnull=False, then=F("post__author__username")),
                When(comment__isnull=False, then=F("comment__author__username")),
            ),
            points=Case(
                When(post__isnull=False, then=Value(5)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        )
        .values("owner")
        .annotate(total=Sum("points"))
        .order_by("-total")[:5]
    )

    return Response([
        {"username": s["owner"], "total": s["total"]}
        for s in scores
    ])


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def signup_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "missing fields"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "user exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({"status": "created"})

@csrf_exempt
@api_view(["POST"])
def login_view(request):
    user = authenticate(
        username=request.data.get("username"),
        password=request.data.get("password"),
    )

    if user:
        login(request, user)
        return Response({"status": "logged"})
    return Response({"error": "invalid"}, status=400)
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def create_post(request):
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info(f"create_post: request.user = {request.user}")
    logger.info(f"create_post: type(request.user) = {type(request.user)}")
    
    content = request.data.get("content", "").strip()
    if not content:
        return Response({"error": "Content cannot be empty"}, status=400)
    
    if not request.user or request.user.is_anonymous:
        logger.error("User not authenticated!")
        return Response({"error": "User not authenticated"}, status=401)
    
    try:
        post = Post.objects.create(
            author=request.user,
            content=content
        )
        logger.info(f"✓ Post created successfully: {post.id}")
        emit_sync(broadcast_feed_update)
        return Response({"ok": True, "post_id": post.id})
    except Exception as e:
        logger.error(f"✗ Error creating post: {e}")
        return Response({"error": str(e)}, status=500)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes([AllowAny])
def delete_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if post.author != request.user:
            return Response({"error": "not authorized"}, status=403)
        post.delete()
        emit_sync(broadcast_feed_update)
        return Response({"status": "post deleted"})
    except Post.DoesNotExist:
        return Response({"error": "post not found"}, status=404)

@csrf_exempt
@api_view(["DELETE"])
@permission_classes([AllowAny])
def unlike_post(request, post_id):
    try:
        like = Like.objects.get(user=request.user, post_id=post_id)
        like.delete()
        emit_sync(lambda: broadcast_like_update(post_id))
        return Response({"status": "unliked"})
    except Like.DoesNotExist:
        return Response({"error": "like not found"}, status=404)

@api_view(["DELETE"])
def unlike_comment(request, comment_id):
    like = Like.objects.get(user=request.user, comment_id=comment_id)
    post_id = like.comment.post_id
    like.delete()

    emit_sync(lambda: broadcast_comment_update(post_id))

    return Response({"ok": True})

@csrf_exempt
@api_view(["DELETE"])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)

        if comment.author != request.user:
            return Response({"error": "not authorized"}, status=403)

        post_id = comment.post_id
        comment.delete()

        return Response({"status": "deleted", "post_id": post_id})
    except Comment.DoesNotExist:
        return Response({"error": "not found"}, status=404)