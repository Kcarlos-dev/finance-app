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

## 🛠️ Tecnologias

- **Python 3.13**
- **Flask** - Framework web
- **BeautifulSoup4** - Web scraping
- **Requests** - Requisições HTTP

## 📦 Instalação

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

# Execute a aplicação
python app.py
```

## 🔌 Endpoints

### Ações

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tickers/papers/<ticker>` | Dados fundamentalistas de uma ação |
| GET | `/tickers/dividends/<ticker>` | Histórico de dividendos de uma ação |

### FIIs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tickers/yields/<ticker>` | Dados de rendimentos de um FII |

### Exemplos de Uso

```bash
# Consultar dados da Petrobras
curl http://localhost:5000/tickers/papers/PETR4

# Consultar dividendos do Banco do Brasil
curl http://localhost:5000/tickers/dividends/BBAS3

# Consultar FII HGLG11
curl http://localhost:5000/tickers/yields/HGLG11
```

## 📊 Fontes de Dados

- [Fundamentus](https://www.fundamentus.com.br) - Dados fundamentalistas de ações
- [FIIs.com.br](https://fiis.com.br) - Dados de Fundos Imobiliários

---

## 🚀 Roadmap - Melhorias Futuras

### 🔐 Sistema de Usuários
- Autenticação com JWT
- Cadastro e login de usuários
- Gerenciamento de perfil

### 💼 Carteira de Investimentos
- Banco de dados MySQL para persistência
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
- Integração com LLM (GPT-4, Gemini ou similar)
- Análise detalhada explicando **por que** uma ação é ou não uma boa opção
- Identificação de pontos positivos e riscos
- Recomendações personalizadas por perfil de investidor
- Linguagem acessível para iniciantes

### 📱 Frontend
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

