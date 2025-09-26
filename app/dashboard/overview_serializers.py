# serializers.py
from rest_framework import serializers

from app.accounts.models import UserProfile
from app.features.chat.models import Ai_model_logs
from app.stripe.models import SubscriptionModel, UserSubscriptionModel


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = ['package_id', 'initial_price', 'discount', 'total_price', 'timing', 'is_active']

class UserSubscriptionSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer()
    
    class Meta:
        model = UserSubscriptionModel
        fields = ['user', 'subscription', 'start_date', 'end_date', 'is_active']

class AiModelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ai_model_logs
        fields = ['title', 'ingredients', 'ingredient_items', 'created_on', 'status']
