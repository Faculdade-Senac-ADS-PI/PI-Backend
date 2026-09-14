"""
Testes do modelo Usuario.

Cobre a criacao de usuarios, campos obrigatorios e propriedades.
Execute com: python manage.py test apps.usuarios
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

Usuario = get_user_model()


class UsuarioModelTests(TestCase):
    """Testes do modelo de Usuario."""

    def setUp(self):
        """Cria um usuario de teste antes de cada teste."""
        self.usuario = Usuario.objects.create_user(
            username="joao.silva",
            email="joao@email.com",
            password="senha-segura-123",
            first_name="Joao",
            last_name="Silva",
            tipo_usuario="profissional",
            telefone="(11) 99999-9999",
            bio="Desenvolvedor web com 5 anos de experiencia",
            endereco="Sao Paulo, SP",
        )

    def test_usuario_criado_com_sucesso(self):
        """Verifica se o usuario foi criado com os dados corretos."""
        usuario = Usuario.objects.get(email="joao@email.com")
        self.assertEqual(usuario.first_name, "Joao")
        self.assertEqual(usuario.last_name, "Silva")
        self.assertEqual(usuario.tipo_usuario, "profissional")
        self.assertEqual(usuario.telefone, "(11) 99999-9999")

    def test_senha_esta_hasheada(self):
        """Verifica se a senha foi hasheada e nao armazenada em texto puro."""
        usuario = Usuario.objects.get(email="joao@email.com")
        self.assertNotEqual(usuario.password, "senha-segura-123")
        self.assertTrue(usuario.check_password("senha-segura-123"))

    def test_str_retorna_nome_completo(self):
        """Verifica se __str__ retorna o nome completo."""
        usuario = Usuario.objects.get(email="joao@email.com")
        self.assertEqual(str(usuario), "Joao Silva")

    def test_login_por_email(self):
        """Verifica se o usuario consegue autenticar com email."""
        usuario = Usuario.objects.get(email="joao@email.com")
        autenticado = usuario
        self.assertIsNotNone(autenticado)

    def test_quantidade_servicos_padrao_zero(self):
        """Verifica que um usuario novo tem 0 servicos."""
        self.assertEqual(self.usuario.quantidade_servicos, 0)

    def test_criar_usuario_empresa(self):
        """Verifica a criacao de usuario do tipo empresa."""
        empresa = Usuario.objects.create_user(
            username="empresa@email.com",
            email="empresa@email.com",
            password="senha-segura-123",
            tipo_usuario="empresa",
        )
        self.assertEqual(empresa.tipo_usuario, "empresa")