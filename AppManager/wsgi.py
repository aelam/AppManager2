# coding: utf-8
"""
WSGI config for AppManager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys

DIRNAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DIRNAME)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AppManager.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
