"""
WSGI config for TestHelper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application



sys.path.insert(0, os.path.dirname(__file__)) 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TestHelper.settings")

application = get_wsgi_application()
