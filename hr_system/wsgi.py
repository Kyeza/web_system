"""
WSGI config for hr_system project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('C:/Users/administrator.SCIUGKLA/Bitnami Django Stack projects/hr_system')
os.environ.setdefault("PYTHON_EGG_CACHE", "C:/Users/administrator.SCIUGKLA/Bitnami Django Stack projects/hr_system/egg_cache")


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_system.settings')

application = get_wsgi_application()

