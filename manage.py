#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Arquivo gerenciador do projeto. Usado para executar comandos como:
    python manage.py runserver
    python manage.py migrate
    python manage.py createsuperuser
"""
import os
import sys


def main():
    """Executa tarefas administrativas do Django."""
    # Define o modulo de configuracao padrao baseado na variavel de ambiente
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Nao foi possivel importar o Django. Verifique se o Django esta "
            "instalado e acessivel no seu ambiente virtual. "
            "Execute: uv pip install django"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
