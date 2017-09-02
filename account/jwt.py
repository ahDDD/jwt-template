from account.serializers import UserSerializer
from datetime import datetime, timedelta

def custom_jwt_response(token, user=None, request=None):
    refresh = int((datetime.now() + timedelta(days=7)).timestamp())
    timeout = int((datetime.now() + timedelta(days=30)).timestamp())

    return {
        'token': token,
        'expire': dict(refresh=refresh, timeout=timeout),
        'user': UserSerializer(user, context={'request': request}).data
    }