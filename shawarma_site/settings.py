"""
Django settings for shawarma_site project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# import raven
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import psycopg2.extensions
from .my_settings import db_name, db_login, db_password, static_root, media_root, MY_SECRET_KEY, dadata_token, \
    raven_dsn, \
    allowed_hosts, debug_flag, shaw_queue_url, check_order_status_url, get_menu_url, send_order_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MY_SECRET_KEY

# SECURITY WARNING: keep the secret key used in production secret!
DADATA_TOKEN = dadata_token

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = debug_flag

ALLOWED_HOSTS = allowed_hosts

# Application definition

INSTALLED_APPS = [
    'customer_interface.apps.CustomerInterfaceConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shawarma_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shawarma_site.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': db_login,
        'PASSWORD': db_password,
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s \n'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'file_request': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_request.log',
            'formatter': 'verbose'
        },
        'file_server': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_server.log',
            'formatter': 'verbose'
        },
        'file_template': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_template.log',
            'formatter': 'verbose'
        },
        'file_db': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'log/debug_db.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file_request'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.server': {
            'handlers': ['file_server'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.template': {
            'handlers': ['file_template'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file_db'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru'  # Django 3.0 got new form of language code. Was 'ru-RU'.

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/



STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'customer_interface', 'static'),
)

STATIC_URL = '/static/'
STATIC_ROOT = static_root

MEDIA_URL = '/media/'
MEDIA_ROOT = media_root

# RAVEN_CONFIG = {
#     'dsn': raven_dsn,
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
#     'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
# }

sentry_sdk.init(
    dsn=raven_dsn,
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

SHAW_QUEUE_URL = shaw_queue_url
CHECK_ORDER_STATUS_URL = check_order_status_url
GET_MENU_URL = get_menu_url
SEND_ORDER_URL = send_order_url

try:
    from .local_settings import *
except:
    pass

