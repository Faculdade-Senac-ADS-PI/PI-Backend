"""
Testes dos modelos Servico e Categoria.

Cobre a criacao de servicos, categorias e relacoes.
Execute com: python manage.py test apps.servicos
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Categoria, Servico

Usuario = get_user_model()


class CategoriaModelTests(TestCase):
    """Testes do modelo Categoria."""

    def setUp(self):
        """Cria uma categoria de teste."""
        self.categoria = Categoria.objects.create(
            nome="Desenvolvimento Web",
            descricao="Criacao de sites e sistemas",
            icone="💻",
        )

    def test_categoria_criada(self):
        """Verifica se a categoria foi criada."""
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(self.categoria.nome, "Desenvolvimento Web")

    def test_categoria_nome_unico(self):
        """Verifica que nome de categoria e unico."""
        with self.assertRaises(Exception):
            Categoria.objects.create(nome="Desenvolvimento Web")


class ServicoModelTests(TestCase):
    """Testes do modelo Servico."""

    def setUp(self):
        """Cria usuario e categoria para os testes."""
        self.usuario = Usuario.objects.create_user(
            username="joao.silva",
            email="joao@email.com",
            password="senha-segura-123",
            first_name="Joao",
            last_name="Silva",
        )
        self.categoria = Categoria.objects.create(
            nome="Desenvolvimento Web",
            descricao="Criacao de sites e sistemas",
        )
        self.servico = Servico.objects.create(
            usuario=self.usuario,
            titulo="Criacao de site institucional",
            descricao="Desenvolvimento de site responsivo",
            categoria=self.categoria,
            preco=2500.00,
            tipo_preco="fixo",
            localizacao="Sao Paulo, SP",
        )

    def test_servico_criado(self):
        """Verifica se o servico foi criado com os dados corretos."""
        self.assertEqual(Servico.objects.count(), 1)
        self.assertEqual(self.servico.usuario, self.usuario)
        self.assertEqual(self.servico.categoria, self.categoria)
        self.assertEqual(self.servico.titulo, "Criacao de site institucional")

    def test_servico_vinculado_ao_usuario(self):
        """Verifica a relacao reversa Usuario -> servicos."""
        servicos_do_usuario = self.usuario.servicos.all()
        self.assertEqual(servicos_do_usuario.count(), 1)

    def test_preco_formatado(self):
        """Verifica a formatacao do preco."""
        self.assertEqual(self.servico.preco_formatado, "R$ 2.500,00")

    def test_preco_a_combinar(self):
        """Verifica o preco formatado quando nao ha preco."""
        servico = Servico.objects.create(
            usuario=self.usuario,
            titulo="Consultoria",
            descricao="Hora de consultoria",
            categoria=self.categoria,
            preco=None,
            tipo_preco="a_combinar",
        )
        self.assertEqual(servico.preco_formatado, "A combinar")

    def test_quantidade_servicos_property(self):
        """Verifica a propriedade quantidade_servicos."""
        self.assertEqual(self.usuario.quantidade_servicos, 1)

    def test_delecao_usuario_remove_servicos(self):
        """Verifica que remover o usuario remove seus servicos (CASCADE)."""
        self.usuario.delete()
        self.assertEqual(Servico.objects.count(), 0)