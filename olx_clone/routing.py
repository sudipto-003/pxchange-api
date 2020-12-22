from channels.routing import ProtocolTypeRouter, URLRouter
from .chnmidwr import JWTAuthMiddleware
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})