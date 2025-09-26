from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class UserManagementMentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    
    def get_name(self,obj):
        return obj.profile.full_name
    
    def get_subscription(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        if active_sub:
            return "PAID"
        return "FREE"
    
    
    class Meta:
        model = User
        fields = ["id","name","email","subscription"]