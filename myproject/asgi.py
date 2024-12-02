"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

django_app = get_asgi_application()
from fast_api import app as fastapi_app

# We don't need to create a new FastAPI instance here
# Just use the one from fast_api.py
app = fastapi_app