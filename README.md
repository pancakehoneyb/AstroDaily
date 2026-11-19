# AstroDaily

**Diário de observações astronômicas** para Android, integrado a uma API REST com banco de dados relacional.

O usuário registra o que observou no céu (Lua, planetas, estrelas, constelações, galáxias), informa as condições da noite e o app **calcula uma nota de visibilidade** e classifica a noite como *Excelente*, *Boa*, *Regular* ou *Ruim*. Todos os registros ficam salvos no banco por meio da API.

> Projeto desenvolvido para a **Avaliação Parcial 2 (AP2)** da disciplina de **Desenvolvimento Mobile**.

---

## Funcionalidades

- Cadastro e login simplificado por e-mail, com escolha do **tipo de observador** (olho nu, instrumentos, astrofotógrafo iniciante ou avançado)
- Registro de observações com objeto observado, local, condição do céu, poluição luminosa, lua visível e anotações
- **Nota de visibilidade (0 a 100)** calculada pela API e **classificação da noite**
- Lista de observações do usuário, vinda da API
- Detalhe, **edição** e **exclusão** de cada observação
- **Compartilhar** a observação e **abrir o local no mapa** (Intents implícitas)
- **Sistema de XP e patentes** exibido na home (Iniciante, Explorador, Astrônomo Experiente, Mestre do Céu)

### Como a nota é calculada

A nota parte de 100 e desconta pontos conforme as condições:

| Fator | Desconto |
|---|---|
| Céu parcialmente nublado | −30 |
| Céu nublado | −60 |
| Poluição luminosa (0 a 10) | −4 por nível |
| Lua visível (quando o alvo não é a própria Lua) | −10 |

| Nota | Classificação |
|---|---|
| 80 a 100 | Excelente |
| 60 a 79 | Boa |
| 40 a 59 | Regular |
| 0 a 39 | Ruim |

**XP:** 10 pontos por observação, 5 por foto e 5 por equipamento cadastrado.
**Patentes:** Iniciante (0 a 39), Explorador (40 a 99), Astrônomo Experiente (100 a 199), Mestre do Céu (200+).

---

## Tecnologias

**Aplicativo Android**
- Kotlin
- XML com View Binding
- Material Components (Material 3, tema escuro)
- Retrofit 2 + Gson (consumo da API REST)
- Kotlin Coroutines (chamadas assíncronas)
- RecyclerView e SharedPreferences
- minSdk 24

**Backend**
- Python 3
- FastAPI
- SQLAlchemy 2
- SQLite (banco relacional)
- Uvicorn
- Swagger / OpenAPI (gerado automaticamente)

---

## Estrutura do repositório

```
astrodaily/
├── android/                      # Aplicativo Android (Kotlin)
│   └── app/src/main/
│       ├── java/com/example/astrodaily/
│       │   ├── data/             # Modelos, ApiService, RetrofitClient, SessionManager
│       │   ├── ui/               # Activities e Adapter
│       │   └── util/             # Opções de Spinner, constantes e formatadores
│       └── res/                  # Layouts, tema e recursos
├── backend/                      # API REST (FastAPI)
│   ├── app/
│   │   ├── routers/              # usuarios, equipamentos, observacoes
│   │   ├── database.py           # Conexão com o SQLite
│   │   ├── models.py             # Tabelas (SQLAlchemy)
│   │   ├── schemas.py            # Validação e serialização (Pydantic)
│   │   ├── services.py           # Regras de negócio (nota, XP, patente)
│   │   └── main.py               # Aplicação e Swagger
│   └── requirements.txt
└── README.md
```

---

## Como executar

### Pré-requisitos
- Python 3.10 ou superior
- Android Studio (com SDK instalado)
- Um emulador Android ou um celular com depuração USB

### 1. Backend (API)

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O banco SQLite (`astrodiario.db`) é criado automaticamente na primeira execução.

- API: http://localhost:8000
- **Swagger:** http://localhost:8000/docs

> Deixe o servidor rodando enquanto usa o aplicativo.

### 2. Aplicativo Android

1. Abra a pasta **`android`** no Android Studio (**File → Open**) e aguarde a sincronização do Gradle.
2. Confira o endereço da API em `data/RetrofitClient.kt`:
   - **Emulador:** `http://10.0.2.2:8000/` (já é o padrão; `10.0.2.2` é o `localhost` do computador visto pelo emulador)
   - **Celular físico:** use o IP do computador na rede, por exemplo `http://192.168.0.10:8000/`. Celular e computador precisam estar no mesmo Wi-Fi.
3. Selecione o dispositivo e clique em **Run**.

> O app usa tráfego HTTP sem SSL em ambiente de desenvolvimento (`usesCleartextTraffic` habilitado no manifest).

---

## API REST

