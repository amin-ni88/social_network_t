from django.contrib import admin
from .models import PrivateChat, GroupChat, Message

@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'user', 'created_at')
    search_fields = ('admin__username', 'user__username')
    list_filter = ('created_at',)

@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin', 'name', 'created_at')
    search_fields = ('admin__username', 'name')
    list_filter = ('created_at',)
    filter_horizontal = ('members',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_type', 'chat_id', 'sender', 'content', 'timestamp')
    search_fields = ('sender__username', 'content')
    list_filter = ('chat_type', 'timestamp')
