# views.py
from datetime import datetime

from django.core.exceptions import FieldError
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.models import User
from app.features.chat.models import Ai_model_logs
from app.stripe.models import UserSubscriptionModel


class DashboardView(APIView):
    def get(self, request):
        # Total users
        total_users = User.objects.count()

        # Active subscriptions
        active_subscriptions = UserSubscriptionModel.objects.filter(is_active=True).count()

        # AI usages (logs)
        ai_usages = Ai_model_logs.objects.count()

        # Chart data
        current_year = datetime.now().year
        chart_data = {}

        for year in range(current_year, current_year - 3, -1):
            monthly_data = []
            for month in range(1, 13):
                current_usage = Ai_model_logs.objects.filter(created_on__year=year, created_on__month=month).count()
                previous_usage = Ai_model_logs.objects.filter(created_on__year=year-1, created_on__month=month).count()
                monthly_data.append({
                    "name": datetime(year, month, 1).strftime('%b'),
                    "current": current_usage,
                    "previous": previous_usage
                })
            chart_data[str(year)] = monthly_data

        # Recent signed up users
        try:
            recent_signups = User.objects.all().order_by('-profile__created_on')[:5]  # Order by profile's created_on
        except FieldError:
            recent_signups = User.objects.all().order_by('-date_joined')[:5]  # Fallback to date_joined if profile has no created_on

        recent_signups_data = [{
            "name": user.email,
            # Get the most recent active subscription for the user
            "sub": "Paid" if user.subscriptions.filter(is_active=True).first() else "Free",
            "date": user.profile.created_on.strftime('%b %d, %Y')  # Use profile's created_on field
        } for user in recent_signups]

        # AI Model Logs
        recent_logs = Ai_model_logs.objects.all().order_by('-created_on')[:5]
        recent_logs_data = [{
            "date": log.created_on.strftime('%d/%m/%Y'),
            "email": log.title,
            "ingredients": log.ingredients,
            "recipeGenerated": "Generated Recipe",  # Assuming recipe generation
            # "status": log.status
        } for log in recent_logs]

        # Construct final response
        data = {
            "total_user": total_users,
            "active_subscription": active_subscriptions,
            "ai_usages": ai_usages,
            "chart": chart_data,
            "recent_signed_up": recent_signups_data,
            "recent_ai_logs": recent_logs_data
        }
        return Response(data)
