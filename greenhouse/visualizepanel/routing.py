from .consumers import WSConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

ws_urlpatterns = [
    path('ws/dashboard', WSConsumer.as_asgi()),
]

# application = ProtocolTypeRouter({
#     'websocket':AuthMiddlewareStack(URLRouter( ws_urlpatterns ))
# })