Todos os dados trafegam em **JSON**. A documentação interativa está no **Swagger**: `http://localhost:8000/docs` (com o servidor em execução).

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/usuarios` | Cadastra um usuário (e-mail único) |
| `GET` | `/usuarios/login?email=` | Busca o usuário pelo e-mail |
| `GET` | `/usuarios/{id}` | Consulta um usuário |
| `PUT` | `/usuarios/{id}` | Altera nome ou nível |
| `DELETE` | `/usuarios/{id}` | Remove o usuário e seus dados |
| `GET` | `/usuarios/{id}/estatisticas` | Total de observações, média das notas, objeto mais observado, XP e patente |

### Observações

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/observacoes` | Cria uma observação (calcula nota e classificação) |
| `GET` | `/observacoes?usuario_id=` | Lista as observações, filtrando por usuário |
| `GET` | `/observacoes/{id}` | Consulta uma observação |
| `PUT` | `/observacoes/{id}` | Altera uma observação (recalcula a nota) |
| `DELETE` | `/observacoes/{id}` | Remove uma observação |
| `GET` | `/observacoes/publicas` | Feed de observações marcadas como públicas |
| `POST` | `/observacoes/{id}/foto` | Anexa uma foto (`multipart/form-data`) |

### Equipamentos

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/usuarios/{id}/equipamentos` | Adiciona um equipamento ao usuário |
| `GET` | `/usuarios/{id}/equipamentos` | Lista os equipamentos do usuário |
| `DELETE` | `/equipamentos/{id}` | Remove um equipamento |

### Exemplo de requisição

`POST /observacoes`

```json
{
  "usuario_id": 1,
  "titulo": "Saturno e seus anéis",
  "descricao": "Vi os anéis com binóculos.",
  "tipo_objeto": "PLANETA",
  "local": "Pedra da Gávea, Rio de Janeiro",
  "nuvens": "LIMPO",
  "poluicao_luminosa": 3,
  "lua_visivel": false,
  "publica": false
}
```

Resposta (resumida):

```json
{
  "id": 1,
  "titulo": "Saturno e seus anéis",
  "nota_visibilidade": 88,
  "classificacao": "Excelente",
  "data": "2026-11-15T21:30:00"
}
```

---

## Banco de dados

Banco relacional **SQLite**, acessado exclusivamente pela API via SQLAlchemy.

| Tabela | Colunas principais |
|---|---|
| `usuarios` | `id`, `nome`, `email` (único), `nivel` |
| `equipamentos` | `id`, `usuario_id` (FK), `tipo`, `modelo` |
| `observacoes` | `id`, `usuario_id` (FK), `titulo`, `descricao`, `tipo_objeto`, `local`, `nuvens`, `poluicao_luminosa`, `lua_visivel`, `nota_visibilidade`, `classificacao`, `foto_url`, `publica`, `data` |

Relacionamentos: um usuário tem muitos equipamentos e muitas observações (exclusão em cascata).

---

## Telas do aplicativo

| # | Tela (Activity) | Função |
|---|---|---|
| 1 | `LoginActivity` | Criar conta ou entrar com e-mail |
| 2 | `HomeActivity` | Menu principal, saudação e patente/XP |
| 3 | `NovaObservacaoActivity` | Formulário para criar **e editar** observações |
| 4 | `MinhasObservacoesActivity` | Lista (RecyclerView) vinda da API |
| 5 | `DetalheObservacaoActivity` | Nota calculada, editar, excluir, compartilhar e abrir mapa |

### Navegação e Intents
- **Intents explícitas:** Login → Home → Nova observação / Minhas observações → Detalhe → Editar
- **Intents implícitas:**
  - `ACTION_SEND` para compartilhar a observação
  - `ACTION_VIEW` com `geo:` para abrir o local no mapa (com abertura no navegador como alternativa)

### Componentes de interface utilizados
`TextView`, `EditText`, `Button`, `ImageView`, `Spinner`, `RadioButton`, `SeekBar`, `Switch`, `RecyclerView`, `CardView` e `ProgressBar`.

---

## Organização do código

- **Separação de responsabilidades:** camada `data` (modelos e rede), `ui` (telas) e `util` (apoio)
- **`BaseActivity`:** centraliza o botão voltar e as chamadas à API com tratamento de erro, evitando código repetido
- **Uma única tela de formulário** serve para criar e editar observações
- **Backend em camadas:** rotas, schemas de validação, modelos e regras de negócio em arquivos separados

---

## Melhorias futuras

- Tela de **equipamentos** e perfil no aplicativo (a API já suporta)
- **Upload de fotos** pelo aplicativo (o endpoint já existe)
- Tela de **comunidade** com o feed público (o endpoint já existe)
- Autenticação com senha e token
- Deploy da API em nuvem

---

## Licença

Projeto acadêmico, desenvolvido para fins educacionais.
