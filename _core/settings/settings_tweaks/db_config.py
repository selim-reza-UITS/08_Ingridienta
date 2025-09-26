import os

from _core.settings.base import BASE_DIR

LOCAL_SQLITE_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

LOCAL_POSTGRESQL_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_LOCAL_NAME"),
        'USER': os.getenv("DB_LOCAL_USER"),
        'PASSWORD': os.getenv("DB_LOCAL_PASS"),
        'HOST': os.getenv("DB_LOCAL_HOST"),
        'PORT': os.getenv("DB_LOCAL_PORT")
    }
}


PRODUCTION_POSTGRESQL_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_PROD_NAME"),
        'USER': os.getenv("DB_PROD_USER"),
        'PASSWORD': os.getenv("DB_PROD_PASS"),
        'HOST': os.getenv("DB_PROD_HOST"),
        'PORT': os.getenv("DB_PROD_PORT")
    }
}