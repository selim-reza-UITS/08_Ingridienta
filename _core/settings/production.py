# ===========================================================================================================
# ===========================================================================================================
import os

from dotenv import load_dotenv

from _core.settings.settings_tweaks.app_config import (CUSTOM_APP,
                                                       DJANGO_BUILT_IN_APP,
                                                       PRIORITY_APP,
                                                       PRODUCTION_APP)
from _core.settings.settings_tweaks.cors_config import \
    PRODUCTION_ALLOWED_ORIGIN
from _core.settings.settings_tweaks.django_admin_env_notice_config import *  # noqa: F403
from _core.settings.settings_tweaks.network_ip_config import \
    PRODUCTION_ALLOWED_HOST
from _core.settings.settings_tweaks.rest_framework_settings import \
    LOCAL_REST_FRAMEWORK_SETTINGS

from .base import *  # noqa: F403

load_dotenv()
# ===========================================================================================================
# ===========================================================================================================
ALLOWED_HOSTS = PRODUCTION_ALLOWED_HOST
INSTALLED_APPS = PRIORITY_APP + DJANGO_BUILT_IN_APP + PRODUCTION_APP + CUSTOM_APP # noqa: F405
CORS_ALLOWED_ORIGINS = PRODUCTION_ALLOWED_ORIGIN
CORS_ALLOW_CREDENTIALS = True




WSGI_APPLICATION = '_core.wsgi.application'
REST_FRAMEWORK = LOCAL_REST_FRAMEWORK_SETTINGS


SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = "DENY"

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


ENVIRONMENT_NAME = "Production"
ENVIRONMENT_COLOR = "#FF2222"


