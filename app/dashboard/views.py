from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken  # JWT

from app.accounts.models import User
from app.accounts.serializers.base_serializers import \
    UserManagementMentSerializer
from app.dashboard.serializers.accounts_serializers import (
    AdminLoginSerializer, AdminProfileSerializer, AdminSubscriptionSerializer,
    UserSerializer, UserSubscriptionStatusSerializer)
from app.dashboard.serializers.terms_and_policy import (
    AboutUsSerializer, PrivacyPolicySerializer, TermsConditionsSerializer)
from app.stripe.models import SubscriptionModel, UserSubscriptionModel
from app.stripe.serializers import SubscriptionPatchSerializer

from .models import AboutUs, PrivacyPolicy, TermsConditions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to anyone,
    but write/update access only to admins.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class PrivacyPolicyView(generics.RetrieveUpdateAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self):
        return PrivacyPolicy.objects.first()

class TermsConditionsView(generics.RetrieveUpdateAPIView):
    queryset = TermsConditions.objects.all()
    serializer_class = TermsConditionsSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_object(self):
        return TermsConditions.objects.first()
    
class AboutUsView(generics.RetrieveAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

    def get_object(self):
        return AboutUs.objects.first()



@api_view(["POST"])
def contact_us(request):
    user = request.user
    message = request.data.get("message")

    # Validate inputs
    if not all([message]):
        return Response(
            {"message": None, "error": "All fields except phone are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    context = {
        "email": user.email,
        "message": message,
    }

    subject = f"New message from {user.email}"
    body_html = render_to_string('email/contact.html', context)

    try:
        email_msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Message from {user.email}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.EMAIL_HOST_USER]
        )
        email_msg.attach_alternative(body_html, "text/html")
        email_msg.send()
    except Exception as e:
        return Response(
            {"message": None, "error": f"Failed to send email: {str(e)}","status":status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response(
        {"message": "Your message has been sent successfully.", "error": None,"status":status.HTTP_200_OK},
        status=status.HTTP_200_OK
    )






class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserManagementListView(generics.ListAPIView):
    # queryset = User.objects.select_related('profile').all().order_by('full_name')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserManagementDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(["GET"])
def user_management_view(request):
    user = request.user
    if user.is_staff:
        queryset = User.objects.filter(is_staff=False)
        serializer = UserManagementMentSerializer(queryset,many=True)
        return Response({"data":serializer.data})
    else:
        return Response({"error":"You do not have the authorization to perform this action"})
    
@api_view(['GET'])
def get_user_profile(request,id):
    user = request.user
    if user.is_staff:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        return Response({"error":"You do not have the authorization to perform this action"})
    
@api_view(["GET"])
def user_subs_management_views(request):
    user = request.user
    if user.is_staff:
        query = User.objects.filter(is_staff=False)
        
        serializer = AdminSubscriptionSerializer(query, many=True)
        return Response(serializer.data)
    else:
        return Response({"error":"You do not have the authorization to perform this action"})
    
    
    

@api_view(['PATCH'])
def update_subscription(request, id):
    try:
        subscription = SubscriptionModel.objects.get(pk=id)
    except SubscriptionModel.DoesNotExist:
        return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SubscriptionPatchSerializer(subscription, data=request.data, partial=True)
    
    if serializer.is_valid():
        subscription = serializer.save()
        return Response({
            'id': subscription.id,
            'initial_price': subscription.initial_price,
            'discount': subscription.discount,
            'is_active': subscription.is_active,
            'total_price': subscription.total_price,
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(["GET", "PATCH"])
def admin_profile_view(request):
    user = request.user
    if not user.is_staff:
        return Response({"error": "You are not authorized"}, status=403)
    
    if request.method == "GET":
        serializer = AdminProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = AdminProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Profile updated", "data": serializer.data})
        return Response(serializer.errors, status=400)