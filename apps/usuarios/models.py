"""
Modelo de Usuario customizado.

Define o modelo de usuario do projeto, estendendo o AbstractUser
do Django para suportar campos adicionais necessarios para a
plataforma de servicos.

Caracteristicas:
    - Login por email (ao inves de username)
    - Tipos de usuario: profissional e empresa
    - Campos de perfil: telefone, bio, endereco, foto
"""
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario customizado para a plataforma.

    Estende o AbstractUser do Django adicionando campos especificos
    para uma plataforma de divulgacao e venda de servicos.

    Campos herdados do AbstractUser:
        - username, password, first_name, last_name, email
        - is_active, is_staff, is_superuser
        - date_joined, last_login

    Campos adicionados:
        - id: UUID unico para cada usuario
        - tipo_usuario: 'profissional' ou 'empresa'
        - telefone: numero de contato
        - bio: biografia ou descricao profissional
        - endereco: cidade/estado onde atua
        - foto_perfil: foto do usuario
        - data_nascimento: data de nascimento (opcional)

    Exemplo de uso:
        # Criando um usuario
        usuario = Usuario.objects.create_user(
            username="joao@email.com",
            email="joao@email.com",
            password="senha123",
            tipo_usuario="profissional",
            first_name="Joao",
            last_name="Silva",
        )
    """

    class TipoUsuario(models.TextChoices):
        """Opcoes de tipo de usuario."""
        PROFISSIONAL = "profissional", "Profissional"
        EMPRESA = "empresa", "Empresa"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador unico do usuario (UUID)",
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.PROFISSIONAL,
        help_text="Tipo de usuario: profissional ou empresa",
        verbose_name="Tipo de Usuario",
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
        default="",
        help_text="Numero de telefone para contato",
        verbose_name="Telefone",
    )

    bio = models.TextField(
        blank=True,
        default="",
        help_text="Biografia ou descricao profissional do usuario",
        verbose_name="Biografia",
    )

    endereco = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Cidade e estado onde o usuario atua",
        verbose_name="Endereco",
    )

    foto_perfil = models.ImageField(
        upload_to="perfis/",
        blank=True,
        null=True,
        help_text="Foto de perfil do usuario",
        verbose_name="Foto de Perfil",
    )

    data_nascimento = models.DateField(
        blank=True,
        null=True,
        help_text="Data de nascimento do usuario",
        verbose_name="Data de Nascimento",
    )

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["-date_joined"]

    def __str__(self):
        """Retorna o nome completo ou email do usuario."""
        nome_completo = self.get_full_name()
        return nome_completo if nome_completo else self.email

    @property
    def quantidade_servicos(self):
        """Retorna o numero de servicos publicados pelo usuario."""
        return self.servicos.filter(ativo=True).count()
