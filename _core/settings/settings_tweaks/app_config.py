PRIORITY_APP = [
    'jazzmin',
    "drf_yasg",
    'django_admin_env_notice',
]

DJANGO_BUILT_IN_APP = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',

]


LOCAL_APP = [  # noqa: F405
    'hijack',
    "corsheaders",
    'adminsortable2',
    'rest_framework',
    'rest_framework_simplejwt',
    'silk',
    'debug_toolbar',
    'django_extensions',
]

PRODUCTION_APP = [  # noqa: F405
    "corsheaders",
    'rest_framework',
    'rest_framework_simplejwt', 
]

CUSTOM_APP = [
    "coreapi",
    "app.accounts",
    "app.dashboard",
    "app.stripe",
    "app.features.chat"
]

