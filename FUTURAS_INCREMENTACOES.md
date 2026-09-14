# Futuras Incrementacoes

Roadmap de funcionalidades planejadas para evoluir a plataforma.
Cada incrementacao esta organizada por prioridade e complexidade.

---

## Como Ler Este Documento

| Nivel | Descricao |
|---|---|
| **🟢 Facil** | Pode ser implementado em 1-2 dias |
| **🟡 Medio** | Requer 3-5 dias de desenvolvimento |
| **🔴 Dificil** | Requer 1-2 semanas ou mais |
| **⚪ Complexo** | Requer infraestrutura adicional ou dependencias externas |

---

## Fase 1 - Engajamento e Interacao

### Avaliacoes e Notas dos Profissionais

**Nivel:** 🟡 Medio | **Prioridade:** Alta

```
Modelo sugerido:
- avaliacao (1-5 estrelas)
- comentario (texto)
- autor (usuario que avaliou)
- servico ou usuario avaliado
- data_da_avaliacao

Endpoints:
  POST   /api/v1/avaliacoes/           -> Criar avaliacao
  GET    /api/v1/avaliacoes/?servico=X -> Listar avaliacoes
  DELETE /api/v1/avaliacoes/{id}/       -> Remover (autor)
```

**Por que e importante:**
- Gera confianca entre usuarios
- Ajuda na decisao de contratacao
- Ranking natural de profissionais

---

### Mensagens entre Usuarios

**Nivel:** 🔴 Dificil | **Prioridade:** Alta

```
Modelo sugerido:
- remetente (usuario que envia)
- destinatario (usuario que recebe)
- texto (conteudo da mensagem)
- lida (boolean)
- data_envio

Endpoints:
  GET    /api/v1/conversas/                  -> Listar conversas
  GET    /api/v1/conversas/{id}/mensagens/   -> Mensagens da conversa
  POST   /api/v1/conversas/{id}/mensagens/   -> Enviar mensagem
  PATCH  /api/v1/conversas/{id}/             -> Marcar como lida
```

**Destaques tecnicos:**
- WebSockets em tempo real (Django Channels + Redis)
- ou polling simples com HTTP para MVP

---

### Sistema de Solicitacoes/Propostas

**Nivel:** 🔴 Dificil | **Prioridade:** Alta

```
Fluxo:
  1. Cliente envia solicitacao para profissional
  2. Profissional envia proposta (preco, prazo)
  3. Cliente aceita ou recusa
  4. Servico inicia quando aceito

Modelo:
- solicitacao: cliente, profissional, servico, mensagem
- proposta: solicitacao, preco, prazo, mensagem
- status: pendente/aceita/recusa/concluida
```

---

## Fase 2 - Descoberta e Visibilidade

### Sistema de Favoritos

**Nivel:** 🟢 Facil | **Prioridade:** Media

```
Modelo:
- usuario (que favoritou)
- servico (favoritado)

Endpoints:
  POST   /api/v1/favoritos/           -> Adicionar
  DELETE /api/v1/favoritos/{id}/      -> Remover
  GET    /api/v1/favoritos/           -> Listar meus favoritos
```

---

### Visao Geral do Servico (Estatisticas)

**Nivel:** 🟡 Medio | **Prioridade:** Media

```
Dados a retornar:
- Total de visualizacoes do servico
- Total de solicitacoes recebidas
- Avaliacao media
- Tempo medio de resposta
- Taxa de conversao

Endpoints:
  GET /api/v1/servicos/{id}/estatisticas/  -> Estatisticas
```

---

### Busca Avancada com IA

**Nivel:** 🔴 Dificil | **Prioridade:** Baixa

```
Funcionalidades:
- Busca por similaridade semantica
- Sugerir profissionais baseado no historico
- Classificar resultados por relevancia
- Auto-complete inteligente

Tecnologias:
- Embeddings com sentence-transformers
- Filtro por cosine similarity
- Cache com Redis
```

---

## Fase 3 - Monetizacao e Profissionalismo

### Sistema de Planos/Assinatura

**Nivel:** 🔴 Dificil | **Prioridade:** Media

```
Planos sugeridos:
  Gratuito:
    - 3 servicos ativos
    - Sem prioridade na busca
  
  Pro (R$ 29/mes):
    - Servicos ilimitados
    - Prioridade na busca
    - Badge "Profissional Verificado"
  
  Empresa (R$ 99/mes):
    - Tudo do Pro
    - Multi-usuario (ate 5)
    - Dashboard de analytics

Endpoints:
  GET    /api/v1/planos/             -> Listar planos
  POST   /api/v1/assinatura/         -> Criar assinatura
  DELETE /api/v1/assinatura/{id}/    -> Cancelar assinatura
  GET    /api/v1/assinatura/         -> Ver minha assinatura
```

---

### Pagamentos Integrados

**Nivel:** 🔴 Dificil | **Prioridade:** Media

