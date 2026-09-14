"""
Configuracao do painel administrativo do Django.

O Django Admin permite gerenciar os dados pelo navegador em:
    http://127.0.0.1:8000/admin/

Para acessar, e necessario um usuario superuser:
    python manage.py createsuperuser
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Painel administrativo do modelo Usuario.

    Como o modelo usa login por email, o painel e configurado
    para exibir os campos relevantes do usuario.
    """

    # Campos exibidos na listagem de usuarios
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "tipo_usuario",
        "telefone",
        "is_active",
        "is_staff",
        "date_joined",
    )

    # Campos que podem ser usados na busca
    search_fields = ("email", "username", "first_name", "last_name", "telefone")

    # Filtros laterais
    list_filter = ("tipo_usuario", "is_active", "is_staff")

    # Ordenacao padrao
    ordering = ("-date_joined",)

    # Campos editaveis diretamente na listagem
    list_editable = ("is_active",)

    # Agrupa os campos de perfil na edicao do usuario
    fieldsets = UserAdmin.fieldsets + (
        ("Dados de Perfil", {
            "fields": ("tipo_usuario", "telefone", "bio", "endereco", "foto_perfil", "data_nascimento"),
        }),
    )

    # Campos exibidos ao criar novo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Dados de Perfil", {
            "fields": ("tipo_usuario",),
        }),
    )