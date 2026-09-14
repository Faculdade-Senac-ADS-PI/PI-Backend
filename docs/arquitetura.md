# Arquitetura do Projeto

Documentacao tecnica sobre a estrutura, modelos, fluxos e decisoes de design do projeto.

---

## Visao Geral da Arquitetura

```
┌──────────────────────────────────────────────────────────┐
│                      CLIENTE                             │
│              (App mobile, Web frontend)                  │
│                   ou curl/Postman                        │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP/HTTPS
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    API REST                               │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │    Auth      │  │   Servicos   │  │   Categorias   │  │
│  │  (JWT)       │  │   (CRUD)     │  │   (Leitura)    │  │
│  └──────┬──────┘  └──────┬───────┘  └───────┬────────┘  │
│         │                │                  │            │
│  ┌──────┴────────────────┴──────────────────┴───────┐   │
│  │              DRF + SimpleJWT + Spectacular        │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                                │
│  ┌──────────────────────┴───────────────────────────┐   │
│  │                  Django ORM                       │   │
│  └──────────────────────┬───────────────────────────┘   │
└─────────────────────────┼────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   PostgreSQL / SQLite  │
              │       (banco)         │
              └───────────────────────┘
```

---

## Modelos de Dados

### Diagrama de Relacionamentos

```
┌─────────────────────┐       ┌─────────────────────────┐
│      Usuario        │       │        Servico           │
├─────────────────────┤       ├─────────────────────────┤
│ id (UUID, PK)       │◄──┐   │ id (UUID, PK)           │
│ email (unique)      │   │   │ titulo                  │
│ username            │   │   │ descricao               │
│ password            │   │   │ preco (nullable)        │
│ first_name          │   │   │ tipo_preco              │
│ last_name           │   │   │ localizacao             │
│ tipo_usuario        │   │   │ ativo (bool)            │
│ telefone            │   │   │ criado_em               │
│ bio                 │   │   │ atualizado_em           │
│ endereco            │   │   ├─────────────────────────┤
│ foto_perfil         │   │   │ usuario_id (FK) ────────┤──┐
│ data_nascimento     │   │   │ categoria_id (FK) ──────┤─┐│
│ date_joined         │   │   └─────────────────────────┘ ││
└─────────────────────┘   │                               ││
                          │   ┌─────────────────────────┐ ││
                          │   │      Categoria          │ ││
                          │   ├─────────────────────────┤ ││
                          │   │ id (int, PK)            │ ││
                          │   │ nome (unique)           │◄┘│
                          │   │ descricao               │  │
                          │   │ icone                   │  │
                          │   └─────────────────────────┘  │
                          │                                │
                          └────────────────────────────────┘
                          Relacao: 1:N (1 usuario -> N servicos)
```

### Modelo Usuario

Herda de `AbstractUser` do Django, adicionando campos para a plataforma.

**Caracteristicas:**
- Login por **email** (ao inves de username padrao)
- **UUID** como chave primaria (mais seguro que autoincrement)
- Dois tipos: `profissional` e `empresa`
- Propriedade `quantidade_servicos` (computada)

**Decisao de design:** Usar UUID ao inves de Integer ID evita enumeracao
de IDs por atacantes e facilita distribuicao em futuros microservicos.

### Modelo Servico

Representa um servico publicado por um usuario na plataforma.

**Campos:**
- `preco` e `nullable` (para servicos "a combinar")
- `ativo` permite desativar sem remover
- `auto_now_add` em `criado_em` e `auto_now` em `atualizado_em`
- Relacao CASCADE com Usuario (se remover usuario, remove servicos)
- Relacao PROTECT com Categoria (nao permite remover categoria com servicos)

### Modelo Categoria

Categorias sao gerenciadas pelo Django Admin, nao pela API.
A fixture `categorias.json` carrega 8 categorias iniciais.

---

## Fluxos Principais

### Fluxo 1: Cadastro e Login

```
┌─────────┐     POST /register/      ┌─────────┐
│ Cliente │ ──────────────────────── │  API    │
│         │  email, senha, dados     │         │
│         │ ◄────────────────────── │         │
│         │  { id, email, ... }      │         │
│         │                          │         │
│         │     POST /login/         │         │
│         │ ──────────────────────── │         │
│         │  email + password        │         │
│         │ ◄────────────────────── │         │
│         │  { access, refresh }     │         │
└─────────┘                          └─────────┘

tokens gerados:
  - access token:  60 minutos (curto, seguranca)
  - refresh token: 7 dias (longo, conveniencia)
```

### Fluxo 2: Criacao de Servico

