"""
Filtros para a API de servicos.

Define os filtros disponiveis para a listagem de servicos.
Usa django-filter para filtragem avancada de querysets.
"""
import django_filters

from .models import Servico


class ServicoFilter(django_filters.FilterSet):
    """
    Filtros para a listagem de servicos.

    Filtros disponiveis:
        - categoria: Filtra por ID da categoria
        - tipo_preco: Filtra por 'fixo' ou 'a_combinar'
        - localizacao: Busca por localizacao (contem)
        - preco_min: Preco minimo
        - preco_max: Preco maximo
        - autor: Filtra por UUID do autor

    Exemplo de uso:
        GET /api/v1/servicos/?categoria=1&preco_min=100&preco_max=5000
    """

    categoria = django_filters.NumberFilter(
        field_name="categoria__id",
        help_text="Filtra por ID da categoria",
    )
    tipo_preco = django_filters.ChoiceFilter(
        choices=Servico.TipoPreco.choices,
        help_text="Filtra por tipo de preco: 'fixo' ou 'a_combinar'",
    )
    localizacao = django_filters.CharFilter(
        field_name="localizacao",
        lookup_expr="icontains",
        help_text="Busca por localizacao (case-insensitive, contem)",
    )
    preco_min = django_filters.NumberFilter(
        field_name="preco",
        lookup_expr="gte",
        help_text="Preco minimo",
    )
    preco_max = django_filters.NumberFilter(
        field_name="preco",
        lookup_expr="lte",
        help_text="Preco maximo",
    )
    autor = django_filters.UUIDFilter(
        field_name="usuario__id",
        help_text="Filtra por UUID do autor do servico",
    )

    class Meta:
        model = Servico
        fields = [
            "categoria",
            "tipo_preco",
            "localizacao",
            "preco_min",
            "preco_max",
            "autor",
        ]
