# 📈 Finance App API

API para análise de investimentos em ações e FIIs (Fundos de Investimento Imobiliário) do mercado brasileiro.

## 🎯 Sobre o Projeto

Esta API realiza web scraping de sites financeiros brasileiros para coletar dados fundamentalistas de ações e informações sobre FIIs, permitindo que investidores consultem indicadores importantes para tomada de decisão.

## ⚙️ Funcionalidades Atuais

- **Consulta de Ações** - Dados fundamentalistas de ações (P/L, P/VP, ROE, ROIC, margens, etc.)
- **Consulta de FIIs** - Informações sobre dividendos de Fundos Imobiliários
- **Histórico de Dividendos** - Proventos pagos pelas empresas
- **Sistema de Scoring** - Algoritmo de avaliação de ações em 5 etapas:
  - 🛡️ Sobrevivência (liquidez, dívida, margem)
  - 💰 Valuation (P/L, P/VP, EV/EBIT)
  - ⭐ Qualidade (ROE, ROIC, margem EBIT)
  - 📊 Consistência (histórico de retornos)
  - ⚠️ Risco & Contexto (setor, crescimento)
- **Sistema de Usuários** - Cadastro, login e autenticação JWT (roles: `user`, `admin`)
- **Análise com IA** - Análise de investimento via Google Gemini (endpoint `/tickers/analyze/`)

## 🛠️ Tecnologias

- **Python 3.13**
- **Flask** – Framework web
- **Flask-CORS** – CORS para consumo por frontend
- **BeautifulSoup4** (bs4) – Web scraping
- **Requests** – Requisições HTTP
- **PyJWT** – Tokens de autenticação
- **python-dotenv** – Variáveis de ambiente
- **mysql-connector-python** – Conexão com MySQL
- **Google Genai** – Análise de investimentos com Gemini
- **Gunicorn** – Servidor WSGI (uso em Docker/produção)
- **Docker** – Containerização (Dockerfile + docker-compose com MySQL)
- **Jenkins** – Pipeline CI (build, testes, build da imagem Docker)

## 📦 Instalação

### Local (Python)

```bash
# Clone o repositório
git clone https://github.com/Kcarlos-dev/finance-app.git
cd finance-app

# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação (localhost)
python app.py
# Para aceitar acesso pela rede (via IP): use host="0.0.0.0" em app.run()
```

### Docker (app + MySQL)

O projeto inclui `Dockerfile` e `docker-compose.yml`. O MySQL sobe com os scripts em `database/user/queries/` (ex.: `01-users.sql`) executados na primeira inicialização.

```bash
# Subir app e MySQL
docker compose up -d

# A API fica em http://localhost:5000 (e acessível via IP na porta 5000)
# MySQL na porta 3306
```

O container da app usa **Gunicorn** e escuta em `0.0.0.0:5000`. Variáveis de ambiente vêm do `.env`; no compose, o serviço MySQL espera `MYSQL_PASSWORD` e `MYSQL_DB` no `.env`.

## ⚙️ Configuração

Crie um arquivo `.env` na raiz com as variáveis necessárias, por exemplo:

- **CORS** – `CORS_ORIGINS` (origens permitidas, separadas por vírgula)
- **MySQL** – host, usuário, senha, banco (no Docker, use `MYSQL_HOST=mysql` quando rodar via compose)
- **Gemini** – chave da API Google Genai

O app usa `service.util.config.get_config()` para ler essas configurações.

## 🗄️ Banco de Dados

O schema é aplicado via scripts em `database/user/queries/` (ex.: `01-users.sql`). No Docker, esses arquivos são executados automaticamente na primeira subida do MySQL (`docker-entrypoint-initdb.d`).

### Tabela `users`

