# -*- coding: utf-8 -*-

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# EMAIL_BACKEND = 'eml_email_backend.EmailBackend'
# EMAIL_FILE_PATH = 'media/emails/'