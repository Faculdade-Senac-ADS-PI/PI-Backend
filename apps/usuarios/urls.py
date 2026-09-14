"""
Rotas de URL do app de usuarios.

Endpoints de autenticacao desta aplicacao:
    POST /api/v1/auth/register/           -> Registro de novo usuario
    POST /api/v1/auth/login/              -> Login (gera tokens JWT)
    POST /api/v1/auth/token/refresh/      -> Renova access token
    POST /api/v1/auth/token/verify/       -> Verifica token
    GET/PATCH /api/v1/auth/profile/       -> Perfil do usuario
    POST /api/v1/auth/change-password/    -> Alterar senha

Os endpoints de token (login, refresh, verify) usam as views
padrao do djangorestframework-simplejwt.
"""
from django.urls import path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import AlterarSenhaView, PerfilView, RegistroView


@extend_schema_view(
    post=extend_schema(
        summary="Login (obter tokens JWT)",
        description=(
            "Autentica o usuario e retorna os tokens JWT. "
            "Envie email e password para receber access e refresh tokens."
        ),
        tags=["auth"],
    ),
)
class LoginView(TokenObtainPairView):
    """View de login - gera tokens JWT de acesso e refresh."""


@extend_schema_view(
    post=extend_schema(
        summary="Renovar access token",
        description=(
            "Envia um refresh token valido para receber um novo access token. "
            "Como a rotacao esta ativa, um novo refresh token tambem e emitido."
        ),
        tags=["auth"],
    ),
)
class RefreshView(TokenRefreshView):
    """View de renovacao do access token."""


@extend_schema_view(
    post=extend_schema(
        summary="Verificar token",
        description="Verifica se um access token ainda e valido.",
        tags=["auth"],
    ),
)
class VerifyView(TokenVerifyView):
    """View de verificacao de token."""


urlpatterns = [
    # Autenticacao JWT (views padrao do simplejwt)
    path("login/", LoginView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path("token/verify/", VerifyView.as_view(), name="token_verify"),
    # Registro e perfil
    path("register/", RegistroView.as_view(), name="register"),
    path("profile/", PerfilView.as_view(), name="profile"),
    path("change-password/", AlterarSenhaView.as_view(), name="change_password"),
]