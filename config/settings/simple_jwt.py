from datetime import timedelta

from decouple import config

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "BLACKLIST_AFTER_ROTATION": False,
    "SIGNING_KEY": config("JWT_SECRET_KEY"),
    "AUTH_HEADER_TYPES": ("Bearer",),
}
