import os

from .aws_settings import (
    AWS_STORAGE_BUCKET_NAME_MEDIA,
    AWS_STORAGE_BUCKET_NAME_STATIC,
)
from .environments import BASE_DIR

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "apps", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.s3.amazonaws.com/"
DEFAULT_FILE_STORAGE = "apps.core.services.custom_storages.CustomS3MediaStorage"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME_STATIC}.s3.amazonaws.com/"
STATICFILES_STORAGE = "apps.core.services.custom_storages.CustomS3StaticStorage"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static", "css"),
    os.path.join(BASE_DIR, "static", "img"),
    os.path.join(BASE_DIR, "static", "html"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")