from rest_framework import serializers

from app.stripe.models import (PaymentHistory, SubscriptionModel,
                               UserSubscriptionModel)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = [
            "id",
            "package_id",
            "initial_price",
            "discount",
            "total_price",
            "timing",
            "is_active",
            "created_on",
            "updated_on",
            "calculate_total_price",
        ]
        read_only_fields = [
            "id",
            "total_price",
            "created_on",
            "updated_on",
            "calculate_total_price",
        ]


class SubscriptionPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = ['initial_price', 'discount', 'is_active']

    def validate_initial_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Initial price cannot be negative.")
        return value

    def validate_discount(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Discount must be between 0 and 100.")
        return value

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptionModel
        fields = [
            "user",
            "subscription",
            "start_date",
            "end_date",
            "is_active",
        ]
        
