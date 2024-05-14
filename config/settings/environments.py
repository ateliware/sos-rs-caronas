from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_URLCONF = "config.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WSGI_APPLICATION = "config.wsgi.application"
USE_S3 = config("USE_S3", default=False, cast=bool)