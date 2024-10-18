
from django.urls import path
from .views import chatroom_home, create_private_page, create_group_page, private_chat, group_chat, delete_private_chat, delete_group_chat, leave_group_chat

urlpatterns = [
    path('', chatroom_home, name='chatroom_home'),
    path('create_private/', create_private_page, name='create_private_page'),
    path('create_group/', create_group_page, name='create_group_page'),
    path('private/<int:chat_id>/', private_chat, name='private_chat'),
    path('group/<int:chat_id>/', group_chat, name='group_chat'),
    path('delete_private/<int:chat_id>/', delete_private_chat, name='delete_private_chat'),
    path('delete_group/<int:chat_id>/', delete_group_chat, name='delete_group_chat'),
    path('leave_group/<int:chat_id>/', leave_group_chat, name='leave_group_chat'),
]
