from pathlib import Path

from decouple import Csv, config

from django.utils.translation import gettext_lazy as _

CURRENT_ENVIRONMENT = config("CURRENT_ENVIRONMENT")


class CurrentEnv:
    is_dev = CURRENT_ENVIRONMENT == "development"
    is_prod = CURRENT_ENVIRONMENT == "production"
    is_stage = CURRENT_ENVIRONMENT == "staging"
    is_test = CURRENT_ENVIRONMENT == "testing"


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -----------------------------------------------------------------------------
# GENERAL
# -----------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", cast=str)
DEBUG = config("DEBUG", cast=bool, default=False)
ALLOWED_HOSTS = []
admins_csv = Csv(cast=lambda s: tuple(s.split(",")), delimiter=";")
ADMINS = config("ADMINS", cast=admins_csv, default=None)
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "drf_spectacular",
    "drf_standardized_errors",
    # Local apps
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------------------------------
# URLS
# -----------------------------------------------------------------------------
ROOT_URLCONF = config("ROOT_URLCONF", cast=str, default="config.urls")
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

# -----------------------------------------------------------------------------
# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# -----------------------------------------------------------------------------
# DATABASES
# -----------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# -----------------------------------------------------------------------------
# STATIC
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [str(BASE_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# -----------------------------------------------------------------------------
# MEDIA
# -----------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------------------
USE_TZ = True
TIME_ZONE = "UTC"
USE_I18N = True
LANGUAGE_CODE = "ru"
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# -----------------------------------------------------------------------------
# EMAIL
# -----------------------------------------------------------------------------
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

# -----------------------------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------------------------
DJANGO_VALIDATORS_PATH = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.UserAttributeSimilarityValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.MinimumLengthValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.CommonPasswordValidator"},
    {"NAME": f"{DJANGO_VALIDATORS_PATH}.NumericPasswordValidator"},
]

# -----------------------------------------------------------------------------
# COMPONENTS
# -----------------------------------------------------------------------------
from .components.api import *  # noqa E402, F403
from .components.logging_ import *  # noqa E402, F403
