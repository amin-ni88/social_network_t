

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
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    chat_type = models.CharField(max_length=10, choices=(('private', 'Private'), ('group', 'Group')))
    chat_id = models.PositiveIntegerField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat_type} chat"

