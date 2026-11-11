"""
ASGI config for Fake Job Detection project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Update both files to look like this:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeJobDetection.settings')

application = get_asgi_application()