```sql
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `auth` varchar(100) DEFAULT 'user',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

| Campo      | Tipo         | Descrição                           |
|------------|--------------|-------------------------------------|
| `id`       | bigint       | Chave primária, auto incremento     |
| `email`    | varchar(100) | E-mail do usuário (obrigatório)     |
| `name`     | varchar(100) | Nome do usuário (obrigatório)       |
| `password` | varchar(255) | Senha (hash, obrigatório)           |
| `auth`     | varchar(100) | Nível de autorização (default: user) |

## 🔌 Endpoints

Os endpoints de **Ações**, **FIIs** e **Análise** exigem autenticação: envie o header `Authorization: Bearer <token>` (token obtido em `POST /users/login`).

### Usuários (públicos)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/users/register` | Cadastro de usuário (body: `email`, `name`, `password`) |
| POST | `/users/login` | Login (body: `email`, `password`) — retorna `token` |

### Ações (autenticados)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tickers/papers/<ticker>` | Dados fundamentalistas de uma ação |
| GET | `/tickers/dividends/<ticker>` | Histórico de dividendos de uma ação |

### FIIs (autenticados)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tickers/yields/<ticker>` | Dados de rendimentos de um FII |

### Análise com IA (autenticados)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/tickers/analyze/` | Análise de investimento com Gemini (body: `{ "data": "..." }`) |

### Exemplos de Uso

```bash
# Cadastro
curl -X POST http://localhost:5000/users/register -H "Content-Type: application/json" -d '{"email":"user@email.com","name":"Nome","password":"senha123"}'

# Login (guarde o token retornado)
curl -X POST http://localhost:5000/users/login -H "Content-Type: application/json" -d '{"email":"user@email.com","password":"senha123"}'

# Consultar dados da Petrobras (com token)
curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:5000/tickers/papers/PETR4

# Consultar dividendos do Banco do Brasil
curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:5000/tickers/dividends/BBAS3

# Consultar FII HGLG11
curl -H "Authorization: Bearer SEU_TOKEN" http://localhost:5000/tickers/yields/HGLG11

# Análise com Gemini
curl -X POST http://localhost:5000/tickers/analyze/ -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" -d '{"data":"PETR4"}'
```

## 📊 Fontes de Dados

- [Fundamentus](https://www.fundamentus.com.br) – Dados fundamentalistas de ações
- [FIIs.com.br](https://fiis.com.br) – Dados de Fundos Imobiliários

## 🔄 CI/CD (Jenkins)

O repositório inclui um `Jenkinsfile` para pipeline no Jenkins:

- **Checkout** – branch `dev` do repositório
- **Instalar dependências** – venv + `pip install -r requirements.txt`
- **Verificação básica** – `py_compile` do `app.py`
- **Build Docker** – build da imagem (quando existe `Dockerfile`)

---

## 🚀 Roadmap - Melhorias Futuras

### 🔐 Sistema de Usuários
- ~~Autenticação com JWT~~ ✅
- ~~Cadastro e login de usuários~~ ✅
- Gerenciamento de perfil

### 💼 Carteira de Investimentos
- ~~Banco de dados MySQL para persistência (tabela `users`)~~ ✅
- Cadastro de ações que o usuário possui
- Cálculo de rentabilidade da carteira
- Histórico de compras e vendas
- Dashboard com rendimentos e dividendos recebidos

### ⚡ Cache com Redis
- Implementação de cache para reduzir requisições de web scraping
- Se um usuário consultar uma ação que outro já consultou, os dados serão servidos do cache
- Melhoria significativa na performance e tempo de resposta
- Respeito aos sites fonte (menos requisições)

### 🤖 Análise com Inteligência Artificial
- ~~Integração com LLM (Gemini)~~ ✅ — endpoint `POST /tickers/analyze/`
- Análise detalhada explicando **por que** uma ação é ou não uma boa opção
- Identificação de pontos positivos e riscos
- Recomendações personalizadas por perfil de investidor
- Linguagem acessível para iniciantes

### 📱 Frontend
- https://github.com/Kcarlos-dev/frontend-finance-app
- Interface web moderna e responsiva
- Gráficos interativos de evolução
- Dashboard personalizado por usuário

---

## ⚠️ Aviso Legal

Esta aplicação é apenas para fins educacionais e informativos. **Não constitui recomendação de investimento**. Sempre consulte um profissional certificado antes de tomar decisões de investimento.

## 📄 Licença

Este projeto está sob a licença MIT.

---

Desenvolvido com ☕ e 📈

