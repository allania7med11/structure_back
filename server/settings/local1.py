from .base import *
from server import env
DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "structure_7_2_2020",
        "USER": "myuser",
        "PASSWORD": "mypass", 
        "HOST": "localhost",
        "PORT": 5432
    }
}
LOGIN_REDIRECT_URL = "/projects/"

SOCIAL_AUTH_FACEBOOK_KEY = 209512163258895        # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = "5f5cc19b0f382d4a947241775dc503c5"  # App Secret