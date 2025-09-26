from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import MultipleEmailField
from app.accounts.serializers.profile_serializers import (
    AddEmailSerializer, AddOtherEmailSerializers, UserProfileSerializer)
from app.accounts.utils.choices_fields import (COUNTRY_CHOICES, GENDER_CHOICES,
                                               LANGUAGE_CHOICES)


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    @swagger_auto_schema(
        operation_summary="Get user profile",
        responses={200: UserProfileSerializer()}
    )
    def get(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, context={"request": request})
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=UserProfileSerializer,
        responses={200: UserProfileSerializer()}
    )
    def patch(self, request):
        profile = request.user.profile
        serializer = UserProfileSerializer(
            profile,
            data=request.data,
            context={"request": request},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AddOtherEmailViews(generics.ListAPIView):
    serializer_class =AddOtherEmailSerializers
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return MultipleEmailField.objects.filter(user=user)

class AddEmailView(generics.CreateAPIView):
    serializer_class = AddEmailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
        
class ChoicesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {
            "gender_choices": GENDER_CHOICES,
            "language_choices": LANGUAGE_CHOICES,
            "country_choices": COUNTRY_CHOICES,
        }
        return Response(data)