from django.contrib import admin

from .models import SubscriptionModel, UserSubscriptionModel

# Register your models here.
admin.site.register(SubscriptionModel)
admin.site.register(UserSubscriptionModel)
