"""
Views de servicos e categorias.

Endpoints implementados:
    - CRUD completo de servicos (ViewSet com Router)
    - Listagem de categorias

O ViewSet automaticamente gera os endpoints:
    - GET    /servicos/          -> list
    - POST   /servicos/          -> create
    - GET    /servicos/{id}/     -> retrieve
    - PUT    /servicos/{id}/     -> update
    - PATCH  /servicos/{id}/     -> partial_update
    - DELETE /servicos/{id}/     -> destroy
"""
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import EhDonoOuLeitura

from .filters import ServicoFilter
from .models import Categoria, Servico
from .serializers import (
    CategoriaSerializer,
    ServicoCreateUpdateSerializer,
    ServicoDetailSerializer,
    ServicoListSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Listar servicos",
        description=(
            "Retorna lista paginada de servicos ativos. "
            "Suporta busca por titulo/descricao, filtragem por "
            "categoria, tipo_preco e localizacao."
        ),
        tags=["servicos"],
    ),
    create=extend_schema(
        summary="Criar novo servico",
        description=(
            "Cria um novo servico vinculado ao usuario autenticado. "
            "O campo 'usuario' e definido automaticamente."
        ),
        tags=["servicos"],
    ),
    retrieve=extend_schema(
        summary="Detalhar servico",
        description="Retorna todos os dados de um servico especifico.",
        tags=["servicos"],
    ),
    update=extend_schema(
        summary="Atualizar servico (completo)",
        description="Atualiza todos os campos de um servico. Apenas o autor pode editar.",
        tags=["servicos"],
    ),
    partial_update=extend_schema(
        summary="Atualizar servico (parcial)",
        description="Atualiza apenas os campos enviados. Apenas o autor pode editar.",
        tags=["servicos"],
    ),
    destroy=extend_schema(
        summary="Remover servico",
        description="Remove um servico. Apenas o autor pode remover.",
        tags=["servicos"],
    ),
)
class ServicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de servicos.

    Fornece CRUD completo para servicos com:
        - Listagem paginada com busca e filtros
        - Criacao vinculada ao usuario autenticado
        - Edicao apenas pelo autor do servico
        - Visualizacao publica (requer autenticacao)

    Permissoes:
        - Leitura (GET): Apenas autenticados
        - Criacao (POST): Apenas autenticados
        - Edicao (PUT/PATCH): Apenas o autor
        - Remocao (DELETE): Apenas o autor

    Filtros disponiveis:
        - search: Busca por titulo e descricao
        - categoria: Filtra por ID da categoria
        - tipo_preco: Filtra por 'fixo' ou 'a_combinar'
        - localizacao: Busca por localizacao
        - ativo: Filtra por status (true/false)
        - ordering: Ordena por 'preco', 'criado_em', 'titulo'

    Exemplo de uso com filtros:
        GET /api/v1/servicos/?search=desenvolvimento&categoria=1&ordering=preco
    """

    permission_classes = [IsAuthenticated, EhDonoOuLeitura]
    filterset_class = ServicoFilter
    search_fields = ["titulo", "descricao"]
    ordering_fields = ["preco", "criado_em", "titulo"]
    ordering = ["-criado_em"]

    def get_queryset(self):
        """
        Retorna apenas servicos ativos.

        Otimiza as queries usando select_related para evitar
        o problema N+1 (uma query extra por servico).
        """
        return Servico.objects.filter(
            ativo=True
        ).select_related("usuario", "categoria")

    def get_serializer_class(self):
        """
        Seleciona o serializer baseado na acao.

        - list: Serializer leve (listagem)
        - retrieve: Serializer completo (detalhes)
        - create/update: Serializer de escrita
        """
        if self.action == "list":
            return ServicoListSerializer
        if self.action == "retrieve":
            return ServicoDetailSerializer
        return ServicoCreateUpdateSerializer

    def perform_create(self, serializer):
        """
        Cria o servico vinculado ao usuario autenticado.

        O campo 'usuario' e definido automaticamente a partir
        do usuario que esta fazendo a requisicao.
        """
        serializer.save(usuario=self.request.user)

    @extend_schema(
        summary="Meus servicos",
        description=(
            "Retorna apenas os servicos do usuario autenticado. "
            "Inclui servicos inativos."
        ),
        tags=["servicos"],
    )
    def list(self, request, *args, **kwargs):
        """
        Sobrescreve o list para retornar apenas servicos do usuario.

        Se o parametro 'meus=true' for passado, retorna apenas
        os servicos do usuario autenticado.
        """
        meus = request.query_params.get("meus", "false").lower() == "true"

        if meus:
            # Retorna apenas servicos do usuario (incluindo inativos)
            queryset = Servico.objects.filter(
                usuario=request.user
            ).select_related("usuario", "categoria")
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar categorias",
        description=(
            "Retorna todas as categorias de servicos disponiveis. "
            "Cada categoria inclui o total de servicos ativos."
        ),
        tags=["categorias"],
    ),
    retrieve=extend_schema(
        summary="Detalhar categoria",
        description="Retorna os dados de uma categoria especifica.",
        tags=["categorias"],
    ),
)
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listagem de categorias.

    As categorias sao somente leitura - nao podem ser criadas
    ou editadas pela API. Elas sao gerenciadas pelo Django Admin.

    Endpoints:
        - GET /api/v1/categorias/        -> Lista todas as categorias
        - GET /api/v1/categorias/{id}/   -> Detalha uma categoria

    Exemplo de resposta:
        {
            "count": 10,
            "results": [
                {
                    "id": 1,
                    "nome": "Desenvolvimento Web",
                    "descricao": "Criacao de sites e sistemas web",
                    "icone": "💻",
                    "quantidade_servicos": 15
                },
                ...
            ]
        }
    """

    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Categorias nao precisam de paginacao
