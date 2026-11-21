"""
Testes de integracao da API de servicos e categorias.

Cobrem os casos de teste CT03 e CT04 da documentacao.
Execute com: python manage.py test apps.servicos
"""
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APITestCase

from apps.servicos.models import Categoria, Servico

Usuario = get_user_model()

SERVICOS_URL = "/api/v1/servicos/"
CATEGORIAS_URL = "/api/v1/categorias/"


class ServicoAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.dono = Usuario.objects.create_user(
            username="dono", email="dono@email.com", password="Senha-Forte-2026"
        )
        self.outro = Usuario.objects.create_user(
            username="outro", email="outro@email.com", password="Senha-Forte-2026"
        )
        self.eletrica = Categoria.objects.create(nome="Eletricista")
        self.pintura = Categoria.objects.create(nome="Pintor")
        self.servico = Servico.objects.create(
            usuario=self.dono,
            titulo="Instalacao de tomadas",
            descricao="Instalacao e troca de tomadas residenciais",
            categoria=self.eletrica,
            preco=120,
            localizacao="Fortaleza, CE",
        )
        Servico.objects.create(
            usuario=self.dono,
            titulo="Pintura de apartamento",
            descricao="Pintura interna completa",
            categoria=self.pintura,
            preco=1500,
            localizacao="Caucaia, CE",
        )
        Servico.objects.create(
            usuario=self.dono,
            titulo="Servico inativo",
            descricao="Nao deve aparecer na busca publica",
            categoria=self.eletrica,
            preco=50,
            localizacao="Fortaleza, CE",
            ativo=False,
        )

    def _titulos(self, resp):
        dados = resp.data.get("results", resp.data)
        return {item["titulo"] for item in dados}

    def test_listar_servicos_sem_token_retorna_401(self):
        """RN04 / analise 7.3: listar servicos exige JWT."""
        resp = self.client.get(SERVICOS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ct03_listagem_exibe_somente_ativos(self):
        """CT03 / RN14: servicos inativos nao aparecem na listagem."""
        self.client.force_authenticate(self.outro)
        resp = self.client.get(SERVICOS_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertNotIn("Servico inativo", self._titulos(resp))
        self.assertEqual(len(self._titulos(resp)), 2)

    def test_ct03_filtro_por_categoria(self):
        self.client.force_authenticate(self.outro)
        resp = self.client.get(SERVICOS_URL, {"categoria": self.pintura.id})
        self.assertEqual(self._titulos(resp), {"Pintura de apartamento"})

    def test_ct03_filtro_por_faixa_de_preco(self):
        self.client.force_authenticate(self.outro)
        resp = self.client.get(SERVICOS_URL, {"preco_min": 100, "preco_max": 200})
        self.assertEqual(self._titulos(resp), {"Instalacao de tomadas"})

    def test_ct03_filtro_por_localizacao(self):
        self.client.force_authenticate(self.outro)
        resp = self.client.get(SERVICOS_URL, {"localizacao": "Caucaia"})
        self.assertEqual(self._titulos(resp), {"Pintura de apartamento"})

    def test_busca_textual(self):
        """UC04: busca por titulo e descricao."""
        self.client.force_authenticate(self.outro)
        resp = self.client.get(SERVICOS_URL, {"search": "tomadas"})
        self.assertEqual(self._titulos(resp), {"Instalacao de tomadas"})

    def test_publicar_servico_vincula_ao_usuario_logado(self):
        """UC11: o servico criado pertence ao usuario autenticado."""
        self.client.force_authenticate(self.outro)
        resp = self.client.post(
            SERVICOS_URL,
            {
                "titulo": "Faxina residencial",
                "descricao": "Limpeza completa",
                "categoria": self.eletrica.id,
                "preco": "150.00",
                "tipo_preco": "fixo",
                "localizacao": "Fortaleza, CE",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        criado = Servico.objects.get(titulo="Faxina residencial")
        self.assertEqual(criado.usuario, self.outro)

    def test_preco_negativo_rejeitado(self):
        self.client.force_authenticate(self.outro)
        resp = self.client.post(
            SERVICOS_URL,
            {
                "titulo": "Preco invalido",
                "descricao": "x",
                "categoria": self.eletrica.id,
                "preco": "-10.00",
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ct04_editar_servico_de_outro_usuario_retorna_403(self):
        """CT04: edicao bloqueada por EhDonoOuLeitura."""
        self.client.force_authenticate(self.outro)
        resp = self.client.patch(
            f"{SERVICOS_URL}{self.servico.id}/", {"titulo": "Invadido"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_ct04_excluir_servico_de_outro_usuario_retorna_403(self):
        """CT04: exclusao bloqueada por EhDonoOuLeitura."""
        self.client.force_authenticate(self.outro)
        resp = self.client.delete(f"{SERVICOS_URL}{self.servico.id}/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Servico.objects.filter(id=self.servico.id).exists())

    def test_dono_pode_editar_proprio_servico(self):
        """UC12: o dono edita o proprio servico."""
        self.client.force_authenticate(self.dono)
        resp = self.client.patch(
            f"{SERVICOS_URL}{self.servico.id}/", {"preco": "130.00"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_meus_servicos_inclui_inativos(self):
        """UC14: meus=true lista tambem os inativos do dono."""
        self.client.force_authenticate(self.dono)
        resp = self.client.get(SERVICOS_URL, {"meus": "true"})
        self.assertIn("Servico inativo", self._titulos(resp))


class CategoriaAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        Categoria.objects.create(nome="Diarista")

    def test_categorias_sao_publicas(self):
        """UC07: visitante consulta categorias sem token."""
        resp = self.client.get(CATEGORIAS_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)

    def test_categorias_sao_somente_leitura(self):
        resp = self.client.post(CATEGORIAS_URL, {"nome": "Nova"}, format="json")
        self.assertIn(
            resp.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED),
        )
