from .base import *
DEBUG = False
ALLOWED_HOSTS = [
    "0.0.0.0","localhost",'127.0.0.1',
    'legacy.effectivewebapp.com',"165.22.119.28","www.legacy.effectivewebapp.com"]
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
LOGIN_REDIRECT_URL = "legacy.effectivewebapp.com" + '/projects/'