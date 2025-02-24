"""
Django settings for music_muse project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import sentry_sdk
from enum import StrEnum
from pathlib import Path
from typing import assert_never

import environ
import tomllib
from dj_easy_log import load_loguru
from dotenv import load_dotenv


class FileStoragesTypes(StrEnum):
    LOCAL = "local"
    S3 = "s3"


load_dotenv()

load_loguru(globals())
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PYPROJECT_PATH = os.path.join(BASE_DIR, "pyproject.toml")

with open(PYPROJECT_PATH, "rb") as pyproject_file:
    pyproject_data = tomllib.load(pyproject_file)
    PROJECT_VERSION = pyproject_data["tool"]["poetry"]["version"]

ENV_FILE = ".env"
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

if os.path.exists(os.path.join(BASE_DIR, ENV_FILE)):
    environ.Env.read_env(os.path.join(BASE_DIR, ENV_FILE))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)

HEALTH_SECRET_TOKEN = env("HEALTH_SECRET_TOKEN")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "176.57.213.174",
    "musicmuse-preprod.ru",
    "musicmuse.ru",
    "mlkhall-musicmuseservice-ef0e.twc1.net",
    "91.186.196.162",
]

CSRF_TRUSTED_ORIGINS = [
    "https://musicmuse.ru",
]

# Application definition

INSTALLED_APPS = [
    "embed_video",
    "storages",
    "django_opensearch_dsl",
    "django_prometheus",
    "django_countries",
    "ninja",
    "ninja_apikey",
    "pictures",
    "import_export",
    "django_filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.music.apps.MusicConfig",
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "health_check.contrib.s3boto3_storage",  # requires boto3 and S3BotoStorage backend
    "health_check.contrib.migrations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
    "ninja_put_patch_file_upload_middleware.middlewares.process_put_patch",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "core.wsgi.application"

PICTURES = {
    "BREAKPOINTS": {
        "xs": 576,
        "s": 768,
        "m": 992,
        "l": 1200,
        "xl": 1400,
    },
    "GRID_COLUMNS": 12,
    "CONTAINER_WIDTH": 1200,
    "FILE_TYPES": ["WEBP"],
    "PIXEL_DENSITIES": [1, 2],
    "USE_PLACEHOLDERS": True,
    "QUEUE_NAME": "pictures",
    "PROCESSOR": "pictures.tasks.process_picture",
}
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_prometheus.db.backends.postgresql",
        "NAME": env("POSTGRESQL_DBNAME"),
        "HOST": env("POSTGRESQL_HOST"),
        "PORT": env("POSTGRESQL_PORT"),
        "USER": env("POSTGRESQL_USER"),
        "PASSWORD": env("POSTGRESQL_PASSWORD"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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

OPENSEARCH_DSL = {
    "default": {
        "hosts": [
            {
                "scheme": "https",
                "host": env("OPENSEARCH_HOST"),
                "port": env("OPENSEARCH_PORT"),
            }
        ],
        "http_auth": (env("OPENSEARCH_USERNAME"), env("OPENSEARCH_PASSWORD")),
        "use_ssl": True,
        "verify_certs": False,
        "headers": {"securitytenant": "default_tenant"},
    },
}


sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ru-Ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
FILE_UPLOAD_STORAGE = env(var="FILE_UPLOAD_STORAGE", default=FileStoragesTypes.S3)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Настройки AWS
STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

# Настройки для S3
S3_DOMAIN = env("S3_DOMAIN")
S3_CUSTOM_DOMAIN = f"{STORAGE_BUCKET_NAME}.{S3_DOMAIN}"


default_storages_options = {
    "access_key": env("AWS_ACCESS_KEY_ID"),
    "secret_key": env("AWS_SECRET_ACCESS_KEY"),
    "bucket_name": env("AWS_STORAGE_BUCKET_NAME"),
    "region_name": env("AWS_S3_REGION_NAME"),
    "custom_domain": S3_CUSTOM_DOMAIN,
    "endpoint_url": f"https://{S3_DOMAIN}",
    "use_ssl": True,
}


match FILE_UPLOAD_STORAGE:
    case FileStoragesTypes.S3:
        # Настройки для хранения медиафайлов
        MEDIA_URL = f"https://{S3_CUSTOM_DOMAIN}/media/"

        STORAGES = {
            "default": {
                "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
                "OPTIONS": default_storages_options,
            },
            "staticfiles": {
                "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
                "OPTIONS": default_storages_options,
            },
            "private": {
                "BACKEND": "core.storage_backends.PrivateMediaStorage",
                "OPTIONS": default_storages_options,
            },
            "public": {
                "BACKEND": "core.storage_backends.PublicMediaStorage",
                "OPTIONS": default_storages_options,
            },
        }

        # Настройки для хранения статических файлов
        STATIC_URL = f"https://{S3_CUSTOM_DOMAIN}/static/"
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, "assets"),
            os.path.join(BASE_DIR, "static"),
        ]

    case FileStoragesTypes.LOCAL:
        MEDIA_ROOT_NAME = "media"
        MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
        MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"

        STATIC_URL = "/static/"
        STATIC_ROOT = os.path.join(BASE_DIR, "static")
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, "assets"),
        ]

    case _:
        assert_never(FileStoragesTypes)

S3_STATIC_LOCATION = "static"
S3_PUBLIC_MEDIA_LOCATION = "media/public"
S3_PRIVATE_MEDIA_LOCATION = "media/private"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
