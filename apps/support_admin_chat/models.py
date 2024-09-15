from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='chat_room', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"ChatRoom for {self.user.username} (Active: {self.active})"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.phone_number} in Room {self.room.id}"
