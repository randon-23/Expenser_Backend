"""
ASGI config for backend_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import environ
from django.core.asgi import get_asgi_application

env = environ.Env()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 
    'backend_project.settings.prod' if env("DJANGO_ENV", default="development") == "production" else "backend_project.settings.dev"
)

application = get_asgi_application()
