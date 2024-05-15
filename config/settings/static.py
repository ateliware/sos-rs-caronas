import os

from .aws_settings import (
    AWS_STORAGE_BUCKET_NAME_MEDIA,
    AWS_STORAGE_BUCKET_NAME_STATIC,
)
from .environments import BASE_DIR, USE_S3

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


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static", "css"),
    os.path.join(BASE_DIR, "static", "img"),
    os.path.join(BASE_DIR, "static", "html"),
]

if USE_S3:
    MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME_MEDIA}.s3.amazonaws.com/"
    DEFAULT_FILE_STORAGE = (
        "apps.core.services.custom_storages.CustomS3MediaStorage"
    )
    MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

    STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME_STATIC}.s3.amazonaws.com/"
    STATICFILES_STORAGE = (
        "apps.core.services.custom_storages.CustomS3StaticStorage"
    )
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

else:
    MEDIA_URL = '/media/'
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
