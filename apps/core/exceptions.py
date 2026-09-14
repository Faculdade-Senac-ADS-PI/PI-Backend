"""
Handler de excecoes customizado.

Padroniza o formato de erro retornado por toda a API.
Em vez de usar o formato padrao do DRF, retornamos:
{
    "erro": true,
    "status_code": 400,
    "mensagem": "Descricao do erro",
    "detalhes": { ... }  // Opcional, detalhes adicionais
}
"""
from rest_framework.response import Response
from rest_framework.views import exception_handler


def handler_excecao_customizado(exc, context):
    """
    Handler customizado para excecoes do DRF.

    Este handler intercepta todas as excecoes levantadas pelas views
    do DRF e formata a resposta de erro de forma padronizada.

    Excecoes tratadas:
        - ValidationError: Erros de validacao (400)
        - NotFound: Recurso nao encontrado (404)
        - PermissionDenied: Sem permissao (403)
        - NotAuthenticated: Nao autenticado (401)
        - Throttled: Limite de requisicoes (429)
    """
    # Deixa o DRF tratar as excecoes primeiro
    response = exception_handler(exc, context)

    if response is not None:
        # Formata a resposta de erro
        erro_data = {
            "erro": True,
            "status_code": response.status_code,
        }

        # Adiciona mensagem de erro detalhada
        if hasattr(exc, "detail"):
            if isinstance(exc.detail, dict):
                erro_data["mensagem"] = "Erro de validacao"
                erro_data["detalhes"] = response.data
            elif isinstance(exc.detail, list):
                erro_data["mensagem"] = exc.detail[0] if exc.detail else "Erro desconhecido"
            else:
                erro_data["mensagem"] = str(exc.detail)

        response.data = erro_data

    return response
