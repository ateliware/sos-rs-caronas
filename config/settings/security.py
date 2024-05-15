from decouple import config

SECRET_KEY = config("SECRET_KEY", default="-")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = ["*"]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CSRF_TRUSTED_ORIGINS = [config("APP_DOMAIN")]
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True
AUTH_USER_MODEL = "core.CustomUser"
CORS_ALLOW_HEADERS = [
    "access-control-allow-origin",
    "content-type",
    "authorization",
]
