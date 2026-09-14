"""
Configuracao ASGI para o projeto.

ASGI (Asynchronous Server Gateway Interface) e o protocolo
assincrono moderno do Python. Suporta WebSockets e outras
comunicacoes em tempo real.

Usado pelo Daphne ou Uvicorn em desenvolvimento e producao.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# Garante que o Django e inicializado antes de importar as rotas
application = get_asgi_application()