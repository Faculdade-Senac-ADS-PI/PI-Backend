# Guia de Setup - Plataforma de Servicos

Guia passo a passo para configurar o ambiente de desenvolvimento.

---

## Pre-requisitos

### Software Necessario

| Software | Versao Minima | Como verificar |
|---|---|---|
| Python | 3.10+ | `python --version` |
| UV | 0.10+ | `uv --version` |
| Git | 2.0+ | `git --version` |
| PostgreSQL | 15+ (opcional) | `psql --version` |

### Instalacao do UV

O [UV](https://docs.astral.sh/uv/) e um gerenciador de pacotes Python rapido (alternativa moderna ao pip).

```bash
# Windows (via PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalacao
uv --version
```

### Instalacao do PostgreSQL

> **Nota:** O projeto funciona com SQLite para desenvolvimento local.
> PostgreSQL e necessario apenas para producao.

```bash
# Windows: Baixe em https://www.postgresql.org/download/windows/
# Durante a instalacao, defina a senha do usuario 'postgres'

# Linux (Ubuntu/Debian):
sudo apt install postgresql postgresql-client

# Verificar se esta rodando:
sudo systemctl status postgresql
```

---

## Instalacao do Projeto

### Passo 1: Clonar o repositorio

```bash
git clone <url-do-repositorio>
cd projetointegrador2
```

### Passo 2: Criar ambiente virtual

```bash
# Criar o ambiente virtual com UV
uv venv

# Ativar o ambiente virtual
# Windows (CMD):
.venv\Scripts\activate

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Linux/Mac:
source .venv/bin/activate
```

**Como funciona:** O ambiente virtual cria uma pasta `.venv` que isola as dependencias
do projeto das outras instalacoes de Python no seu computador. Isso evita conflitos
de versoes entre projetos.

### Passo 3: Instalar dependencias

```bash
# Instala todos os pacotes listados no requirements.txt
uv pip install -r requirements.txt
```

**O que sao os pacotes instalados:**

| Pacote | O que faz |
|---|---|
| `django` | Framework web Python |
| `djangorestframework` | Toolkit para criar APIs REST |
| `djangorestframework-simplejwt` | Autenticacao JWT |
| `django-cors-headers` | Controle de acesso cross-origin |
| `django-filter` | Filtros avancados para buscas |
| `drf-spectacular` | Geracao de documentacao Swagger |
| `python-decouple` | Gerenciamento de variaveis de ambiente |
| `psycopg2-binary` | Conexao com PostgreSQL |
| `Pillow` | Manipulacao de imagens |

### Passo 4: Configurar variaveis de ambiente

```bash
# Copie o modelo para o arquivo .env
# Windows:
copy .env.example .env

# Linux/Mac:
cp .env.example .env
```

Abra o arquivo `.env` e edite os valores conforme necessario:

```env
# Chave secreta do Django (gere uma nova em producao!)
SECRET_KEY=django-insecure-sua-chave-aqui

# Configuracoes do banco de dados
DB_NAME=plataforma_servicos
DB_USER=postgres
DB_PASSWORD=sua_senha_postgresql
DB_HOST=localhost
DB_PORT=5432
```

### Passo 5: Configurar o banco de dados

#### Opcao A: SQLite (padrao - recomendado para comecar)

Nenhuma configuracao adicional necessaria. O banco sera criado automaticamente.

#### Opcao B: PostgreSQL

1. Crie o banco de dados:

```bash
# Conectar ao PostgreSQL (vai pedir a senha)
psql -U postgres

# Dentro do psql, execute:
CREATE DATABASE plataforma_servicos;

# Sair do psql:
\q
```

2. Edite o `.env` e adicione:

```env
DB_ENGINE=postgresql
DB_NAME=plataforma_servicos
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### Passo 6: Aplicar migracoes

```bash
python manage.py migrate
```

**O que sao migracoes?** Migracoes sao arquivos que dizem ao Django como criar
e atualizar as tabelas do banco de dados. O comando `migrate` aplica todas
as migracoes pendentes, criando as tabelas necessarias.

### Passo 7: Carregar dados iniciais

```bash
python manage.py loaddata categorias
```

Isso carrega 8 categorias de servicos: Desenvolvimento Web, Design Grafico,
Marketing Digital, Consultoria, Aulas, Manutencao, Saude e Fotografia.

### Passo 8: Criar usuario administrador

```bash
python manage.py createsuperuser
```

Siga as instrucoes no terminal para definir email, username e senha.
Esse usuario tera acesso ao painel administrativo em `/admin/`.

### Passo 9: Iniciar o servidor

```bash
python manage.py runserver
```

O servidor iniciara em http://127.0.0.1:8000/

---

## Verificando a Instalacao

Apos iniciar o servidor, acesse os seguintes links:

| URL | Descricao |
|---|---|
| http://127.0.0.1:8000/admin/ | Painel administrativo (login com superuser) |
| http://127.0.0.1:8000/api/docs/ | Swagger UI - documentacao interativa |
| http://127.0.0.1:8000/api/redoc/ | ReDoc - documentacao para leitura |
| http://127.0.0.1:8000/api/v1/auth/login/ | Endpoint de login JWT |

---

## Testando a API

### 1. Registrar um usuario

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "username": "teste@email.com",
    "password": "senha-segura-123",
    "password2": "senha-segura-123",
    "first_name": "Maria",
    "last_name": "Silva",
    "tipo_usuario": "profissional"
  }'
```

### 2. Fazer login e obter token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teste@email.com",
    "password": "senha-segura-123"
  }'
```

A resposta contera `access` e `refresh` tokens. Copie o `access` token.

### 3. Criar um servico (com token)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/servicos/ \
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Desenvolvimento de site",
    "descricao": "Crio sites modernos e responsivos",
    "categoria": 1,
    "preco": 2500.00,
    "tipo_preco": "fixo",
    "localizacao": "Sao Paulo, SP"
  }'
```

---

## Solucao de Problemas

### Erro: "ModuleNotFoundError: No module named 'django'"

```bash
# Certifique-se de que o ambiente virtual esta ativado
# Windows:
.venv\Scripts\activate

# Linux/Mac:
source .venv/bin/activate

# Reinstale as dependencias
uv pip install -r requirements.txt
```

### Erro: "OperationalError: no such table"

```bash
# Aplique as migracoes
python manage.py migrate
```

### Erro: "IntegrityError: UNIQUE constraint failed"

O email ou username ja esta em uso. Use um email diferente.

### Erro: "PermissionDenied" em endpoints protegidos

Certifique-se de de enviar o header `Authorization: Bearer <token>`.

---

## Variaveis de Ambiente

Referencia completa das variaveis do `.env`:

| Variavel | Padrao | Descricao |
|---|---|---|
| `SECRET_KEY` | (obrigatoria) | Chave secreta do Django |
| `DJANGO_SETTINGS_MODULE` | `config.settings.development` | Modulo de settings |
| `DB_ENGINE` | `sqlite` | Engine do banco (sqlite ou postgresql) |
| `DB_NAME` | `plataforma_servicos` | Nome do banco PostgreSQL |
| `DB_USER` | `postgres` | Usuario do PostgreSQL |
| `DB_PASSWORD` | `postgres` | Senha do PostgreSQL |
| `DB_HOST` | `localhost` | Host do PostgreSQL |
| `DB_PORT` | `5432` | Porta do PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | Origens permitidas (frontend) |
