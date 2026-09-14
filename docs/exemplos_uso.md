# Exemplos de Uso da API

Exemplos praticos de como interagir com a API usando **curl**.
Cada exemplo inclui o comando completo e a resposta esperada.

---

## Preparacao

Antes de testar, inicie o servidor:

```bash
python manage.py runserver
```

---

## 1. Registrar um Usuario

### Profissional

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"joao@email.com\", \"username\": \"joao@email.com\", \"password\": \"senha123\", \"password2\": \"senha123\", \"first_name\": \"Joao\", \"last_name\": \"Silva\", \"tipo_usuario\": \"profissional\"}"
```

**Resposta (201 Created):**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "joao@email.com",
  "username": "joao@email.com",
  "first_name": "Joao",
  "last_name": "Silva",
  "tipo_usuario": "profissional"
}
```

### Empresa

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"empresa@email.com\", \"username\": \"empresa@email.com\", \"password\": \"senha123\", \"password2\": \"senha123\", \"first_name\": \"Tech\", \"last_name\": \"Corp\", \"tipo_usuario\": \"empresa\"}"
```

---

## 2. Login e Obter Token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"joao@email.com\", \"password\": \"senha123\"}"
```

**Resposta (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

> **Importante:** Copie o `access` token para usar nas requisicoes autenticadas.
> Ele expira em 60 minutos.

---

## 3. Renovar Access Token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/refresh/ ^
  -H "Content-Type: application/json" ^
  -d "{\"refresh\": \"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...\"}"
```

**Resposta (200 OK):**

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## 4. Ver Perfil do Usuario

```bash
curl http://127.0.0.1:8000/api/v1/auth/profile/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>"
```

**Resposta (200 OK):**

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "joao@email.com",
  "username": "joao@email.com",
  "first_name": "Joao",
  "last_name": "Silva",
  "tipo_usuario": "profissional",
  "telefone": "",
  "bio": "",
  "endereco": "",
  "foto_perfil": null,
  "data_nascimento": null,
  "date_joined": "2026-01-15T10:30:00Z",
  "quantidade_servicos": 0
}
```

---

## 5. Atualizar Perfil

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/auth/profile/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"bio\": \"Desenvolvedor web com 3 anos de experiencia\", \"telefone\": \"(11) 99999-9999\", \"endereco\": \"Sao Paulo, SP\"}"
```

---

## 6. Alterar Senha

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/change-password/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"password_atual\": \"senha123\", \"nova_password\": \"novasenha456\", \"nova_password2\": \"novasenha456\"}"
```

---

## 7. Criar um Servico

```bash
curl -X POST http://127.0.0.1:8000/api/v1/servicos/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"titulo\": \"Desenvolvimento de site institucional\", \"descricao\": \"Crio sites modernos, responsivos e otimizados para SEO. Inclui ate 5 paginas, formulario de contato e hospedagem por 1 ano.\", \"categoria\": 1, \"preco\": 2500.00, \"tipo_preco\": \"fixo\", \"localizacao\": \"Sao Paulo, SP\"}"
```

**Resposta (201 Created):**

```json
{
  "id": "uuid-do-servico",
  "titulo": "Desenvolvimento de site institucional",
  "descricao": "Crio sites modernos, responsivos...",
  "categoria": 1,
  "categoria_nome": "Desenvolvimento Web",
  "preco": 2500.00,
  "preco_formatado": "R$ 2.500,00",
  "tipo_preco": "fixo",
  "localizacao": "Sao Paulo, SP",
  "ativo": true,
  "criado_em": "2026-01-15T10:30:00Z",
  "atualizado_em": "2026-01-15T10:30:00Z"
}
```

### Servico "a combinar"

```bash
curl -X POST http://127.0.0.1:8000/api/v1/servicos/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"titulo\": \"Consultoria em TI\", \"descricao\": \"Consultoria personalizada para sua empresa\", \"categoria\": 4, \"tipo_preco\": \"a_combinar\", \"localizacao\": \"Remoto\"}"
```

---

## 8. Listar Servicos

### Todos os servicos

```bash
curl http://127.0.0.1:8000/api/v1/servicos/
```

### Apenas os meus servicos

```bash
curl "http://127.0.0.1:8000/api/v1/servicos/?meus=true" ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>"
```

### Com filtros

```bash
# Buscar por palavra-chave
curl "http://127.0.0.1:8000/api/v1/servicos/?search=site"

# Filtrar por categoria
curl "http://127.0.0.1:8000/api/v1/servicos/?categoria=1"

# Filtrar por faixa de preco
curl "http://127.0.0.1:8000/api/v1/servicos/?preco_min=100&preco_max=5000"

# Filtrar por localizacao
curl "http://127.0.0.1:8000/api/v1/servicos/?localizacao=sao+paulo"

# Filtrar por tipo de preco
curl "http://127.0.0.1:8000/api/v1/servicos/?tipo_preco=fixo"

# Ordenar por preco (crescente)
curl "http://127.0.0.1:8000/api/v1/servicos/?ordering=preco"

# Ordenar por preco (decrescente)
curl "http://127.0.0.1:8000/api/v1/servicos/?ordering=-preco"

# Combinar filtros
curl "http://127.0.0.1:8000/api/v1/servicos/?search=design&tipo_preco=fixo&ordering=-preco"
```

### Paginacao

```bash
# Pagina 2 com 10 itens
curl "http://127.0.0.1:8000/api/v1/servicos/?page=2&page_size=10"
```

---

## 9. Detalhar um Servico

```bash
curl http://127.0.0.1:8000/api/v1/servicos/<UUID-DO-SERVICO>/
```

**Resposta (200 OK):**

```json
{
  "id": "uuid-do-servico",
  "titulo": "Desenvolvimento de site institucional",
  "descricao": "Crio sites modernos...",
  "categoria": 1,
  "categoria_nome": "Desenvolvimento Web",
  "preco": 2500.00,
  "preco_formatado": "R$ 2.500,00",
  "tipo_preco": "fixo",
  "localizacao": "Sao Paulo, SP",
  "ativo": true,
  "criado_em": "2026-01-15T10:30:00Z",
  "atualizado_em": "2026-01-15T10:30:00Z",
  "autor": {
    "id": "uuid-do-autor",
    "nome": "Joao Silva",
    "tipo_usuario": "profissional",
    "bio": "Desenvolvedor web...",
    "telefone": "(11) 99999-9999",
    "foto_perfil": null,
    "quantidade_servicos": 1
  }
}
```

---

## 10. Editar um Servico

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/servicos/<UUID-DO-SERVICO>/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>" ^
  -H "Content-Type: application/json" ^
  -d "{\"preco\": 3000.00, \"descricao\": \"Descricao atualizada com mais detalhes\"}"
```

---

## 11. Remover um Servico

```bash
curl -X DELETE http://127.0.0.1:8000/api/v1/servicos/<UUID-DO-SERVICO>/ ^
  -H "Authorization: Bearer <SEU_ACCESS_TOKEN>"
```

**Resposta:** `204 No Content` (sem corpo)

---

## 12. Listar Categorias

```bash
curl http://127.0.0.1:8000/api/v1/categorias/
```

**Resposta (200 OK):**

```json
{
  "count": 8,
  "total_pages": 1,
  "current_page": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "nome": "Desenvolvimento Web",
      "descricao": "Criacao de sites, sistemas web e e-commerces",
      "icone": "💻",
      "quantidade_servicos": 5
    },
    {
      "id": 2,
      "nome": "Design Grafico",
      "descricao": "Logotipos, identidade visual, banners e artes",
      "icone": "🎨",
      "quantidade_servicos": 3
    }
  ]
}
```

---

## 13. Erros Comuns

### Email ja em uso

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

### Senhas nao conferem

```json
{
  "erro": true,
  "status_code": 400,
  "mensagem": "Erro de validacao",
  "detalhes": {
    "password2": ["As senhas nao conferem."]
  }
}
```

### Nao autenticado

```json
{
  "detail": "Credenciais de autenticacao nao fornecidas."
}
```

### Nao autorizado (dono diferente)

```json
{
  "detail": "Voce nao tem permissao para executar esta acao."
}
```

### Preco obrigatorio quando tipo e "fixo"

```json
{
  "erro": true,
  "status_code": 400,
  "mensagem": "Erro de validacao",
  "detalhes": {
    "preco": ["Preco e obrigatorio quando o tipo e 'fixo'."]
  }
}
```

---

## Notas sobre o Linux/Mac

No Linux e Mac, os comandos curl usam `\` para continuacao de linha em vez de `^`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@email.com", "password": "senha123"}'
```

Note tambem que aspas simples `'` sao usadas no Linux para aspas externas.
