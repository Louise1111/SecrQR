"""
Django settings for backendSecQR project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4lt&iu*l=g(+36vjxf%nd+!_0f#4_r)l*&u#oq(690v9f(8p52"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# The `ALLOWED_HOSTS` setting in Django specifies a list of strings representing the host/domain names
# that this Django site can serve. When `DEBUG` is set to `False`, Django will only allow requests
# with a `Host` header that matches one in this list.
ALLOWED_HOSTS = ['localhost', 'Lc1223.pythonanywhere.com']
VIRUS_TOTAL_API_KEY ="a759ba9c8a836e1bde3da7da0567d32842fa186ffaf1999f5cdbeff92e519fa8"
APP_PREFIX = 'SecQR'
AUTH_USER_MODEL="account.User"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "account",
    "corsheaders",
    "secqr_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.common.CommonMiddleware",
    
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Require authentication for all views
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',  # Add MultiPartParser for file uploads
    ],
}
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
CORS_ALLOWED_ORIGINS = []

ROOT_URLCONF = "backendSecQR.urls"

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

WSGI_APPLICATION = "backendSecQR.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'secqr',
#         'USER': 'root',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',  # or the hostname where your MySQL server is running
#         'PORT': '3306',      # or the port on which your MySQL server is listening
#     }
# }

DATABASES = {
    'default': {
        
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'VewNruQJVFKvhSrXIAIPZIASzeozKRwb',
        'HOST': 'viaduct.proxy.rlwy.net',
        'PORT': '37248',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'account.jwt.JWTAuthentication',
    ]
    
}
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = 'media/'

MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


import os
from django.core.mail.backends.smtp import EmailBackend
STATIC_ROOT= os.path.join(BASE_DIR, 'static')

# Email backend configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # Gmail SMTP server
EMAIL_PORT = 587  # Gmail SMTP port
EMAIL_USE_TLS = True  # Gmail requires TLS

# Replace these placeholders with your actual Gmail email address and password
EMAIL_HOST_USER = 'secqr_app@outlook.com'  # Your Gmail email address
EMAIL_HOST_PASSWORD = 'SecQr@1919'  # Your Gmail password

DEFAULT_FROM_EMAIL = 'secqr_app@outlook.com'  # Your Gmail email address