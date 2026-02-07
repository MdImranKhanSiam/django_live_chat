from django.contrib import admin
from . models import ChatRoom, GroupInvite, RoomMember, Message, MessageReadStatus

# Register your models here.

admin.site.register(ChatRoom)
admin.site.register(GroupInvite)
admin.site.register(RoomMember)
admin.site.register(Message)
admin.site.register(MessageReadStatus)