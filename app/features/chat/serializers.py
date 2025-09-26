from rest_framework import serializers

from .models import Ai_model_logs, ChatMessage, ChatSession


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "sender", "message_type", "content", "extra_data", "created_at"]


class ChatSessionSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatSession
        fields = ["id", "title", "created_at", "updated_at", "last_message"]

    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        if last_msg:
            return ChatMessageSerializer(last_msg).data
        return None




class AiModelLogsSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    class Meta:
        model = Ai_model_logs
        fields = ['id','email', 'title', 'overview', 'rating', 'ingredients', 'ingredient_items', 'instructions', 'created_on', 'updated_on',"status"]
        
    def get_status(self, obj):
        # Replace title with 'Failed' if it is an error log
        if obj.title == "Recipe Request Invalid":
            return "Failed"
        return "Success"