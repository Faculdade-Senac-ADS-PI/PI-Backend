"""
Configuracao do painel administrativo para servicos e categorias.

O Django Admin permite gerenciar servicos e categorias em:
    http://127.0.0.1:8000/admin/servicos/
"""
from django.contrib import admin

from .models import Categoria, Servico


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """Painel administrativo do modelo Categoria."""

    # Campos exibidos na listagem
    list_display = ("nome", "icone", "total_servicos")

    # Campos que podem ser usados na busca
    search_fields = ("nome", "descricao")

    def total_servicos(self, obj):
        """Retorna o total de servicos na categoria."""
        return obj.servicos.count()

    total_servicos.short_description = "Servicos"


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    """Painel administrativo do modelo Servico."""

    # Campos exibidos na listagem
    list_display = (
        "titulo",
        "usuario",
        "categoria",
        "preco",
        "tipo_preco",
        "ativo",
        "criado_em",
    )

    # Campos que podem ser usados na busca
    search_fields = ("titulo", "descricao", "usuario__email")

    # Filtros laterais
    list_filter = ("ativo", "tipo_preco", "categoria", "criado_em")

    # Campos editaveis diretamente na listagem
    list_editable = ("ativo", "preco")

    # Formulario de edicao
    fieldsets = (
        ("Informacoes do Servico", {
            "fields": ("usuario", "titulo", "descricao", "categoria"),
        }),
        ("Preco e Localizacao", {
            "fields": ("preco", "tipo_preco", "localizacao"),
        }),
        ("Status", {
            "fields": ("ativo",),
        }),
    )

    # Otimiza a listagem evitando consultas N+1
    list_select_related = ("usuario", "categoria")

    def get_queryset(self, request):
        """Otimiza as consultas usando select_related."""
        qs = super().get_queryset(request)
        return qs.select_related("usuario", "categoria")