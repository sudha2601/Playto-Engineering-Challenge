"""
Socket event emitter for real-time updates
"""
import threading
from .serializers import PostSerializer
from .models import Post

try:
    from socketio_client import emit_event
except ImportError:
    def emit_event(event_name, event_data):
        pass

def broadcast_feed_update():
    """Broadcast updated feed to all connected clients"""
    try:
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(post, context={"request": None})

        emit_event('feed_update', {'posts': serializer.data})
    except Exception as e:
        print(f"Feed update error: {e}")

def broadcast_like_update(post_id):
    """Broadcast like count update for a specific post"""
    try:
        post = Post.objects.get(id=post_id)
        emit_event('like_update', {
            'post_id': post_id,
            'like_count': post.like_set.count()
        })
    except Post.DoesNotExist:
        pass
    except Exception as e:
        print(f"Like update error: {e}")

def broadcast_comment_update(post_id):
    """Broadcast comment update for a specific post"""
    try:
        post = Post.objects.get(id=post_id)
        serializer = PostSerializer(post)
        emit_event('comment_update', {
            'post_id': post_id,
            'post': serializer.data
        })
    except Post.DoesNotExist:
        pass
    except Exception as e:
        print(f"Comment update error: {e}")

def emit_sync(func):
    """Helper to emit socket events in a background thread"""
    def wrapper():
        try:
            func()
        except Exception as e:
            print(f"Emit error: {e}")
    
    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()

