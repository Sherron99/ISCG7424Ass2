"""
WSGI config for ISCG7424_Assi2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ISCG7424_Assi2.settings')

# application = get_wsgi_application()
app = get_wsgi_application() #这一步更改了