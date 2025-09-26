from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.accounts.models import UserProfile
from app.stripe.models import SubscriptionModel, UserSubscriptionModel


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_and_subscription(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile
        UserProfile.objects.create(user=instance)
        
        # Ensure there is a "Free" plan in the SubscriptionModel
        free_plan, created = SubscriptionModel.objects.get_or_create(
            package_id=SubscriptionModel.PlanOptions.FREE,
            is_active=True,
            defaults={'initial_price': 0.00, 'discount': 0.00, 'total_price': 0.00, 'timing': SubscriptionModel.TimingText.FREE}
        )
        
        # Check if the user already has a subscription, if not, create one with the Free plan
        if not UserSubscriptionModel.objects.filter(user=instance, subscription=free_plan).exists():
            UserSubscriptionModel.objects.create(
                user=instance,
                subscription=free_plan,
                is_active=True
            )
