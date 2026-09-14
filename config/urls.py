"""
Rotas principais do projeto.

Organiza as URLs em dois grupos:
    1. URLs administrativas (/admin/)
    2. URLs da API (/api/v1/)

A documentacao da API (Swagger/ReDoc) esta disponivel em:
    GET /api/docs/        -> Swagger UI interativo
    GET /api/redoc/       -> ReDoc documentacao
    GET /api/schema/      -> Schema OpenAPI (YAML/JSON)
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Admin do Django
    path("admin/", admin.site.urls),

    # API v1 - rotas de autenticacao
    path(
        "api/v1/auth/",
        include("apps.usuarios.urls"),
    ),

    # API v1 - rotas de servicos e categorias (usam Router)
    path("api/v1/", include("apps.servicos.urls")),

    # Documentacao OpenAPI (Swagger)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# Em desenvolvimento, serve o diretorio /media/ para as imagens
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)