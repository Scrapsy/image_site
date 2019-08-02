import os, sys

sys.path.append('C:\Users\a_qua\Desktop\Own\Projects\image_server\image_site')
os.environ['DJANGO_SETTINGS_MODULE'] = 'image_site.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()