"""
Serializers de servicos e categorias.

Serializadores responsaveis por:
    - Retornar dados de servicos e categorias
    - Validar dados de entrada para criacao/edicao
    - Formatar respostas da API
"""
from typing import Any, Dict, Optional

from rest_framework import serializers

from .models import Categoria, Servico


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura de categorias.

    Retorna os dados basicos de uma categoria.

    Campos retornados:
        - id, nome, descricao, icone
        - quantidade_servicos: total de servicos na categoria

    Exemplo de resposta:
        {
            "id": 1,
            "nome": "Desenvolvimento Web",
            "descricao": "Criacao de sites e sistemas web",
            "icone": "💻",
            "quantidade_servicos": 15
        }
    """

    quantidade_servicos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ["id", "nome", "descricao", "icone", "quantidade_servicos"]

    def get_quantidade_servicos(self, obj) -> int:
        """Conta quantos servicos ativos existem nesta categoria."""
        return obj.servicos.filter(ativo=True).count()


class ServicoListSerializer(serializers.ModelSerializer):
    """
    Serializer para listagem de servicos.

    Retorna os dados essenciais de um servico para listagens.
    Inclui informacoes resumidas do autor e categoria.

    Campos retornados:
        - id, titulo, descricao (resumida)
        - categoria (nome), preco, preco_formatado, tipo_preco
        - localizacao, ativo, criado_em
        - autor (nome, tipo_usuario, foto_perfil)

    Exemplo de resposta:
        {
            "id": "uuid-do-servico",
            "titulo": "Desenvolvimento de site",
            "descricao_resumida": "Crio sites modernos...",
            "categoria": "Desenvolvimento Web",
            "preco": 2500.00,
            "preco_formatado": "R$ 2.500,00",
            "tipo_preco": "fixo",
            "localizacao": "Sao Paulo, SP",
            "ativo": true,
            "criado_em": "2026-01-01T00:00:00Z",
            "autor": {
                "id": "uuid-do-autor",
                "nome": "Joao Silva",
                "tipo_usuario": "profissional",
                "foto_perfil": "/media/perfis/foto.jpg"
            }
        }
    """

    categoria = serializers.CharField(source="categoria.nome", read_only=True)
    autor = serializers.SerializerMethodField()
    preco_formatado = serializers.ReadOnlyField()

    class Meta:
        model = Servico
        fields = [
            "id",
            "titulo",
            "descricao",
            "categoria",
            "preco",
            "preco_formatado",
            "tipo_preco",
            "localizacao",
            "ativo",
            "criado_em",
            "autor",
        ]

    def get_autor(self, obj) -> Dict[str, Any]:
        """Retorna informacoes resumidas do autor do servico."""
        usuario = obj.usuario
        return {
            "id": str(usuario.id),
            "nome": usuario.get_full_name() or usuario.username,
            "tipo_usuario": usuario.tipo_usuario,
            "foto_perfil": (
                usuario.foto_perfil.url if usuario.foto_perfil else None
            ),
        }


class ServicoDetailSerializer(serializers.ModelSerializer):
    """
    Serializer para detalhes de um servico.

    Retorna todos os dados de um servico, incluindo informacoes
    completas do autor e da categoria.

    Usado nas endpoints de:
        - GET /api/v1/servicos/{id}/
        - PUT/PATCH /api/v1/servicos/{id}/

    Campos retornados:
        - Todos os campos do modelo
        - autor: informacoes completas do autor
        - categoria_nome: nome da categoria
    """

    autor = serializers.SerializerMethodField()
    categoria_nome = serializers.CharField(source="categoria.nome", read_only=True)
    preco_formatado = serializers.ReadOnlyField()

    class Meta:
        model = Servico
        fields = [
            "id",
            "titulo",
            "descricao",
            "categoria",
            "categoria_nome",
            "preco",
            "preco_formatado",
            "tipo_preco",
            "localizacao",
            "ativo",
            "criado_em",
            "atualizado_em",
            "autor",
        ]
        read_only_fields = ["id", "criado_em", "atualizado_em"]

    def get_autor(self, obj) -> Dict[str, Any]:
        """Retorna informacoes completas do autor do servico."""
        usuario = obj.usuario
        return {
            "id": str(usuario.id),
            "nome": usuario.get_full_name() or usuario.username,
            "tipo_usuario": usuario.tipo_usuario,
            "bio": usuario.bio,
            "telefone": usuario.telefone,
            "foto_perfil": (
                usuario.foto_perfil.url if usuario.foto_perfil else None
            ),
            "quantidade_servicos": usuario.quantidade_servicos,
        }


class ServicoCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para criacao e atualizacao de servicos.

    Usado apenas para escrita (POST, PUT, PATCH).
    O campo 'usuario' e definido automaticamente pelo viewset.

    Campos aceitos:
        - titulo: titulo do servico (obrigatorio)
        - descricao: descricao detalhada (obrigatorio)
        - categoria: ID da categoria (obrigatorio)
        - preco: valor do servico (opcional)
        - tipo_preco: 'fixo' ou 'a_combinar' (opcional, padrao: fixo)
        - localizacao: cidade/estado (opcional)
        - ativo: true/false (opcional, padrao: true)

    Exemplo de requisicao:
        POST /api/v1/servicos/
        {
            "titulo": "Desenvolvimento de site institucional",
            "descricao": "Crio sites modernos e responsivos...",
            "categoria": 1,
            "preco": 2500.00,
            "tipo_preco": "fixo",
            "localizacao": "Sao Paulo, SP"
        }
    """

    class Meta:
        model = Servico
        fields = [
            "titulo",
            "descricao",
            "categoria",
            "preco",
            "tipo_preco",
            "localizacao",
            "ativo",
        ]

    def validate_categoria(self, value):
        """Verifica se a categoria existe."""
        if not Categoria.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Categoria nao encontrada.")
        return value

    def validate(self, attrs):
        """Validacao cruzada entre preco e tipo_preco."""
        tipo_preco = attrs.get("tipo_preco", Servico.TipoPreco.FIXO)
        preco = attrs.get("preco")

        if tipo_preco == Servico.TipoPreco.FIXO and preco is None:
            raise serializers.ValidationError(
                {"preco": "Preco e obrigatorio quando o tipo e 'fixo'."}
            )
        if tipo_preco == Servico.TipoPreco.A_COMBINAR and preco is not None:
            raise serializers.ValidationError(
                {"preco": "Preco deve ser vazio quando o tipo e 'a combinar'."}
            )
        return attrs
