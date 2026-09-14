# Plataforma de Servicos - API REST

Backend API para plataforma de divulgacao e venda de servicos, inspirada no GetNinjas e LinkedIn.

## Visao Geral

Esta API permite que **profissionais** e **empresas** publiquem seus servicos, enquanto **clientes** podem buscar, filtrar e encontram profissionais por area de atuacao.

---

## Funcionalidades do MVP

| Funcionalidade | Status | Descricao |
|---|---|---|
| Cadastro de usuarios | ✅ | Registro com email, tipos: profissional/empresa |
| Login JWT | ✅ | Autenticacao via tokens (access + refresh) |
| Perfil de usuario | ✅ | Visualizar e editar dados do perfil |
| Alteracao de senha | ✅ | Com verificacao da senha atual |
| CRUD de servicos | ✅ | Criar, listar, editar e remover servicos |
| Busca de servicos | ✅ | Por titulo, descricao, categoria e localizacao |
| Filtros avancados | ✅ | Por categoria, preco, tipo e autor |
| Categorias | ✅ | 8 categorias pre-cadastradas |
| Documentacao API | ✅ | Swagger UI e ReDoc interativos |
| Admin Django | ✅ | Painel para gerenciar dados |
| Testes | ✅ | 14 testes automatizados |

---

## Stack Tecnologica

| Componente | Tecnologia |
|---|---|
| Framework | Django 6.1 + Django REST Framework 3.18 |
| Banco de dados | PostgreSQL 16+ (desenvolvimento: SQLite) |
| Autenticacao | JWT via djangorestframework-simplejwt |
| Documentacao OpenAPI 3.x | drf-spectacular (Swagger + ReDoc) |
| Filtros | django-filter |
| CORS | django-cors-headers |
| Gerenciador de pacotes | UV (alternativa moderna ao pip) |
| Variaveis de ambiente | python-decouple |

---

## Estrutura do Projeto

```
projetointegrador2/
├── config/                        # Configuracoes do projeto
│   ├── settings/
│   │   ├── base.py               # Configs compartilhadas
│   │   ├── development.py        # Desenvolvimento (DEBUG=True)
│   │   └── production.py         # Producao (DEBUG=False, seguranca)
│   ├── urls.py                   # URLs raiz (admin, API, docs)
│   ├── wsgi.py                   # WSGI (Gunicorn)
│   └── asgi.py                   # ASGI (Daphne, WebSockets)
│
├── apps/                          # Aplicacoes do projeto
│   ├── usuarios/                  # Autenticacao e perfis
│   │   ├── models.py             # Modelo Custom User (email-based)
│   │   ├── serializers.py        # Registro, perfil, alterar senha
│   │   ├── views.py              # Registro, perfil, alterar senha
│   │   ├── urls.py               # Rotas de autenticacao JWT
│   │   ├── permissions.py        # (usado via core)
│   │   └── admin.py              # Painel admin de usuarios
│   │
│   ├── servicos/                  # Servicos e categorias
│   │   ├── models.py             # Modelo Servico e Categoria
│   │   ├── serializers.py        # Leitura, escrita, detalhes
│   │   ├── views.py              # ViewSet CRUD + busca
│   │   ├── filters.py            # Filtros django-filter
│   │   ├── urls.py               # Router (CRUD automatico)
│   │   └── admin.py              # Painel admin de servicos
│   │
│   └── core/                      # Utilidades compartilhadas
│       ├── pagination.py          # Paginacao padrao (20 itens)
│       ├── exceptions.py          # Handler de erros padronizado
│       └── permissions.py         # Permissoes reutilizaveis
│
├── fixtures/
│   └── categorias.json            # 8 categorias iniciais
│
├── docs/
│   ├── guia_setup.md              # Passo a passo de instalacao
│   ├── arquitetura.md             # Diagramas e estrutura
│   └── exemplos_uso.md            # Exemplos com curl/httpie
│
├── FUTURAS_INCREMENTACOES.md      # Roadmap de funcionalidades
├── README.md                      # Este arquivo
├── requirements.txt               # Dependencias com versoes
├── .env.example                   # Template de variaveis
├── .gitignore                     # Arquivos ignorados pelo git
└── manage.py                      # Comandos Django
```

