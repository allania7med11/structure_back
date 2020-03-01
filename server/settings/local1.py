from .base import *
from server import env
DEBUG = True
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "initial",
        "USER": "myuser",
        "PASSWORD": "mypass", 
        "HOST": "localhost",
        "PORT": 5432
    }
}
LOGIN_REDIRECT_URL = "/projects/"