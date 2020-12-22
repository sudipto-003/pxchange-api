from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt 
from django.conf import settings
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs


class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        #websocke path: ws://<path to web socket>/?token=<access token>
        token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError):
            return None
        
        else:
            paylod = jwt.decode(token, settings.SECRET_KEY)
            user = get_user_model().objects.get(id=paylod['user_id'])

        return self.inner(dict(scope, user=user))