---

## Endpoints da API

### Autenticacao

| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| `POST` | `/api/v1/auth/register/` | Registrar novo usuario | ❌ |
| `POST` | `/api/v1/auth/login/` | Login (retorna JWT) | ❌ |
| `POST` | `/api/v1/auth/token/refresh/` | Renovar access token | ❌ |
| `POST` | `/api/v1/auth/token/verify/` | Verificar se token e valido | ❌ |

### Perfil do Usuario

| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| `GET` | `/api/v1/auth/profile/` | Ver perfil do usuario logado | ✅ |
| `PATCH` | `/api/v1/auth/profile/` | Atualizar perfil do usuario | ✅ |
| `POST` | `/api/v1/auth/change-password/` | Alterar senha | ✅ |

### Servicos

| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| `GET` | `/api/v1/servicos/` | Listar servicos (com filtros) | ❌ |
| `POST` | `/api/v1/servicos/` | Criar novo servico | ✅ |
| `GET` | `/api/v1/servicos/{id}/` | Detalhar um servico | ❌ |
| `PUT/PATCH` | `/api/v1/servicos/{id}/` | Editar servico (dono) | ✅ |
| `DELETE` | `/api/v1/servicos/{id}/` | Remover servico (dono) | ✅ |

### Categorias

| Metodo | Endpoint | Descricao | Auth |
|--------|----------|-----------|------|
| `GET` | `/api/v1/categorias/` | Listar categorias | ❌ |
| `GET` | `/api/v1/categorias/{id}/` | Detalhar categoria | ❌ |

### Documentacao

| Endpoint | Descricao |
|----------|-----------|
| `/api/docs/` | Swagger UI (interativo) |
| `/api/redoc/` | ReDoc (leitura) |
| `/api/schema/` | Schema OpenAPI (YAML/JSON) |

---

## Quick Start (Resumo)

```bash
# 1. Clonar o repositorio
git clone <url-do-repositorio>
cd projetointegrador2

# 2. Criar ambiente virtual
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
uv pip install -r requirements.txt

# 4. Configurar variaveis de ambiente
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# 5. Aplicar migracoes
python manage.py migrate

# 6. Carregar categorias iniciais
python manage.py loaddata categorias

# 7. Criar usuario administrador
python manage.py createsuperuser

# 8. Iniciar servidor
python manage.py runserver
```

Para instrucoes detalhadas, veja [docs/guia_setup.md](docs/guia_setup.md).

---

## Documentacao da API

Apos iniciar o servidor, acesse:

- **Swagger UI** (recomendado): http://127.0.0.1:8000/api/docs/
  - Interativo - voce pode testar os endpoints direto no navegador
  - Botao "Authorize" para autenticar com JWT

- **ReDoc**: http://127.0.0.1:8000/api/redoc/
  - Visualizacao limpa e organizada para leitura

- **Schema OpenAPI**: http://127.0.0.1:8000/api/schema/
  - JSON ou YAML para gerar clientes automaticamente

---

## Como Contribuir

1. Faca um fork do repositorio
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Commit suas alteracoes (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

### Convencao de Commits

```
tipo(escopo): mensagem curta

Exemplos:
feat(servicos): adiciona filtros por preco
fix(auth): corrige validacao de email duplicado
docs(readme): atualiza instrucoes de setup
```

### Rodar os Testes

```bash
python manage.py test apps
```

### Verificar a Configuracao

```bash
python manage.py check
```

### Gerar schema da documentacao

```bash
python manage.py spectacular --validate --color --file schema.yml
```

---

## Equipe

Desenvolvido como projeto integrador.

---

## Licença

Projeto academico para fins de aprendizado.
