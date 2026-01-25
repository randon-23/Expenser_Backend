from .base import *
import os
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env")) 

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.232',
]

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:19006",      # Expo dev
#     "http://localhost:8081",       # React Native Metro
#     "exp://*",                     # Expo tunnel
#     "http://127.0.0.1:19006",
# ]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b^)3lbua98(7*(jdx2lw11u)aoz+0@)%$z(4)-83s&)()og1+p'
