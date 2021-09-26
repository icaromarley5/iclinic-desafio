"""
Django settings for iclinic_api project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ["DEBUG"] == "True"

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

# Application definition

INSTALLED_APPS = [
    "api",
    "rest_framework",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "iclinic_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
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

WSGI_APPLICATION = "iclinic_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
if os.environ["CI"] != "False":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        },
    }
else:
    DATABASE_URL = os.environ["DATABASE_URL"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "USER": DATABASE_URL.split("//")[1].split(":")[0],
            "NAME": DATABASE_URL.split("//")[1].split("/")[1],
            "PASSWORD": DATABASE_URL.split("//")[1].split("@")[0].split(":")[1],
            "HOST": DATABASE_URL.split("//")[1].split("@")[1].split(":")[0],
            "PORT": DATABASE_URL.split("//")[1]
            .split("@")[1]
            .split(":")[1]
            .split("/")[0],
        },
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# cache
if os.environ["CI"] != "False":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ["REDIS_URL"],
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# services
# PHYSICIANS SERVICE
PHYSICIANS_URL = os.environ["PHYSICIANS_URL"]
PHYSICIANS_TOKEN = os.environ["PHYSICIANS_TOKEN"]
PHYSICIANS_TIMEOUT_SECONDS = int(os.environ["PHYSICIANS_TIMEOUT_SECONDS"])
PHYSICIANS_RETRIES = int(os.environ["PHYSICIANS_RETRIES"])
PHYSICIANS_CACHE_TTL_HOURS = int(os.environ["PHYSICIANS_CACHE_TTL_HOURS"])
# CLINICS SERVICE
CLINICS_URL = os.environ["CLINICS_URL"]
CLINICS_TOKEN = os.environ["CLINICS_TOKEN"]
CLINICS_TIMEOUT_SECONDS = int(os.environ["CLINICS_TIMEOUT_SECONDS"])
CLINICS_RETRIES = int(os.environ["CLINICS_RETRIES"])
CLINICS_CACHE_TTL_HOURS = int(os.environ["CLINICS_CACHE_TTL_HOURS"])
# PATIENTS SERVICE
PATIENTS_URL = os.environ["PATIENTS_URL"]
PATIENTS_TOKEN = os.environ["PATIENTS_TOKEN"]
PATIENTS_TIMEOUT_SECONDS = int(os.environ["PATIENTS_TIMEOUT_SECONDS"])
PATIENTS_RETRIES = int(os.environ["PATIENTS_RETRIES"])
PATIENTS_CACHE_TTL_HOURS = int(os.environ["PATIENTS_CACHE_TTL_HOURS"])
# METRICS SERVICE
METRICS_URL = os.environ["METRICS_URL"]
METRICS_TOKEN = os.environ["METRICS_TOKEN"]
METRICS_TIMEOUT_SECONDS = int(os.environ["METRICS_TIMEOUT_SECONDS"])
METRICS_RETRIES = int(os.environ["METRICS_RETRIES"])
METRICS_CACHE_TTL_HOURS = int(os.environ["METRICS_CACHE_TTL_HOURS"])

# static
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
# sentry
if os.environ.get("SENTRY_URL"):
    sentry_sdk.init(
        dsn=os.environ["SENTRY_URL"],
        integrations=[DjangoIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
    )
