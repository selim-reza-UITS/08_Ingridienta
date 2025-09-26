from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from app.accounts.utils.choices_fields import (COUNTRY_CHOICES, GENDER_CHOICES,
                                               LANGUAGE_CHOICES)

from .misc.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    
    
class UserProfile(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to='photo/profile_images/', blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20, null=True, blank=True)
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=40, null=True, blank=True)
    country = models.CharField(choices=COUNTRY_CHOICES, max_length=40, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)  # Removed null=True as it's unnecessary
    is_subs = models.BooleanField(null=True,default=False)
    recipe_generate = models.PositiveIntegerField(default=0,null=True)
    def __str__(self):
        return f"Profile of {self.full_name} ({self.user.email})"



class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - OTP: {self.otp}"
    
    
    
class MultipleEmailField(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="emailList",null=True)
    email = models.EmailField(max_length=255,unique=True)
    created_on = models.DateField(null=True,auto_now_add=True)
    def __str__(self):
        return f"{self.user.email}"