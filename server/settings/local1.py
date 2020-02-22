from .base import *
from server import env
DEBUG = True
ALLOWED_HOSTS = ["0.0.0.0","localhost",'127.0.0.1','mysite',"www.localhost"]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'structure_7_2_2020',
        'USER': 'myuser',
        'PASSWORD': 'mypass', 
        'HOST': 'localhost',
        'PORT': 5432
    }
}
LOGIN_REDIRECT_URL = '/projects/'