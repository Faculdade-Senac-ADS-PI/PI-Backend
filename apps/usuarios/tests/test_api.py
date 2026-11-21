"""
Testes de integracao da API de autenticacao e perfil.

Cobrem os casos de teste CT01, CT02 e as regras RN04/RN06 da documentacao.
Execute com: python manage.py test apps.usuarios
"""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

Usuario = get_user_model()

REGISTRO_URL = "/api/v1/auth/register/"
LOGIN_URL = "/api/v1/auth/login/"
REFRESH_URL = "/api/v1/auth/token/refresh/"
VERIFY_URL = "/api/v1/auth/token/verify/"
PERFIL_URL = "/api/v1/auth/profile/"
SENHA_URL = "/api/v1/auth/change-password/"

DADOS_VALIDOS = {
    "email": "maria@email.com",
    "username": "maria",
    "password": "Senha-Forte-2026",
    "password2": "Senha-Forte-2026",
    "first_name": "Maria",
    "last_name": "Souza",
    "tipo_usuario": "profissional",
}


class BaseAPITest(APITestCase):
    def setUp(self):
        # O throttling usa cache; limpa entre testes para evitar 429.
        cache.clear()


class RegistroLoginTests(BaseAPITest):
    def test_ct01_cadastro_valido_e_login_retorna_tokens(self):
        """CT01: cadastro valido cria conta e login devolve access/refresh."""
        resp = self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", resp.data)

        resp = self.client.post(
            LOGIN_URL,
            {"username": "maria", "password": "Senha-Forte-2026"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_ct02_email_duplicado_rejeitado(self):
        """CT02: e-mail ja cadastrado e rejeitado com mensagem."""
        self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        dados = {**DADOS_VALIDOS, "username": "outra"}
        resp = self.client.post(REGISTRO_URL, dados, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", str(resp.data))

    def test_ct02_username_duplicado_rejeitado(self):
        """CT02: username ja cadastrado e rejeitado com mensagem."""
        self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        dados = {**DADOS_VALIDOS, "email": "outra@email.com"}
        resp = self.client.post(REGISTRO_URL, dados, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", str(resp.data))

    def test_senhas_diferentes_rejeitadas(self):
        dados = {**DADOS_VALIDOS, "password2": "Outra-Senha-2026"}
        resp = self.client.post(REGISTRO_URL, dados, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rn06_senha_armazenada_com_hash(self):
        """RN06: a senha nunca e gravada em texto puro."""
        self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        usuario = Usuario.objects.get(username="maria")
        self.assertNotEqual(usuario.password, "Senha-Forte-2026")
        self.assertTrue(usuario.check_password("Senha-Forte-2026"))

    def test_login_com_senha_errada_retorna_401(self):
        self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        resp = self.client.post(
            LOGIN_URL, {"username": "maria", "password": "errada"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_e_verify_de_token(self):
        """UC03: renovar e verificar token JWT."""
        self.client.post(REGISTRO_URL, DADOS_VALIDOS, format="json")
        tokens = self.client.post(
            LOGIN_URL,
            {"username": "maria", "password": "Senha-Forte-2026"},
            format="json",
        ).data
        resp = self.client.post(VERIFY_URL, {"token": tokens["access"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.post(REFRESH_URL, {"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)


class PerfilTests(BaseAPITest):
    def setUp(self):
        super().setUp()
        self.usuario = Usuario.objects.create_user(
            username="joao", email="joao@email.com", password="Senha-Forte-2026"
        )

    def test_rn04_perfil_sem_token_retorna_401(self):
        """RN04: funcionalidades privadas exigem JWT valido."""
        resp = self.client.get(PERFIL_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_editar_perfil_autenticado(self):
        """UC08/UC09: ver e editar o proprio perfil."""
        self.client.force_authenticate(self.usuario)
        resp = self.client.patch(PERFIL_URL, {"telefone": "(85) 98888-7777"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["telefone"], "(85) 98888-7777")
        self.assertNotIn("password", resp.data)

    def test_email_do_perfil_e_somente_leitura(self):
        self.client.force_authenticate(self.usuario)
        self.client.patch(PERFIL_URL, {"email": "novo@email.com"}, format="json")
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.email, "joao@email.com")

    def test_alterar_senha_exige_senha_atual(self):
        """UC10: troca de senha so com a senha atual correta."""
        self.client.force_authenticate(self.usuario)
        resp = self.client.post(
            SENHA_URL,
            {
                "password_atual": "errada",
                "nova_password": "Nova-Senha-2026",
                "nova_password2": "Nova-Senha-2026",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        resp = self.client.post(
            SENHA_URL,
            {
                "password_atual": "Senha-Forte-2026",
                "nova_password": "Nova-Senha-2026",
                "nova_password2": "Nova-Senha-2026",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("Nova-Senha-2026"))
