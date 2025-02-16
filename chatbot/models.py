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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    GEDNER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("non-binary", "Non-binary"),
        ("prefer_not_say", "Prefer not to say"),
        ("other", "Other"),
    ]
    gender = models.CharField(max_length=20, choices=GEDNER_CHOICES, blank=True)
    bio = models.TextField(blank=True, help_text="A short description about yourself.")
    interests = models.TextField(blank=True, help_text="What are you interested in? (comma-separated)")
    conversation_summary = models.TextField(blank=True)
    
    MOOD_LEVEL_CHOICES = [
        (1, "Very Unpleasant"),
        (2, "Unpleasant"),
        (3, "A Bit Unpleasant"),
        (4, "Neutral"),
        (5, "A Bit Pleasant"),
        (6, "Pleasant"),
        (7, "Very Pleasant"),
    ]
    current_mood_level = models.IntegerField(choices=MOOD_LEVEL_CHOICES, default=4)
    
    MOOD_TAG_CHOICES = [
        ("calm", "Calm"),
        ("stressed", "Stressed"),
        ("anxious", "Anxious"),
        ("excited", "Excited"),
        ("tired", "Tired"),
        ("grateful", "Grateful"),
        ("happy", "Happy"),
        ("frustrated", "Frustrated"),
        ("sad", "Sad"),
        ("hopeful", "Hopeful"),
        ("angry", "Angry"),
        ("lonely", "Lonely"),
        ("confident", "Confident"),
        ("content", "Content"),
        ("motivated", "Motivated"),
        ("bored", "Bored"),
        ("neutral", "Neutral"),
    ]
    current_mood_tag = models.JSONField(default=list, blank=True)
    
    conversation_summary = models.TextField(blank=True, help_text="A summary of the conversation with the AI.")
    last_chat_history = models.JSONField(default=list, blank=True, help_text="The last chat history with the AI.")
    
    def __str__(self):
        return self.user.username
    