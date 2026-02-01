from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class QueryParamAuthentication(BaseAuthentication):
    """
    Authenticate using user_id from query parameter or request body.
    """
    
    def authenticate(self, request):
        # Get user_id from query parameter or POST data
        user_id = request.GET.get('user_id') or request.POST.get('user_id')
        
        logger.info(f"QueryParamAuthentication: user_id = {user_id}")
        
        if not user_id:
            logger.warning("QueryParamAuthentication: No user_id provided")
            return None
        
        try:
            user = User.objects.get(id=int(user_id))
            logger.info(f"QueryParamAuthentication: ✓ Authenticated as {user.username}")
            return (user, None)
        except (User.DoesNotExist, ValueError) as e:
            logger.error(f"QueryParamAuthentication: ✗ Failed: {e}")
            raise AuthenticationFailed(f'Invalid user_id: {user_id}')
