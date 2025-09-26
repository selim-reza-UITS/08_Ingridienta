from rest_framework import serializers

from app.accounts.models import MultipleEmailField, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField(read_only=True)  # for GET
    image = serializers.ImageField(required=False, allow_null=True, write_only=True)  # for PATCH/upload

    def get_email(self, obj):
        return obj.user.email

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            if request:
                return request.build_absolute_uri(f"/api/v1{url}")
            return f"/api/v1{url}"
        return None

    class Meta:
        model = UserProfile
        fields = [
            "email",
            "image",   
            "image_url",
            "full_name",
            "gender",
            "language",
            "country",
            "is_subs"
        ]
        

class AddOtherEmailSerializers(serializers.ModelSerializer):
    main_email = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_main_email(self, obj):
        return obj.user.email
    
    def get_email(self, obj):
        # Get all additional emails for the user excluding the main email
        additional_emails = MultipleEmailField.objects.filter(user=obj.user).exclude(email=obj.user.email)
        
        # Use a set to ensure uniqueness of email addresses
        unique_emails = set(email.email for email in additional_emails)
        
        # Return the unique emails as a list
        return list(unique_emails)

    class Meta:
        model = MultipleEmailField
        fields = ["main_email", "email","created_on"]

class AddEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleEmailField
        fields = ["email"]
        