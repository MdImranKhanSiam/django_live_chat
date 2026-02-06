from django.urls import re_path
from . consumers import chat_consumer, PrivateChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/$', chat_consumer.as_asgi(), name='socket'),
    re_path(r'^ws/privatechat/(?P<user_id>\d+)/$', PrivateChatConsumer.as_asgi()),
    
]