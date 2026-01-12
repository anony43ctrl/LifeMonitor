"""
Django settings for user_monitoring project.
"""

from pathlib import Path
import os
import json
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- DYNAMIC DATABASE CONFIGURATION START ---
# Check if we are running on Android (or passed a specific data path)
android_data_path = os.environ.get("ANDROID_DATA_PATH")

if android_data_path:
    # We are on mobile/packaged app: Use the writable data directory
    data_dir = Path(android_data_path)
    # Create the folder if it doesn't exist
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
        
    current_db_path = data_dir / 'db.sqlite3'
    # Use the config file from the writable area, not the read-only install area
    DB_CONFIG_FILE = data_dir / 'db_config.json'

else:
    # We are on Desktop/Dev: Use the local source folder
    DB_CONFIG_FILE = BASE_DIR / 'db_config.json'
    DEFAULT_DB_PATH = BASE_DIR / 'db.sqlite3'
    current_db_path = DEFAULT_DB_PATH

# Load dynamic config if it exists
if DB_CONFIG_FILE.exists():
    try:
        with open(DB_CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
            # load path and convert to Path object
            saved_path = config_data.get('db_path')
            if saved_path:
                current_db_path = Path(saved_path)
    except Exception as e:
        print(f"Error loading db_config.json: {e}")

# --- DYNAMIC DATABASE CONFIGURATION END ---

SECRET_KEY = "django-insecure-*jyp*=#f&6n7opvn48bh#m*y=x7m)q*-lg9(7s&4h%jl!0ron@"

DEBUG = True

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "monitor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "user_monitoring.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = "user_monitoring.wsgi.application"

# Database Configuration using the dynamic path
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': current_db_path,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "monitor/static",
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# --- ANDROID STATIC FILES CONFIG (CRITICAL) ---
# 1. Tell WhiteNoise to find files in your source folders dynamically
WHITENOISE_USE_FINDERS = True

# 2. Use basic storage. Do NOT use Manifest/Compressed storage on Android.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# DELETE or COMMENT OUT this line if it exists:
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"