```
Integracao com gateway de pagamento:
- Mercado Pago (Brasil)
- Stripe (internacional)
- PagSeguro

Funcionalidades:
- Pagamento online de servicos
- Escrow (reter pagamento ate conclusao)
- Reembolso em caso de desistencia
- Notas fiscais automatizadas
```

---

### Notificacoes Push

**Nivel:** 🔴 Dificil | **Prioridade:** Media

```
Tipos de notificacao:
- Nova mensagem recebida
- Nova avaliacao
- Proposta recebida
- Solicitacao aceita
- Promocoes e novidades

Tecnologias:
- Firebase Cloud Messaging (FCM) para mobile
- Web Push API para web
- Django Channels para real-time
```

---

## Fase 4 - Seguranca e Qualidade

### Verificacao de Identidade (KYC)

**Nivel:** 🔴 Dificil | **Prioridade:** Media

```
Funcionalidades:
- Upload de documento de identidade
- Selfie com documento
- Verificacao manual ou via API (AWS Rekognition)
- Badge "Verificado" no perfil
- Aprovacao pelo admin
```

---

### Sistema de Denuncia

**Nivel:** 🟡 Medio | **Prioridade:** Alta

```
Modelo:
- denunciante (usuario que denuncia)
- motivo: fraude, spam, conteudo inadequado, outro
- descricao
- evidencias (links, prints)
- status: pendente/em_analise/resolvida

Endpoints:
  POST   /api/v1/denuncias/          -> Criar denuncia
  GET    /api/v1/denuncias/          -> Admin: listar denuncias
  PATCH  /api/v1/denuncias/{id}/     -> Admin: atualizar status
```

---

### Rate Limiting Avancado

**Nivel:** 🟡 Medio | **Prioridade:** Media

```
Funcionalidades:
- Limites diferentes por tipo de usuario
- Limites diferentes por endpoint
- Protecao contra brute force no login
- Blacklist de IPs suspeitos

Configuracoes:
  anon:     100/hour
  user:     1000/hour
  login:    5/min (por IP)
  register: 3/hour (por IP)
```

---

### Logging e Monitoramento

**Nivel:** 🟡 Medio | **Prioridade:** Media

```
Funcionalidades:
- Logs estruturados (JSON)
- Integracao com Sentry (erros)
- Metricas de performance (Prometheus)
- Alertas de uso anomalo
- Dashboard de admin com metricas

Django Apps sugeridos:
  - sentry-sdk
  - django-prometheus
```

---

## Fase 5 - Escalabilidade

### Cache com Redis

**Nivel:** 🟡 Medio | **Prioridade:** Media

```
Funcionalidades:
- Cache de listagens populares
- Cache de buscas frequentes
- Cache de dados de perfil
- Invalidacao inteligente

Django Apps sugeridos:
  - django-redis
  - django-cacheops
```

---

### API Versionada (v2)

**Nivel:** 🟡 Medio | **Prioridade:** Baixa

```
Acoes:
  - Criar /api/v2/ com mudancas breaking
  - Manter /api/v1/ funcional
  - Migracao gradual dos clientes
  - Documentacao separada por versao
```

---

### Deploy e CI/CD

**Nivel:** 🔴 Dificil | **Prioridade:** Alta

```
Stack sugerido:
  - Docker + docker-compose
  - GitHub Actions (CI/CD)
  - Render ou Railway (hosting)
  - Cloudflare (CDN + DNS)
  - PostgreSQL na nuvem (Render/Neon)

Pipeline:
  1. Push para main -> executa testes
  2. Testes passam -> build do Docker
  3. Deploy automatico em staging
  4. Aprovacao manual -> deploy em producao
```

---

## Fase 6 - Mobile e Frontend

### App React/Next.js

**Nivel:** 🔴 Dificil | **Prioridade:** Alta

```
Paginas:
  - Landing page (marketing)
  - Login / Registro
  - Feed de servicos
  - Perfil do profissional
  - Detalhe do servico
  - Meus servicos (CRUD)
  - Mensagens
  - Favoritos
  - Configuracoes
```

---

### App Mobile (React Native / Flutter)

**Nivel:** 🔴 Dificil | **Prioridade:** Media

```
Funcionalidades:
  - Push notifications
  - Camera para fotos
  - GPS para localizacao
  - Offline mode (cache)
  - Deep links
```

---

## Roadmap Resumido

| Fase | Prazo Estimado | Prioridade |
|---|---|---|
| **Fase 1** - Avaliacoes, Mensagens, Propostas | 2-4 semanas | ⭐⭐⭐ |
| **Fase 2** - Favoritos, Estatisticas, Busca IA | 2-3 semanas | ⭐⭐ |
| **Fase 3** - Planos, Pagamentos, Notificacoes | 3-4 semanas | ⭐⭐ |
| **Fase 4** - KYC, Denuncias, Monitoring | 2-3 semanas | ⭐⭐ |
| **Fase 5** - Redis, API v2, CI/CD | 2-3 semanas | ⭐⭐⭐ |
| **Fase 6** - Frontend, Mobile | 4-8 semanas | ⭐⭐⭐ |
