from .database import DATABASES
from .environments import (
    BASE_DIR,
    DEFAULT_AUTO_FIELD,
    ROOT_URLCONF,
    WSGI_APPLICATION,
)
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
from .static import STATIC_URL, STATICFILES_DIRS, TEMPLATES
