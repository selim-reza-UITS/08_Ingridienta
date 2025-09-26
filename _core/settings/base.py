from pathlib import Path

from _core.settings.settings_tweaks.caches_config import LOCAL_REDIS_CACHES
from _core.settings.settings_tweaks.middleware_config import DEFAULT_MIDDLEWARE
from _core.settings.settings_tweaks.password_tweaks import (
    DEFAULT_PASSWORD_HASHERS, DEFAULT_PASSWORD_VALIDATOR)
from _core.settings.settings_tweaks.template_config import DEFAULT_CONFIG

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = True
# Application definition
MIDDLEWARE = DEFAULT_MIDDLEWARE
ROOT_URLCONF = '_core.urls'
TEMPLATES = DEFAULT_CONFIG
# Password validation
PASSWORD_HASHERS = DEFAULT_PASSWORD_HASHERS
AUTH_PASSWORD_VALIDATORS = DEFAULT_PASSWORD_VALIDATOR
# 
CACHES = LOCAL_REDIS_CACHES
# Optional: This is to ensure Django sessions are stored in Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
# 
AUTH_USER_MODEL = "accounts.User"