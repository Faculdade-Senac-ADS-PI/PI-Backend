"""
Views de autenticacao e perfil de usuario.

Endpoints implementados:
    - Registro de novos usuarios (publico)
    - Visualizacao e edicao do perfil (autenticado)
    - Alteracao de senha (autenticado)

A autenticacao JWT (login, refresh, blacklist) e feita
pelas views do djangorestframework-simplejwt.
"""
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AlterarSenhaSerializer, RegistroSerializer, UsuarioSerializer

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        summary="Registrar novo usuario",
        description=(
            "Cria uma nova conta na plataforma. "
            "Aceita email, username, senha e dados basicos. "
            "Retorna os dados do usuario criado."
        ),
        tags=["auth"],
    ),
)
class RegistroView(generics.CreateAPIView):
    """
    View de registro de novos usuarios.

    Esta view e PUBLICA (AllowAny) - qualquer pessoa pode criar uma conta.
    Apos o registro, o usuario deve fazer login para obter um token JWT.

    Metodos aceitos:
        - POST: Cria um novo usuario

    Fluxo de registro:
        1. Usuario envia dados via POST
        2. Dados sao validados (email unico, senhas conferem)
        3. Usuario e criado com senha hasheada
        4. Resposta com dados do usuario (sem senha)
        5. Usuario faz login em /api/v1/auth/login/ para obter token
    """

    queryset = User.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="Obter perfil do usuario autenticado",
        description="Retorna todos os dados do perfil do usuario logado.",
        tags=["usuarios"],
    ),
    patch=extend_schema(
        summary="Atualizar perfil do usuario",
        description=(
            "Atualiza parcialmente os dados do perfil. "
            "Apenas os campos enviados serao atualizados."
        ),
        tags=["usuarios"],
    ),
)
class PerfilView(generics.RetrieveUpdateAPIView):
    """
    View de perfil do usuario autenticado.

    Permite ao usuario logado visualizar e editar seu proprio perfil.
    Requer autenticacao JWT.

    Metodos aceitos:
        - GET: Retorna os dados do perfil
        - PATCH: Atualiza parcialmente o perfil
    """

    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Retorna o usuario autenticado.

        Em vez de buscar por ID na URL, retorna sempre
        o usuario que esta fazendo a requisicao (request.user).
        """
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        summary="Alterar senha do usuario",
        description=(
            "Altera a senha do usuario autenticado. "
            "Requer a senha atual para confirmar a identidade."
        ),
        tags=["usuarios"],
        request=AlterarSenhaSerializer,
        responses={200: None},
    ),
)
class AlterarSenhaView(APIView):
    """
    View de alteracao de senha.

    Requer autenticacao JWT e a senha atual do usuario.

    Metodos aceitos:
        - POST: Altera a senha

    Fluxo:
        1. Usuario envia senha atual + nova senha
        2. Senha atual e verificada
        3. Nova senha e validada (regras do Django)
        4. Senha e atualizada
        5. Tokens antigos continuam validos (ate expirar)
    """

    permission_classes = [IsAuthenticated]
    serializer_class = AlterarSenhaSerializer

    def post(self, request):
        """Altera a senha do usuario."""
        serializer = AlterarSenhaSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"mensagem": "Senha alterada com sucesso."},
            status=status.HTTP_200_OK,
        )
