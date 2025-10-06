
from datetime import timedelta

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import User
from app.stripe.models import (PaymentHistory, SubscriptionModel,
                               UserSubscriptionModel)
from app.stripe.serializers import SubscriptionSerializer

load_dotenv()


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY  # Secret Key from Stripe Dashboard

class CreateStripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        package_id = request.data.get("package_id")
        if not package_id:
            return Response({"error": "package_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Subscription Model based on the package_id
        try:
            subscription_plan = SubscriptionModel.objects.get(id=package_id, is_active=True)
        except SubscriptionModel.DoesNotExist:
            return Response({"error": "SubscriptionModel package not found or inactive."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        try:
            # Stripe expects the price in cents
            price_in_cents = int(subscription_plan.total_price * 100)

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",  # Adjust currency as needed
                            "unit_amount": price_in_cents,
                            "product_data": {
                                "name": f"{subscription_plan.package_id}",
                            },
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",  # One-time payment
                success_url="http://localhost:5015/payment/success",  # Adjust URLs as needed
                cancel_url="http://localhost:5015/payment/cancel",
                metadata={
                    "user_id": str(user.id),
                    "package_id": package_id,
                    "payment_for": "SubscriptionModel",
                },
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"checkout_url": checkout_session.url})

    
class CancelSubscriptionModelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = getattr(user, "profile", None)

        if not profile:
            return Response({"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the free SubscriptionModel plan
        free_plan = SubscriptionModel.objects.filter(
            package_type=SubscriptionModel.PackageType.FREE,
            status=True
        ).first()

        if not free_plan:
            return Response({"error": "Free SubscriptionModel plan not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Downgrade user SubscriptionModel to free
        profile.SubscriptionModel_plan = free_plan
        profile.SubscriptionModel_start = None
        profile.SubscriptionModel_end = None
        profile.save()

        return Response({"message": "SubscriptionModel canceled and downgraded to free plan."}, status=status.HTTP_200_OK)





stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # Secret Key from Stripe Dashboard


@api_view(['POST'])
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    # Verify webhook signature
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  # contains a stripe.checkout.Session

        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        package_id = metadata.get('package_id')
        payment_for = metadata.get('payment_for')

        if payment_for != "SubscriptionModel":
            return HttpResponse(status=200)  # Ignore non-SubscriptionModel payments here

        try:
            user = User.objects.get(id=user_id)
            subscription_plan = SubscriptionModel.objects.get(id=package_id, is_active=True)
            profile = user.profile
            profile.is_subs = True
            profile.save()
            # Create User Subscription
            user_subscription = UserSubscriptionModel.objects.create(
                user=user,
                subscription=subscription_plan,
                start_date=timezone.now(),
                is_active=True,
            )

            # Create Payment History
            PaymentHistory.objects.create(
                user=user,
                plan=subscription_plan,
                price_paid=session.get('amount_total') / 100,  # Convert from cents
            )

            # Update the UserProfile subscription info
            user_profile = user.profile
            user_profile.subscription_plan = subscription_plan
            user_profile.subscription_start = timezone.now()

            # Set expiry based on the subscription plan type
            if subscription_plan.timing == SubscriptionModel.TimingText.MONTHLY:
                user_profile.subscription_end = timezone.now() + timedelta(days=30)
            elif subscription_plan.timing == SubscriptionModel.TimingText.YEARLY:
                user_profile.subscription_end = timezone.now() + timedelta(days=365)
            else:
                user_profile.subscription_end = None  # Free or no expiry

            user_profile.save()

        except (User.DoesNotExist, SubscriptionModel.DoesNotExist):
            return HttpResponse(status=400)

    return HttpResponse(status=200)


class SubscriptionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Filter out subscriptions with package_id 'free'
            queryset = SubscriptionModel.objects.exclude(package_id=SubscriptionModel.PlanOptions.FREE)
            serializer = SubscriptionSerializer(queryset, many=True)
            return Response({"data": serializer.data})
        except Exception as e:
            return Response({"error": str(e)})