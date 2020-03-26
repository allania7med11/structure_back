from .base import *
DEBUG = False
ALLOWED_HOSTS = [
    'effectivewebapp.com',
    "206.189.117.238",
    "www.effectivewebapp.com",
    "about.effectivewebapp.com"]
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

SOCIAL_AUTH_FACEBOOK_KEY = 642560686562639        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "582ae889d77decc2fd5d7a44690c2bf8"  # App Secret