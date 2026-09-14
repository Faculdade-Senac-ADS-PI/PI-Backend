"""
Configuracoes de DESENVOLVIMENTO.

Usadas quando o projeto roda localmente para desenvolvimento.
DEBUG=True, erros detalhados, emails no console.
"""
from .base import *  # noqa: F401, F403
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ---------------------------------------------------------------------------
# Banco de dados
#
# POR PADRAO, o projeto usa SQLite em desenvolvimento. Isso permite
# rodar o projeto imediatamente sem precisar configurar o PostgreSQL.
#
# Para usar PostgreSQL, defina no .env:
#   DB_ENGINE=postgresql
#   DB_NAME=plataforma_servicos
#   DB_USER=postgres
#   DB_PASSWORD=sua_senha
#   DB_HOST=localhost
#   DB_PORT=5432
#
# Voce tambem precisa criar o banco antes (via pgAdmin ou psql):
#   CREATE DATABASE plataforma_servicos;
# ---------------------------------------------------------------------------
if config("DB_ENGINE", default="sqlite") == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST", default="localhost"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    # SQLite - banco em arquivo simples (django.db), perfeito para dev
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Email: imprime emails no console (nao envia de verdade)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# CORS: permite todas as origens em desenvolvimento
CORS_ALLOW_ALL_ORIGINS = True

# Debug Toolbar (opcional - descomente se quiser usar)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
# INTERNAL_IPS = ["127.0.0.1"]

# Log detalhado no console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
