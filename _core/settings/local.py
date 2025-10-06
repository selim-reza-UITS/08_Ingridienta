# ===========================================================================================================
# ===========================================================================================================
import os

from dotenv import load_dotenv

from .base import *  # noqa: F403

load_dotenv()


from _core.settings.settings_tweaks.app_config import (CUSTOM_APP,
                                                       DJANGO_BUILT_IN_APP,
                                                       LOCAL_APP, PRIORITY_APP)
from _core.settings.settings_tweaks.caches_config import LOCAL_CACHE_CONFIG
from _core.settings.settings_tweaks.dashboard import JAZZMIN_DISPAY_SETTING
from _core.settings.settings_tweaks.db_config import (LOCAL_POSTGRESQL_CONFIG,
                                                      LOCAL_SQLITE_CONFIG)
from _core.settings.settings_tweaks.django_admin_env_notice_config import *  # noqa: F403
from _core.settings.settings_tweaks.logging_settings import LOGGER_SETTINGS
from _core.settings.settings_tweaks.middleware_config import \
    LOCAL_MIDDLEWARE_ADDED
from _core.settings.settings_tweaks.network_ip_config import (
    LOCAL_ALLOWED_HOST, LOCAL_INTERNAL_IP)
from _core.settings.settings_tweaks.rest_framework_settings import \
    LOCAL_REST_FRAMEWORK_SETTINGS
from _core.settings.settings_tweaks.simple_jwt_config import \
    LOCAL_SIMPLE_JWT_SETTINGG

# ===========================================================================================================
# ===========================================================================================================
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = LOCAL_ALLOWED_HOST
INTERNAL_IPS = LOCAL_INTERNAL_IP
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# 
INSTALLED_APPS = PRIORITY_APP + DJANGO_BUILT_IN_APP + LOCAL_APP + CUSTOM_APP  # noqa: F405
# 
MIDDLEWARE += LOCAL_MIDDLEWARE_ADDED  # noqa: F405
# 
WSGI_APPLICATION = '_core.wsgi.application'
#
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = LOCAL_POSTGRESQL_CONFIG
# 
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True
# 

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # noqa: F405

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # noqa: F405
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # This now includes css/, js/, images/, audio/, video/ # noqa: F405
]
# 



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "srreza1999@gmail.com"
EMAIL_HOST_PASSWORD ="thvljalqrgiucbgx"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CACHES = LOCAL_CACHE_CONFIG
REST_FRAMEWORK = LOCAL_REST_FRAMEWORK_SETTINGS
SIMPLE_JWT=LOCAL_SIMPLE_JWT_SETTINGG
JAZZMIN_SETTINGS = JAZZMIN_DISPAY_SETTING


# Set label and color for current environment:
ENVIRONMENT_NAME = "Local Dev"
ENVIRONMENT_COLOR = "#33CC33"

STRIPE_TEST_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")