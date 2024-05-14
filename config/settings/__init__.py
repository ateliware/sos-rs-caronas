from .aws_settings import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_ACL,
    AWS_S3_FILE_OVERWRITE,
    AWS_S3_REGION_NAME,
    AWS_S3_SIGNATURE_NAME,
    AWS_S3_VERIFY,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)
from .database import DATABASES
from .environments import (
    BASE_DIR,
    DEFAULT_AUTO_FIELD,
    ROOT_URLCONF,
    WSGI_APPLICATION,
)
from .file_storages import DEFAULT_FILE_STORAGE, MEDIA_ROOT, MEDIA_URL
from .i18n import LANGUAGE_CODE, TIME_ZONE, USE_I18N, USE_TZ
from .installed_apps import INSTALLED_APPS
from .jazzmin_settings import JAZZMIN_SETTINGS
from .middleware import MIDDLEWARE
from .rest_framework import REST_FRAMEWORK
from .security import (
    ALLOWED_HOSTS,
    AUTH_PASSWORD_VALIDATORS,
    AUTH_USER_MODEL,
    CORS_ALLOW_HEADERS,
    CORS_ORIGIN_ALLOW_ALL,
    DEBUG,
    SECRET_KEY,
)
from .simple_jwt import SIMPLE_JWT
from .spectacular_settings import SPECTACULAR_SETTINGS
from .static import STATIC_ROOT, STATIC_URL, STATICFILES_DIRS, TEMPLATES
