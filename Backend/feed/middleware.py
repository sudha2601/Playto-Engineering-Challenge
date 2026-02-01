from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class MockAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Try to get user_id from query parameter first, then from header
        user_id = (
            request.GET.get("user_id") or 
            request.POST.get("user_id") or
            request.headers.get("X-Mock-User-ID") or 
            request.headers.get("x-mock-user-id") or
            request.META.get("HTTP_X_MOCK_USER_ID")
        )
        
        logger.info(f"MockAuthMiddleware: user_id = {user_id}")

        if user_id:
            try:
                user_obj = User.objects.get(id=int(user_id))
                request.user = user_obj
                logger.info(f"MockAuthMiddleware: ✓ Set user to {user_obj.username} (id={user_obj.id})")
            except (User.DoesNotExist, ValueError) as e:
                logger.error(f"MockAuthMiddleware: ✗ Failed to set user: {e}")
        else:
            logger.info("MockAuthMiddleware: ✗ No user_id found")

        return self.get_response(request)
