# 🤖 Aurora Chatbot — Agente Financeiro Inteligente com IA Generativa

> Repositório com um pequeno projeto de chatbot voltado à área financeira, desenvolvido a partir do desafio de laboratório **"Bia do Futuro"** da [Digital Innovation One](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).

## 📖 Sobre o projeto

Este projeto propõe idealizar e prototipar um **agente financeiro** que utiliza IA Generativa para atividades que apoiam um analista do mercado financeiro. Esse chatbot pode coletar e analisar notícias recentes de ativos financeiros. No futuro, desejo incrementar ferramentas de análise de dados automatizadas e controladas por meio da IA.

## 🗂️ Estrutura do repositório

```
aurora-chatbot/
│
├── README.md
│
│
├── docs/                          # Documentação do projeto
│   ├── 01-documentacao-agente.md  # Caso de uso, persona e arquitetura
│   ├── 02-base-conhecimento.md    # Estratégia de dados
│   ├── 03-prompts.md              # Engenharia de prompts
│   ├── 04-metricas.md             # Avaliação e métricas
│   └── 05-pitch.md                # Roteiro do pitch
│
└── src/                           # Código-fonte da aplicação
    ├── Sessions/                  # Guarda as sessões do agente
    ├── app.py                     # Aplicações visuais do chatbot
    ├── agente.py                  # Parte da execução do chatbot
    ├── config.py                  # Arquivo de configurações do chatbot
    └── requirements.txt           # Requisitos para execução do chatbot


```

## 📋 Documentação do agente

A documentação completa do agente está na pasta [`docs/`](./docs) e cobre:

| Documento | Conteúdo |
| --- | --- |
| `01-documentacao-agente.md` | Caso de uso, persona, tom de voz e arquitetura do agente |
| `02-base-conhecimento.md` | Estrutura e estratégia da base de conhecimento |
| `03-prompts.md` | System prompt, exemplos de interação e tratamento de edge cases |
| `04-metricas.md` | Métricas de avaliação (precisão, taxa de alucinação, coerência) |
| `05-pitch.md` | Roteiro do pitch de apresentação do agente |

## 🧠 Base de conhecimento

O agente utiliza dados de notícias obtidos via yfinance utilizando o ticker de um ativo financeiro

## 🛠️ Tecnologias e ferramentas

| Categoria | Ferramentas |
| --- | --- |
| **LLMs** | Ollama |
| **Desenvolvimento** | Streamlit |
| **Dados** | yfinance |


## 🚀 Como executar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/FelipeApSAr/lab-chatbot.git
   cd lab-chatbot
   ```
2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Instale as dependências do projeto (ajuste conforme o `requirements.txt` do repositório):
   ```bash
   pip install -r requirements.txt
   ```
4. Configure sua chave de API do provedor de LLM escolhido como variável de ambiente, por exemplo:
   ```bash
   export OPENAI_API_KEY="sua_chave_aqui"
   ```
5. Execute a aplicação (exemplo com Streamlit):
   ```bash
   streamlit run src/app.py
   ```


## 📊 Avaliação e métricas

A qualidade do agente é avaliada considerando:

- **Precisão/assertividade** das respostas geradas;
- **Taxa de respostas seguras**, sem alucinações;
- **Coerência** das respostas com o perfil e contexto do cliente.

Detalhes completos em [`docs/04-metricas.md`](./docs/04-metricas.md).

## 🎯 Créditos

Este repositório é um **fork** do desafio de laboratório da [Digital Innovation One](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro), adaptado por [@FelipeApSAr](https://github.com/FelipeApSAr).

## 📄 Licença

Este projeto segue os termos de licença do repositório original. Consulte o repositório para mais detalhes.