```
┌─────────┐  POST /servicos/    ┌─────────┐     ┌─────────┐
│ Cliente │ ────────────────── │  API    │ ──  │  Banco  │
│         │  titulo, preco,    │         │     │         │
│         │  categoria, token  │         │     │         │
│         │ ◄───────────────── │         │ ◄── │         │
│         │  { servico criado }│         │     │         │
└─────────┘                    └─────────┘     └─────────┘

Permissoes:
  - Precisa estar autenticado (token JWT)
  - O campo usuario e definido automaticamente pelo servidor
```

### Fluxo 3: Busca com Filtros

```
┌─────────┐  GET /servicos/?search=web&categoria=1  ┌─────────┐
│ Cliente │ ─────────────────────────────────────── │  API    │
│         │ ◄───────────────────────────────────── │         │
│         │  { count, results: [...], ... }         │         │
└─────────┘                                        └─────────┘

Filtros disponiveis:
  - search: busca no titulo e descricao
  - categoria: ID da categoria
  - tipo_preco: "fixo" ou "a_combinar"
  - localizacao: busca por localizacao
  - preco_min / preco_max: faixa de preco
  - autor: UUID do autor
  - ordering: "preco", "-preco", "criado_em", "-criado_em"
  - meus: "true" (apenas servicos do usuario logado)
```

### Fluxo 4: Renovacao de Token

```
┌─────────┐  POST /token/refresh/   ┌─────────┐
│ Cliente │ ─────────────────────── │  API    │
│         │  { refresh: "..." }     │         │
│         │ ◄───────────────────── │         │
│         │  { access: "novo..." }  │         │
└─────────┘                         └─────────┘

Com ROTATE_REFRESH_TOKENS=True:
  - O refresh token antigo e invalidado
  - Um novo refresh token e emitido
  - Garante que cada refresh token e usado apenas 1x
```

---

## Estrutura de Configuracao

### Settings Split (base/dev/prod)

```
config/settings/
├── base.py          # Configs compartilhadas (INSTALLED_APPS, REST_FRAMEWORK, etc.)
├── development.py   # DEBUG=True, CORS aberto, SQLite/PostgreSQL, logs no console
└── production.py    # DEBUG=False, HTTPS, seguranca reforcada, logs em arquivo
```

**Como funciona:** `manage.py` carrega o modulo definido em `DJANGO_SETTINGS_MODULE`.
O arquivo `development.py` ou `production.py` importa tudo do `base.py` e sobrescreve
apenas o necessario.

### Autenticacao JWT

```
Login:
  POST /auth/login/ → { access, refresh }

Requisicoes autenticadas:
  GET /servicos/ -H "Authorization: Bearer <access_token>"

Refresh:
  POST /auth/token/refresh/ → { access }

Logout (revogacao):
  POST /auth/token/refresh/ com o token antigo (blacklist)
```

### Tratamento de Erros

Todas as respostas de erro seguem o formato padronizado:

```json
{
  "erro": true,
  "status_code": 400,
  "mensagem": "Erro de validacao",
  "detalhes": {
    "email": ["Este email ja esta em uso."]
  }
}
```

---

## Paginacao

Formato padrao das respostas de listagem:

```json
{
  "count": 100,
  "total_pages": 5,
  "current_page": 1,
  "next": "http://127.0.0.1:8000/api/v1/servicos/?page=2",
  "previous": null,
  "results": [...]
}
```

Parametros aceitos: `page` e `page_size` (maximo 100).

---

## Seguranca

| Aspecto | Implementacao |
|---|---|
| Senhas | Hashing automatico via Django (`create_user`) |
| JWT | Access token curto (60 min), refresh token rotativo |
| CORS | Origens especificas configuraveis |
| HTTPS | Obrigatorio em producao |
| Debug | False em producao |
| Secrets | Em variaveis de ambiente (.env), nunca no codigo |
| Throttling | 100 req/hora (anonimo), 1000 req/hora (autenticado) |
| Admin | Protegido por autenticacao Django |

---

## Decisoes de Design

### Por que UUID ao inves de Integer ID?
- Seguranca: impossivel enumerar IDs
- Privacidade: nao expoe a quantidade de registros
- Distribuicao: funcional em arquiteturas distribuidas

### Por que SQLite em dev e PostgreSQL em prod?
- SQLite: zero configuracao, funciona imediatamente
- PostgreSQL: prod-ready, suporta transacoes, concorrencia, JSON fields

### Por que drf-spectacular ao inves de drf-yasg?
- drf-spectacular: OpenAPI 3.x (padrao atual)
- drf-yasg: OpenAPI 2.0 (descontinuado)
- drf-spectacular: melhor inferencia de tipos, mais ativo

### Por que email-based login?
- Mais intuitivo que username para plataformas profissionais
- Padrao em apps modernos (LinkedIn, GetNinjas)
- email e unico por usuario, username e auxiliar
