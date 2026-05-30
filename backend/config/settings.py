"""Django settings for PaperRepo backend (DRF API)."""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load backend/.env into the environment before reading any settings.
load_dotenv(BASE_DIR / ".env")


def _env_bool(key: str, default: str = "False") -> bool:
    return os.environ.get(key, default).lower() in ("1", "true", "yes")


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "django-insecure-CHANGE-ME")
DEBUG = _env_bool("DJANGO_DEBUG", "True")
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "core.client_model_app.apps.ClientModelAppConfig",
    "user_management",
    "subject_management",
    "question_paper_management",
    "important_topic_management",
    "material_management",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "config.middleware.authorization.AuthorizationMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

# --- Database: Supabase Postgres ONLY (no local/sqlite fallback) ---
if not os.environ.get("SUPABASE_DB_HOST") or not os.environ.get("SUPABASE_DB_PASSWORD"):
    raise ImproperlyConfigured(
        "Supabase is required. Set SUPABASE_DB_HOST and SUPABASE_DB_PASSWORD "
        "in the environment. No local/sqlite fallback is permitted."
    )

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SUPABASE_DB_NAME", "postgres"),
        "USER": os.environ.get("SUPABASE_DB_USER", "postgres"),
        "PASSWORD": os.environ["SUPABASE_DB_PASSWORD"],
        "HOST": os.environ["SUPABASE_DB_HOST"],
        "PORT": os.environ.get("SUPABASE_DB_PORT", "5432"),
        "OPTIONS": {"sslmode": os.environ.get("SUPABASE_DB_SSLMODE", "require")},
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "UNAUTHENTICATED_USER": None,
}

# --- JWT ---
JWT_SECRET = os.environ.get("JWT_SECRET", SECRET_KEY)
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = int(os.environ.get("JWT_EXPIRY_HOURS", "168"))
AUTH_COOKIE_NAME = "session_details"
AUTH_COOKIE_SECURE = _env_bool("AUTH_COOKIE_SECURE", "False")
AUTH_COOKIE_SAMESITE = os.environ.get("AUTH_COOKIE_SAMESITE", "Lax")

# --- Supabase Storage ---
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "papers")
SUPABASE_SIGNED_URL_TTL = int(os.environ.get("SUPABASE_SIGNED_URL_TTL", "3600"))

# --- CORS ---
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
).split(",")
