from django.contrib import admin

from .models import PrivacyPolicy, TermsConditions


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']

@admin.register(TermsConditions)
class TermsConditionsAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__']
