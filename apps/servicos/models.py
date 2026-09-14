"""
Modelos de Servico e Categoria.

Define os modelos para o catalogo de servicos da plataforma.
Cada usuario pode publicar multiplos servicos em diferentes categorias.
"""
import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Categoria(models.Model):
    """
    Categoria de servicos.

    Agrupa servicos por area de atuacao, facilitando a busca
    e navegacao dos usuarios.

    Exemplos de categorias:
        - Desenvolvimento Web
        - Design Grafico
        - Marketing Digital
        - Consultoria

    Exemplo de uso:
        categoria = Categoria.objects.create(
            nome="Desenvolvimento Web",
            descricao="Criacao de sites e sistemas web",
            icone="💻"
        )
    """

    nome = models.CharField(
        max_length=100,
        unique=True,
        help_text="Nome unico da categoria",
        verbose_name="Nome",
    )

    descricao = models.TextField(
        blank=True,
        default="",
        help_text="Descricao da categoria",
        verbose_name="Descricao",
    )

    icone = models.CharField(
        max_length=10,
        blank=True,
        default="",
        help_text="Emoji ou icone representativo da categoria",
        verbose_name="Icone",
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["nome"]

    def __str__(self):
        """Retorna o nome da categoria."""
        return self.nome


class Servico(models.Model):
    """
    Modelo de servico publicado na plataforma.

    Cada servico esta associado a um usuario (autor) e a uma categoria.
    O servico contem informacoes sobre o servico oferecido, preco
    e localizacao.

    Campos principais:
        - titulo: nome do servico
        - descricao: detalhes sobre o servico
        - categoria: area de atuacao
        - preco: valor do servico (null = a combinar)
        - localizacao: onde o servico e oferecido

    Exemplo de uso:
        servico = Servico.objects.create(
            usuario=usuario,
            titulo="Desenvolvimento de site institucional",
            descricao="Crio sites modernos e responsivos...",
            categoria=categoria_web,
            preco=2500.00,
            tipo_preco="fixo",
            localizacao="Sao Paulo, SP",
        )
    """

    class TipoPreco(models.TextChoices):
        """Opcoes de tipo de preco."""
        FIXO = "fixo", "Preco Fixo"
        A_COMBINAR = "a_combinar", "A Combinar"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identificador unico do servico (UUID)",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="servicos",
        help_text="Usuario que publicou o servico",
        verbose_name="Autor",
    )

    titulo = models.CharField(
        max_length=200,
        help_text="Titulo descritivo do servico",
        verbose_name="Titulo",
    )

    descricao = models.TextField(
        help_text="Descricao detalhada do servico oferecido",
        verbose_name="Descricao",
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="servicos",
        help_text="Categoria do servico",
        verbose_name="Categoria",
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Preco do servico (deixe vazio para 'A Combinar')",
        verbose_name="Preco",
    )

    tipo_preco = models.CharField(
        max_length=20,
        choices=TipoPreco.choices,
        default=TipoPreco.FIXO,
        help_text="Tipo do preco: fixo ou a combinar",
        verbose_name="Tipo de Preco",
    )

    localizacao = models.CharField(
        max_length=200,
        blank=True,
        default="",
        help_text="Cidade e estado onde o servico e oferecido",
        verbose_name="Localizacao",
    )

    ativo = models.BooleanField(
        default=True,
        help_text="Se o servico esta disponivel para contratacao",
        verbose_name="Ativo",
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e hora de criacao do servico",
        verbose_name="Criado em",
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        help_text="Data e hora da ultima atualizacao",
        verbose_name="Atualizado em",
    )

    class Meta:
        verbose_name = "Servico"
        verbose_name_plural = "Servicos"
        ordering = ["-criado_em"]

    def __str__(self):
        """Retorna o titulo do servico."""
        return self.titulo

    @property
    def preco_formatado(self):
        """Retorna o preco formatado como moeda brasileira."""
        if self.preco is None:
            return "A combinar"
        return f"R$ {self.preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
