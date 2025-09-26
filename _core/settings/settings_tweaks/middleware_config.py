DEFAULT_MIDDLEWARE= [
    '_core.middleware.request_logger.RequestLoggingMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    # 'csp.middleware.CSPMiddleware', Configure when you can do it yourself.
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]


LOCAL_MIDDLEWARE_ADDED = [  # noqa: F405
    'hijack.middleware.HijackUserMiddleware',
    'silk.middleware.SilkyMiddleware',
]