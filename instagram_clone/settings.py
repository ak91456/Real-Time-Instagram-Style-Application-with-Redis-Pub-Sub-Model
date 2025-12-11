from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-secret-change-me"
DEBUG = True
ALLOWED_HOSTS = ["*"]  # Allow Docker + local + GitHub Actions


# -----------------------------------------------------------------------------
# INSTALLED APPS
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "channels",

    "accounts",
    "posts",
    "notifications",
]


# -----------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "instagram_clone.urls"


# -----------------------------------------------------------------------------
# TEMPLATES
# -----------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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


# -----------------------------------------------------------------------------
# ASGI
# -----------------------------------------------------------------------------
ASGI_APPLICATION = "instagram_clone.asgi.application"


# -----------------------------------------------------------------------------
# DATABASE CONFIG
# Handles 3 environments:
#   1. Docker → Postgres (HOST=db)
#   2. GitHub Actions CI → Postgres (HOST=localhost)
#   3. Local pytest → SQLite
# -----------------------------------------------------------------------------

if os.environ.get("GITHUB_ACTIONS") == "true":
    # GitHub Actions: use PostgreSQL service on localhost
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "instagram"),
            "USER": os.environ.get("POSTGRES_USER", "admin"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "adminpassword"),
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

elif "pytest" in sys.modules:
    # Local pytest: use SQLite to avoid host errors & external DB need
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "test_db.sqlite3",
        }
    }

else:
    # Docker & production
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "instagram"),
            "USER": os.environ.get("POSTGRES_USER", "admin"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "adminpassword"),
            "HOST": os.environ.get("POSTGRES_HOST", "db"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }


# -----------------------------------------------------------------------------
# AUTH
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []
AUTH_USER_MODEL = "accounts.User"


# -----------------------------------------------------------------------------
# LOCALIZATION
# -----------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# -----------------------------------------------------------------------------
# STATIC & MEDIA
# -----------------------------------------------------------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# -----------------------------------------------------------------------------
# CHANNELS (REDIS)
# -----------------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    os.environ.get("REDIS_HOST", "redis"),
                    int(os.environ.get("REDIS_PORT", 6379)),
                )
            ],
        },
    },
}


# -----------------------------------------------------------------------------
# DRF & JWT
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}
