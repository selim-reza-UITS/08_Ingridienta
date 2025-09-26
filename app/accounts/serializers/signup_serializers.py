from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import \
    TokenRefreshSerializer as BaseRefreshSerializer

User = get_user_model()

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    class Meta:
        model = User
        fields = ['email', 'password','confirmPassword']

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already associated with another account.")
        return value
    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({"error":"Password do not match"})
        return attrs
    def create(self, validated_data):
        validated_data.pop("confirmPassword",None)
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email and password:
            user = authenticate(email=email,password=password)
            if not user:
                raise serializers.ValidationError({"error":"Invalid email or password"})
            if not user.is_active:
                raise serializers.ValidationError({"error":"Your account is inactive"})
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError({"error":"Need to provide both email and password"})
    

class TokenRefreshSerializer(BaseRefreshSerializer):

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except serializers.ValidationError:
            raise serializers.ValidationError({"error": "Invalid or expired refresh token."})

        return {
            "message": "Access token refreshed successfully",
            "access": data.get("access")
        }
        
        
class AccountDeleteSerializer(serializers.Serializer):
    confirmation = serializers.BooleanField()
    agreement = serializers.BooleanField()

    def validate(self, attrs):
        confirmation = attrs.get("confirmation")
        agreement = attrs.get("agreement")

        if not confirmation or not agreement:
            raise serializers.ValidationError({"error": "You must confirm and agree before deleting your account"})
        return attrs