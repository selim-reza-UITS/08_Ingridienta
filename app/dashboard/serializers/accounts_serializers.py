from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from app.accounts.models import User, UserProfile
from app.stripe.models import UserSubscriptionModel


class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_staff:
            raise serializers.ValidationError("You do not have admin access.")

        data['user'] = user
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['image', 'address', 'age', 'status']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfile
    # profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'profile']
       
class AdminSubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    subscription_plan = serializers.SerializerMethodField()
    package_amount = serializers.SerializerMethodField()
    renewal_date = serializers.SerializerMethodField()
    expiry_warnings = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.profile.full_name if hasattr(obj, "profile") and obj.profile.full_name else obj.email

    def get_subscription_plan(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        return active_sub.subscription.package_id if active_sub else "FREE"

    def get_package_amount(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        return float(active_sub.subscription.total_price) if active_sub else 0.00

    def get_renewal_date(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        if active_sub and active_sub.end_date:
            return active_sub.end_date + timedelta(days=1)
        return None

    def get_expiry_warnings(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        return active_sub.end_date if active_sub else None

    def get_status(self, obj):
        active_sub = obj.subscriptions.filter(is_active=True).first()
        return "Active" if active_sub and active_sub.is_active else "Inactive"

    class Meta:
        model = User
        fields = [
            "name",
            "subscription_plan",
            "package_amount",
            "renewal_date",
            "expiry_warnings",
            "status",
        ]

        
class UserSubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptionModel
        fields = ["is_active"]
        

class AdminProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    action = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ["name", "email","gender", "role", "last_login", "action", "old_password", "new_password"]

    def get_gender(self, obj):
        return obj.profile.gender if obj.profile.gender is not None else None
    
    def get_name(self, obj):
        return obj.profile.full_name if hasattr(obj, "profile") and obj.profile.full_name else obj.email

    def get_role(self, obj):
        return "Admin" if obj.is_staff else "User"

    def get_action(self, obj):
        return True

    def update(self, instance, validated_data):
        # Update name
        name = validated_data.get("name")
        if name:
            if hasattr(instance, "profile"):
                instance.profile.full_name = name
                instance.profile.save()
            else:
                # If no profile exists, create one
                instance.profile = instance.profile.create(full_name=name)
        
        # Change password
        old_password = validated_data.get("old_password")
        new_password = validated_data.get("new_password")
        if old_password and new_password:
            if not instance.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Old password is incorrect"})
            instance.password = make_password(new_password)
        
        instance.save()
        return instance
    
    
    
    
     