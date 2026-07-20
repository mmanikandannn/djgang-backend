"""
Django settings for the DJ Chemboi backend.
"""

from datetime import timedelta
from pathlib import Path

import environ


# ==============================================================================
# Base configuration
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
)

environ.Env.read_env(BASE_DIR / ".env")


SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-change-me-in-production",
)

DEBUG = env.bool(
    "DEBUG",
    default=True,
)

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "djgang-backend.onrender.com",
        "djgang.wtf",
        "www.djgang.wtf",
    ],
)


# ==============================================================================
# Applications
# ==============================================================================

INSTALLED_APPS = [
    # Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Cloudinary
    # Keep this after django.contrib.staticfiles so Django's normal
    # collectstatic command is used.
    "cloudinary_storage",
    "cloudinary",

    # Third-party applications
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",

    # Local applications
    "accounts",
    "catalog",
    "cart",
    "orders",
    "bookings",
    "events_app",
    "gallery",
    "music",
]


AUTH_USER_MODEL = "accounts.User"


# ==============================================================================
# Middleware
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise must come directly after SecurityMiddleware.
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # CORS should appear before CommonMiddleware.
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"


# ==============================================================================
# Templates
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "config" / "templates",
        ],

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


WSGI_APPLICATION = "config.wsgi.application"


# ==============================================================================
# Database
# ==============================================================================
# Uses DATABASE_URL when supplied.
# Falls back to SQLite when DATABASE_URL is missing.
# ==============================================================================

DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}


if not DEBUG:
    DATABASES["default"]["CONN_MAX_AGE"] = 600


# ==============================================================================
# Password validation
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==============================================================================
# Internationalization
# ==============================================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ==============================================================================
# Static files
# ==============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = []


# ==============================================================================
# Cloudinary configuration
# ==============================================================================

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": env(
        "CLOUDINARY_CLOUD_NAME",
        default="",
    ),
    "API_KEY": env(
        "CLOUDINARY_API_KEY",
        default="",
    ),
    "API_SECRET": env(
        "CLOUDINARY_API_SECRET",
        default="",
    ),
}


# ==============================================================================
# Storage configuration
# ==============================================================================

STORAGES = {
    # Product, gallery and other uploaded files are stored in Cloudinary.
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },

    # Django Admin, CSS and JavaScript static files use WhiteNoise.
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}

# Compatibility setting required by django-cloudinary-storage 0.3.0.
# The package's collectstatic command still checks this legacy setting.
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# ==============================================================================
# Media files
# ==============================================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# Default primary key
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ==============================================================================
# Django REST Framework
# ==============================================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),

    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
    ),

    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),

    "PAGE_SIZE": 20,
}


# ==============================================================================
# JWT configuration
# ==============================================================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=6),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),

    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,

    "AUTH_HEADER_TYPES": (
        "Bearer",
    ),

    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


# ==============================================================================
# CORS configuration
# ==============================================================================

CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://djgang.wtf",
        "https://www.djgang.wtf",
    ],
)

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_ALL_ORIGINS = False


# ==============================================================================
# CSRF configuration
# ==============================================================================

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "https://djgang-backend.onrender.com",
        "https://djgang.wtf",
        "https://www.djgang.wtf",
    ],
)


# ==============================================================================
# Production security
# ==============================================================================

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = True

    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"


# ==============================================================================
# Razorpay
# ==============================================================================

RAZORPAY_KEY_ID = env(
    "RAZORPAY_KEY_ID",
    default="",
)

RAZORPAY_KEY_SECRET = env(
    "RAZORPAY_KEY_SECRET",
    default="",
)


# ==============================================================================
# Django Admin branding
# ==============================================================================

ADMIN_SITE_HEADER = "DJ Chemboi Control Room"

ADMIN_SITE_TITLE = "DJ Chemboi Admin"

ADMIN_INDEX_TITLE = "Manage DJ Chemboi Website"