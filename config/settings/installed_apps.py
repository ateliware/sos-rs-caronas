INSTALLED_APPS = [
    # theme
    "jazzmin",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # application apps
    "apps.core",
    "apps.address_manager",
    "apps.term_manager",
    "apps.ride_manager",
    # 3rd apps
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]
