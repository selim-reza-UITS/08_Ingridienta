from django.conf import settings
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Chat {self.id}"


class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ("conversation", "Conversation"),
        ("recipe", "Recipe"),
        ("error", "Error"),
    ]

    chat = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(
        max_length=50,
        choices=[("user", "User"), ("assistant", "Assistant")]
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default="conversation")
    content = models.TextField(null=True, blank=True)  # for plain text messages
    extra_data = models.JSONField(null=True, blank=True)  # for recipes or errors
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.message_type}] {self.sender}: {self.content[:40] if self.content else ''}"


class Ai_model_logs(models.Model):
    email = models.EmailField(null=True)
    title = models.CharField(max_length=255)
    overview = models.TextField()
    rating = models.CharField(max_length=10)
    
    # Store ingredients list as JSON
    ingredients = models.JSONField()
    ingredient_items = models.JSONField()
    
    instructions = models.TextField()
    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title