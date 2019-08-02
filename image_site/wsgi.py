"""
WSGI config for image_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_site.settings')
sys.path.append('C:/Users/a_qua/Desktop/Own/Projects/image_server/image_site')
sys.path.append('C:/Users/a_qua/Desktop/Own/Projects/image_server/image_site/image_site')
sys.path.append('C:/Users/a_qua/Desktop/Own/Projects/image_server/image_site/views')

application = get_wsgi_application()
