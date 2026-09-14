"""
Paginacao padrao da API.

Define como as respostas de listas sao paginadas.
Todas as respostas de listagem usam esta paginacao por padrao.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PadraoPaginacao(PageNumberPagination):
    """
    Paginacao padrao com 20 itens por pagina.

    Formato da resposta:
    {
        "count": 100,          // Total de itens
        "total_pages": 5,      // Total de paginas
        "current_page": 1,     // Pagina atual
        "next": "...",         // URL da proxima pagina
        "previous": null,      // URL da pagina anterior
        "results": [...]       // Itens da pagina atual
    }

    Parametros de consulta aceitos:
        - page: Numero da pagina (padrao: 1)
        - page_size: Itens por pagina (padrao: 20, maximo: 100)
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "count": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
