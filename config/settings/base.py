"""
Configuracoes BASE do projeto.

Este arquivo contem todas as configuracoes compartilhadas entre
ambientes (desenvolvimento e producao). Cada ambiente pode
sobrescrever essas configuracoes conforme necessario.

Arquivos de ambiente:
    - development.py: Configuracoes para desenvolvimento (DEBUG=True)
    - production.py: Configuracoes para producao (DEBUG=False)
"""
import os
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# A chave secreta NUNCA deve ser commitada no versionamento.
# Ela e carregada do arquivo .env
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-mude-esta-chave-em-producao",
)

# Application definition
# Lista de aplicacoes Django instaladas neste projeto
INSTALLED_APPS = [
    # Apps padrao do Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps de terceiros
    "rest_framework",  # Django REST Framework - framework de API
    "rest_framework_simplejwt",  # Autenticacao JWT
    "rest_framework_simplejwt.token_blacklist",  # Revogacao de tokens
    "corsheaders",  # Controle de CORS
    "django_filters",  # Filtros avancados para querysets
    "drf_spectacular",  # Geracao de documentacao OpenAPI (Swagger)
    # Apps do projeto
    "apps.core",  # Utilidades compartilhadas
    "apps.usuarios",  # Gerenciamento de usuarios
    "apps.servicos",  # Gerenciamento de servicos
]

# Middleware - processam requisicoes/respostas em ordem
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS deve ser o primeiro
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Custom User Model
# Define o modelo de usuario customizado para o projeto
AUTH_USER_MODEL = "usuarios.Usuario"

# Internationalization
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (uploads de imagens)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Django REST Framework
# Configuracoes globais do framework de API
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    # Autenticacao padrao: JWT em todas as rotas protegidas
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Permissao padrao: apenas usuarios autenticados podem acessar
    # Rotas publicas precisam sobrescrever com AllowAny
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # Filtros: busca, filtragem por campos e ordenacao
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Paginacao: 20 itens por pagina
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.PadraoPaginacao",
    "PAGE_SIZE": 20,
    # Gerador de schema OpenAPI para documentacao
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Throttling: limitacao de taxa de requisicoes
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
        "login": "5/min",
    },
    # Handler de excecoes customizado
    "EXCEPTION_HANDLER": "apps.core.exceptions.handler_excecao_customizado",
}

# ---------------------------------------------------------------------------
# SimpleJWT - Configuracao de autenticacao JWT
# ---------------------------------------------------------------------------
from datetime import timedelta

SIMPLE_JWT = {
    # Tempo de vida do access token (curto para seguranca)
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    # Tempo de vida do refresh token (longo para conveniencia)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Rotaciona o refresh token a cada uso (seguranca adicional)
    "ROTATE_REFRESH_TOKENS": True,
    # Invalida o refresh token anterior apos rotacionar
    "BLACKLIST_AFTER_ROTATION": True,
    # Header de autenticacao: Bearer <token>
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ---------------------------------------------------------------------------
# drf-spectacular - Configuracao do gerador de documentacao OpenAPI
# ---------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Plataforma de Servicos API",
    "DESCRIPTION": (
        "API REST para plataforma de divulgacao e venda de servicos. "
        "Permite que profissionais e empresas publiquem seus servicos "
        "e que clientes encontrem e contratem profissionais."
    ),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Separa schemas de entrada e saida nos componentes
    "COMPONENT_SPLIT_REQUEST": True,
    # Prefixo para geracao dos operation_id
    "SCHEMA_PATH_PREFIX": "/api/v1/",
    # Configuracao de seguranca para o Swagger UI (botao Authorize)
    "SECURITY": [{"BearerAuth": []}],
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
    # Tags para organizar os endpoints na documentacao
    "TAGS": [
        {"name": "auth", "description": "Autenticacao e gerenciamento de tokens"},
        {"name": "usuarios", "description": "Gerenciamento de perfis de usuarios"},
        {"name": "servicos", "description": "CRUD de servicos"},
        {"name": "categorias", "description": "Listagem de categorias de servicos"},
    ],
    # Configuracoes do Swagger UI
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": False,
    },
}

# ---------------------------------------------------------------------------
# CORS - Configuracao de acesso cross-origin
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# ---------------------------------------------------------------------------
# Imagens - Tamanhos maximos para upload
# ---------------------------------------------------------------------------
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
