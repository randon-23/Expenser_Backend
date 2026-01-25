from .base import *
import os

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = ["192.168.1.232"]  # add domain later
CORS_ALLOW_ALL_ORIGINS = False

#on server set 
#export DJANGO_SETTINGS_MODULE=backend_project.settings.prod
#export DJANGO_SECRET_KEY="a-long-random-prod-key"