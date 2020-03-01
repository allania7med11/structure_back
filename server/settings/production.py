from .base import *
DEBUG = False
ALLOWED_HOSTS = ['effectivewebapp.com',"178.62.22.165","www.effectivewebapp.com"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'structurefull',
        'USER': "ah",
        'PASSWORD': "1993",
        'HOST': 'localhost',
        'PORT': '',
    }
}
LOGIN_REDIRECT_URL = '/projects/'