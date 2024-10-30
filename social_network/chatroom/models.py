
from django.db import models
from django.contrib.auth.models import User

class PrivateChat(models.Model):
    admin = models.ForeignKey(User, related_name='admin_private_chats', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='private_chats', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.admin.username} and {self.user.username}"



class GroupChat(models.Model):
    admin = models.ForeignKey(User, related_name='admin_group_chats', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='group_chats', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    chat_type = models.CharField(max_length=10)  # 'group' or 'private'
    chat_id = models.IntegerField()
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    replied_message = models.ForeignKey('self', related_name='replies', on_delete=models.SET_NULL, blank=True, null=True)
    forwarded_message = models.ForeignKey('self', related_name='forwards', on_delete=models.SET_NULL, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:20]}'
