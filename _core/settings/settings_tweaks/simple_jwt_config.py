from datetime import timedelta

LOCAL_SIMPLE_JWT_SETTINGG = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}