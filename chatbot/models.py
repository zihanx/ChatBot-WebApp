from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One user, one chat
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation of {self.user.username}"


class Message(models.Model):
    """Stores individual messages in a conversation."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    # author = models.CharField(max_length=10, choices=[("user", "User"), ("ai", "AI")])
    author = models.CharField(max_length=50)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.capitalize()} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
