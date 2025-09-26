# Create your views here.
from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase

from app.accounts.serializers.profile_serializers import UserProfileSerializer
from app.accounts.serializers.signup_serializers import (
    AccountDeleteSerializer, LoginSerializer, TokenRefreshSerializer,
    UserSignupSerializer)

User = get_user_model()

class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Signup using full name, email, mobile, and password.",
        request_body=UserSignupSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request (validation errors)")
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Handle user signup with validated serializer data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"message":"You have registered successfully"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    @swagger_auto_schema(
        request_body=LoginSerializer,
        operation_summary="User Login",
        operation_description="Login with email and password to get JWT tokens."
    )
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        profile_data = {}
        
        if hasattr(user,"profile"):
            profile_data = UserProfileSerializer(user.profile).data
            
        return Response({
            "message":"Login successful",
            "access":str(refresh.access_token),
            "refresh":str(refresh),
            "user": profile_data,
            "admin":user.is_staff
        },status=status.HTTP_200_OK)
        
        
class CustomTokenRefreshView(TokenViewBase):
    """
    Custom view for refreshing JWT access tokens with a friendly message.
    """
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
    
    
class AccountDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AccountDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.delete()

        return Response(
            {"message": "Your account has been deleted successfully."},
            status=status.HTTP_200_OK
        )
        
class GoogleLoginAPIView(APIView):
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        if not email or password:
            return Response({"error":"Provide all the fields"})
        user = User.objects.get(email=email)
        if user:
            refresh = RefreshToken.for_user(user)
        
            profile_data = {}
            
            if hasattr(user,"profile"):
                profile_data = UserProfileSerializer(user.profile).data
                
            return Response({
                "message":"Login successful",
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "user": profile_data
            },status=status.HTTP_200_OK)
        else:
            new_user = User.objects.create(email=email)
            new_user.set_password(password)
            refresh = RefreshToken.for_user(user)
        
            profile_data = {}
            
            if hasattr(user,"profile"):
                profile_data = UserProfileSerializer(user.profile).data
                
            return Response({
                "message":"Login successful",
                "access":str(refresh.access_token),
                "refresh":str(refresh),
                "user": profile_data
            },status=status.HTTP_200_OK)
        