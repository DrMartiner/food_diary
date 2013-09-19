# -*- coding: utf-8 -*-

import sys
import os.path
from os import path

try:
    from settings_local import *
except ImportError:
    print "Don't forget create settings_local.py"

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

SITE_NAME = path.basename(path.realpath(path.curdir))
SITE_ROOT = os.path.join(path.realpath(path.pardir), SITE_NAME)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Alexey Kuzmin', 'DrMaritner@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'food_diary',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

INTERNAL_IPS = ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'media'))

STATIC_URL = '/static/'
STATIC_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'static'))

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if not DEBUG:
    TEMPLATE_LOADERS += ('django.template.loaders.eggs.Loader', )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'constance.context_processors.config',
)

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = SITE_NAME + '.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'admin_honeypot',
    'crispy_forms',
    'djangojs',
    'eml_email_backend',
    'email_html',
    'factory',
    'pytils',
    'registration',
    'robots',
    'smsaero',
    'south',
    'tastypie',

    'apps.api',
    'apps.food',
    'apps.users',
    'django_cleanup',

    'django_coverage',
    'django_factory_boy',
)

ACCOUNT_ACTIVATION_DAYS = 3
AUTH_USER_MODEL = 'users.User'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/users/my-profile/'

CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'
CONSTANCE_SUPERUSER_ONLY = True
CONSTANCE_REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
}
CONSTANCE_CONFIG = {

}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
    },
}

CRISPY_TEMPLATE_PACK = 'bootstrap'

LOGGING_DIR = os.path.join(SITE_ROOT, 'logs')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '(%(asctime)s) %(levelname)s - %(name)s <%(pathname)s:%(lineno)d> "%(message)s"'
        },
        'simple': {
            'format': '>>> %(levelname)s: %(message)s'
        },
        'message': {
            'format': '(%(asctime)s) %(name)s - %(levelname)s: [%(filename)s %(funcName)s %(lineno)d]: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'messages.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'message',
        },
        'request_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'request.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default',],
            'level': 'ERROR',
            'propagate': True
        },
        'console': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler', ],
            'level': 'ERROR',
            'propagate': False
        },
        'notification': {
            'handlers': ['request_handler', ],
            'level': 'ERROR',
            'propagate': False
        },
        'messages': {
            'handlers': ['default', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'collect_okpdtr': {
            'handlers': ['default', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'smsaero': {
            'handlers': ['default', ],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'food.diary88@gmail.com'
DEFAULT_FROM_EMAIL = 'food.diary88@gmail.com'
EMAIL_HOST_PASSWORD = ''

SMSAERO_USER = 'DrMartiner@GMail.Com'
SMSAERO_PASSWORD_MD5 = ''

try:
    from settings_local import *
except ImportError:
    pass