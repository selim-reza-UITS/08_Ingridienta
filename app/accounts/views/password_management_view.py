# views.py
import random

from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from app.accounts.models import PasswordResetOTP
from app.accounts.serializers.password_serializers import (
    ChangePasswordSerializer,
    RequestOTPSerializer,
    ResetPasswordSerializer,
    VerifyOTPSerializer,
)
from _core.settings.local import EMAIL_HOST_USER

User = get_user_model()


class RequestOTPView(APIView):
    @swagger_auto_schema(
        request_body=RequestOTPSerializer,
        operation_summary="Request For OTP",
        operation_description="Request to send OTP to email",
    )
    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        otp = str(random.randint(1234, 9999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        # HTML email
        subject = "Password Reset OTP"
        from_email = EMAIL_HOST_USER
        to = [email]

        html_content = f"""
        <html>
        <body style="background-color:#FFFDF8; font-family: Arial, sans-serif; padding: 40px;">
            <div style="max-width: 500px; margin: auto; background-color:#E4572E; padding: 30px; border-radius: 10px; text-align: center; color: white;">
                <h2>Password Reset OTP</h2>
                <p style="font-size: 18px;">Your OTP is:</p>
                <p style="font-size: 36px; font-weight: bold; letter-spacing: 4px;">{otp}</p>
            </div>
        </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, "", from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        return Response(
            {"message": "OTP sent to your email."}, status=status.HTTP_200_OK
        )


class VerifyOTPView(APIView):
    @swagger_auto_schema(
        operation_summary="OTP Verification",
        operation_description="Verify requested OTP",
        request_body=VerifyOTPSerializer,
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(
                user=user, otp=otp, is_used=False
            ).latest("created_at")
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"error": "Invalid OTP or email."}, status=400)

        if not otp_obj.is_valid():
            return Response({"error": "OTP expired or already used."}, status=400)

        return Response({"message": "OTP verified."}, status=200)


class ResetPasswordView(APIView):
    @swagger_auto_schema(
        operation_summary="Reset Password",
        operation_description="Reset user's current password using otp",
        request_body=ResetPasswordSerializer,
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(
                user=user, otp=otp, is_used=False
            ).latest("created_at")
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            return Response({"error": "Invalid OTP or email."}, status=400)

        if not otp_obj.is_valid():
            return Response({"error": "OTP expired or already used."}, status=400)

        user.set_password(new_password)
        user.save()
        otp_obj.is_used = True
        otp_obj.save()

        return Response({"message": "Password reset successfully."}, status=200)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["put"]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_summary="Update Password",
        operation_description="Update the user's password by validating the current one.",
        request_body=ChangePasswordSerializer,
        responses={200: "Password changed successfully", 400: "Validation error"},
    )
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password changed successfully"}, status=status.HTTP_200_OK
        )
