"""
Configuracao WSGI para o projeto.

WSGI (Web Server Gateway Interface) e o protocolo padrao
entre servidores web e aplicacoes Python.

Usado em producao por servidores como Gunicorn.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_wsgi_application()