from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# from app.accounts.views import account_management_view as user_views
from app.accounts.views import account_management_view as user_views
from app.accounts.views import password_management_view as password_views
from app.accounts.views import profile_management_view as profile_views
from app.dashboard import views as admin_views
from app.dashboard.overview_views import DashboardView
from app.features.chat import views as chat_views
from app.stripe import stripe_views as subs_views

urlpatterns = [
    # your existing URLs
    path("sign-up/",user_views.UserSignupView.as_view()), #Done
    path("login/",user_views.LoginView.as_view()), #Done
    path("google/login/",user_views.GoogleLoginAPIView.as_view()),
    # create new account with google
    path('get/new/token/', user_views.CustomTokenRefreshView.as_view(), name='token_refresh'), # Done
    path('profile/fields/choices/', profile_views.ChoicesAPIView.as_view(), name='choices-api'), # Done
    path('profile/', profile_views.ProfileView.as_view()), # Done
    path('user/emails/', profile_views.AddOtherEmailViews.as_view(), name='email-list'), #Done
    path('user/emails/add/', profile_views.AddEmailView.as_view(), name='email-add'), # Done
    # otp:
    path("send-otp/",password_views.RequestOTPView.as_view()), #Done
    path("verify-otp/",password_views.VerifyOTPView.as_view()), #done
    path("reset-password/",password_views.ResetPasswordView.as_view()), # done
    path("update-password/",password_views.ChangePasswordView.as_view()), #Done
    path('user/account/delete/', user_views.AccountDeleteView.as_view(), name='account_delete'), #Done
    # 
    path('privacy-policy/', admin_views.PrivacyPolicyView.as_view(), name='privacy-policy'), #GET DONE !!!
    path('terms-and-conditions/', admin_views.TermsConditionsView.as_view(), name='terms-and-conditions'), #Get DONE
    #
    # ADMIN = API = ADMIN
    #
    path("admin/users/list/", admin_views.user_management_view, name="admin-user-management"),
    path("admin/user/profile/view/<int:id>/",admin_views.get_user_profile,name="admin-user-profile-view"),
    path("admin/user/subs/list/",admin_views.user_subs_management_views,name="admin subs list"),
    # path("admin/user/subscription/42/update-status/",admin_views.update_subscription_status,name="admin subs list"),
    path('admin/profile/', admin_views.admin_profile_view, name='admin-profile'),
    #
    path("chats/list/", chat_views.list_chats, name="list-chats"),
    path("chats/send_message/", chat_views.send_message, name="send-message"),
    path('admin/user/subscription/<str:id>/update-status/', admin_views.update_subscription, name='update-subscription'),
    #
    path("make/subscribtion/payment/",subs_views.CreateStripeCheckoutSessionView.as_view(),name="subscribe"),
    
    path("cancel/subscribtion/payment/",subs_views.CancelSubscriptionModelView.as_view()),
    path("stripe/webhook/",subs_views.stripe_webhook),
    #
    path("subscription/list/",subs_views.SubscriptionListView.as_view()),
    #
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    #
    path('ai-model-logs/',chat_views.AiModelLogsListView.as_view(), name='ai_model_logs_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
