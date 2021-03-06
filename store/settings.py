"""
Django settings for store project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from decouple import config, Csv

# Settings dir folder
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))

# Project's root folder
BASE_DIR = os.path.dirname(SETTINGS_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local apps
    "account",
    "client",
    "product",
    "order",
    # third part django packages
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "drf_yasg",
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

ROOT_URLCONF = "store.urls"

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

WSGI_APPLICATION = "store.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME", cast=str),
        "USER": config("DATABASE_USER", cast=str),
        "PASSWORD": config("DATABASE_PASS", cast=str),
        "HOST": config("DATABASE_HOST", cast=str),
        "PORT": config("DATABASE_PORT", cast=str),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"}, # pylint: disable=line-too-long
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, # pylint: disable=line-too-long
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"}, # pylint: disable=line-too-long
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"} # pylint: disable=line-too-long
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = config("TIMEZONE", cast=str)

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(SETTINGS_DIR, "static_files")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(SETTINGS_DIR, "media")


# Custom User
AUTH_USER_MODEL = "account.User"


# Django Rest Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
}

JWT_AUTH = {
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=3),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
    "JWT_ALLOW_REFRESH": True,
    "JWT_AUTH_HEADER_PREFIX": "JWT",
}


# Url append slash
APPEND_SLASH = True


# For email purpose
FRONTEND_URL = config("FRONTEND_URL", cast=str)

# Email settings
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=str)


# sentry settings
if DEBUG is False:
    sentry_sdk.init(
        dsn=config("SENTRY_DNS", default="", cast=str),
        integrations=[DjangoIntegration()],

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )
