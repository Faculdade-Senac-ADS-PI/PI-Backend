"""
Rotas de URL do app de servicos.

Endpoints de servicos e categorias:
    GET    /api/v1/servicos/          -> Lista servicos
    POST   /api/v1/servicos/          -> Cria servico
    GET    /api/v1/servicos/{id}/     -> Detalha servico
    PUT    /api/v1/servicos/{id}/     -> Atualiza servico
    PATCH  /api/v1/servicos/{id}/     -> Atualiza parcialmente
    DELETE /api/v1/servicos/{id}/     -> Remove servico
    GET    /api/v1/servicos/?meus=true -> Apenas servicos do usuario

    GET    /api/v1/categorias/        -> Lista categorias
    GET    /api/v1/categorias/{id}/   -> Detalha categoria
"""
from rest_framework.routers import DefaultRouter

from .views import CategoriaViewSet, ServicoViewSet

# Router do DRF - gera automaticamente os endpoints CRUD
# padrao (rota, viewset, basename)
router = DefaultRouter()
router.register("servicos", ServicoViewSet, basename="servicos")
router.register("categorias", CategoriaViewSet, basename="categorias")

urlpatterns = router.urls