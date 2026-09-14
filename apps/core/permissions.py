"""
Permissoes reutilizaveis para a API.

Permissoes customizadas que podem ser usadas em qualquer view/viewset
do projeto. Combinam com as permissoes padrao do DRF.
"""
from rest_framework.permissions import BasePermission


class EhDonoOuLeitura(BasePermission):
    """
    Permissao que permite:
        - Qualquer usuario autenticado: ler (GET, HEAD, OPTIONS)
        - Apenas o dono do objeto: editar (PUT, PATCH, DELETE)

    Como usar:
        permission_classes = [EhDonoOuLeitura]

    A view precisa ter um atributo 'owner_field' que indica qual
    campo do modelo contem o dono do objeto. Padrao: 'usuario'.

    Exemplo:
        class MinhaViewSet(viewsets.ModelViewSet):
            permission_classes = [EhDonoOuLeitura]
            owner_field = 'autor'  # campo no modelo que referencia o dono
    """

    # Campo padrao que referencia o dono do objeto
    owner_field = "usuario"

    def has_permission(self, request, view):
        # Usuarios autenticados podem acessar a view
        # (leitura e criacao sao controladas por has_object_permission)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Qualquer usuario autenticado pode ler
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # Apenas o dono pode editar/deletar
        owner_field = getattr(view, "owner_field", "usuario")
        return getattr(obj, owner_field, None) == request.user


class EhDonoDoObjeto(BasePermission):
    """
    Permissao que permite acesso APENAS ao dono do objeto.

    Diferente do EhDonoOuLeitura, esta permissao bloqueia
    ate a leitura para quem nao e o dono.

    Como usar:
        permission_classes = [EhDonoDoObjeto]
    """

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "usuario", None) == request.user
