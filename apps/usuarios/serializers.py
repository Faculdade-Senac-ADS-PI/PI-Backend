"""
Serializers de autenticacao e perfil de usuario.

Serializadores responsaveis por:
    - Registrar novos usuarios
    - Exibir e atualizar o perfil do usuario
    - Validar dados de entrada

Importante: Senhas NUNCA sao retornadas nas respostas da API.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novos usuarios.

    Campos aceitos no POST:
        - email: email do usuario (obrigatorio, unico)
        - username: nome de usuario (obrigatorio, unico)
        - password: senha (obrigatoria, minimo 8 caracteres)
        - password2: confirmacao da senha (deve ser igual a password)
        - first_name: nome (obrigatorio)
        - last_name: sobrenome (obrigatorio)
        - tipo_usuario: 'profissional' ou 'empresa' (opcional, padrao: profissional)

    Campos retornados na resposta:
        - id, email, username, first_name, last_name, tipo_usuario

    Exemplo de requisicao:
        POST /api/v1/auth/register/
        {
            "email": "joao@email.com",
            "username": "joao@email.com",
            "password": "senha123",
            "password2": "senha123",
            "first_name": "Joao",
            "last_name": "Silva",
            "tipo_usuario": "profissional"
        }
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        validators=[validate_password],
        help_text="Senha do usuario (minimo 8 caracteres)",
    )
    password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Confirmacao da senha (deve ser igual a senha)",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "tipo_usuario",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        """Verifica se o email ja esta em uso."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ja esta em uso.")
        return value

    def validate_username(self, value):
        """Verifica se o username ja esta em uso."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nome de usuario ja esta em uso.")
        return value

    def validate(self, attrs):
        """Verifica se as senhas sao iguais."""
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "As senhas nao conferem."}
            )
        return attrs

    def create(self, validated_data):
        """
        Cria o usuario com a senha hasheada.

        Remove o campo password2 (confirmacao) antes de criar o usuario.
        Usa create_user() do Django para garantir o hash correto da senha.
        """
        # Remove a confirmacao de senha (nao e campo do modelo)
        validated_data.pop("password2")

        # Cria o usuario com create_user (hash automatico)
        usuario = User.objects.create_user(**validated_data)
        return usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura dos dados do usuario.

    Usado para retornar os dados do perfil do usuario nas respostas da API.
    NUNCA inclui dados sensiveis como senha ou tokens.

    Campos retornados:
        - id, email, username, first_name, last_name
        - tipo_usuario, telefone, bio, endereco
        - foto_perfil, data_nascimento
        - date_joined, quantidade_servicos

    Exemplo de resposta:
        {
            "id": "uuid-do-usuario",
            "email": "joao@email.com",
            "username": "joao@email.com",
            "first_name": "Joao",
            "last_name": "Silva",
            "tipo_usuario": "profissional",
            "telefone": "(11) 99999-9999",
            "bio": "Desenvolvedor web...",
            "endereco": "Sao Paulo, SP",
            "foto_perfil": "/media/perfis/foto.jpg",
            "data_nascimento": "1990-01-15",
            "date_joined": "2026-01-01T00:00:00Z",
            "quantidade_servicos": 5
        }
    """

    quantidade_servicos = serializers.SerializerMethodField()
    foto_perfil = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "tipo_usuario",
            "telefone",
            "bio",
            "endereco",
            "foto_perfil",
            "data_nascimento",
            "date_joined",
            "quantidade_servicos",
        ]
        read_only_fields = ["id", "email", "date_joined"]

    def get_quantidade_servicos(self, obj) -> int:
        return obj.quantidade_servicos


class AlterarSenhaSerializer(serializers.Serializer):
    """
    Serializer para alteracao de senha.

    Campos aceitos:
        - password_atual: senha atual (obrigatorio)
        - nova_password: nova senha (obrigatorio, minimo 8 caracteres)
        - nova_password2: confirmacao da nova senha

    Exemplo de requisicao:
        POST /api/v1/auth/change-password/
        {
            "password_atual": "senhaantiga",
            "nova_password": "novasenha123",
            "nova_password2": "novasenha123"
        }
    """

    password_atual = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Senha atual do usuario",
    )
    nova_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        validators=[validate_password],
        help_text="Nova senha (minimo 8 caracteres)",
    )
    nova_password2 = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        help_text="Confirmacao da nova senha",
    )

    def validate(self, attrs):
        """Verifica se as novas senhas conferem."""
        if attrs["nova_password"] != attrs["nova_password2"]:
            raise serializers.ValidationError(
                {"nova_password2": "As senhas nao conferem."}
            )
        return attrs

    def validate_password_atual(self, value):
        """Verifica se a senha atual esta correta."""
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value

    def save(self, **kwargs):
        """Salva a nova senha do usuario."""
        user = self.context["request"].user
        user.set_password(self.validated_data["nova_password"])
        user.save()
        return user
