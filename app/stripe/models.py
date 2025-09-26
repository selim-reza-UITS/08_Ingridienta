from django.contrib.auth import get_user_model
from django.db import models
from shortuuid.django_fields import ShortUUIDField

User = get_user_model()
class SubscriptionModel(models.Model):
    class PlanOptions(models.TextChoices):
        FREE = "free", "Free"
        BASIC = "basic", "Basic"
        STANDARD = "standard", "Standard"

    class TimingText(models.TextChoices):
        FREE = "free", "Free"
        MONTHLY = "monthly", "Monthly"
        YEARLY = "yearly", "Yearly"

    id = ShortUUIDField(length=4, max_length=4, alphabet="0123456789selimrza", primary_key=True)
    package_id = models.CharField(max_length=255, choices=PlanOptions.choices, default=PlanOptions.FREE)
    initial_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    discount = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)  
    total_price = models.DecimalField(decimal_places=2, max_digits=10, default=0.00, editable=False)
    timing = models.CharField(max_length=255, choices=TimingText.choices, default=TimingText.FREE)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        discount_amount = (self.discount / 100) * self.initial_price
        return self.initial_price - discount_amount

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.package_id} ({self.timing}) - Total Price: {self.total_price}"
 
class UserSubscriptionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    subscription = models.ForeignKey(SubscriptionModel, on_delete=models.CASCADE, related_name="user_subscriptions")
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    free_trial = models.PositiveIntegerField(default=0,null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.subscription.package_id}"


# Create your models here.
class PaymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    plan = models.ForeignKey(SubscriptionModel, on_delete=models.SET_NULL, null=True)  # Added plan field
    price_paid = models.PositiveIntegerField(default=0)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return f"Payment No - {self.pk}: by {self.user.email if self.user else 'Unknown'} for {self.plan.package_id if self.plan else 'N/A'}"




###############################################################################################
###############################################################################################


