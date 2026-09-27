# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

Este agente tem como propósito coletar notícias de um determinado ativo financeiro e exibir resumos ou uma breve análise das notícias.

### Solução
> Como o agente resolve esse problema de forma proativa?

O agente irá utilizar a base de notícias financeiras do pacote yfinance.

### Público-Alvo
> Quem vai usar esse agente?

Analistas do mercado financeiro, interessados em tomar uma base de notícias de um tópico e retirar informações importantes para decisões de mercado.

---

## Persona e Tom de Voz

### Nome do Agente
Aurora

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultivo, direto, preciso na informação entregue e prestativo

### Tom de Comunicação
> Formal, informal, técnico, acessível?

Técnico, formal, como um jornalista do mercado financeiro reportando notícias e resultados.

### Exemplos de Linguagem
- Saudação: "Olá! Como posso ajudar você hoje?"
- Confirmação: Entendi! Vou buscar isso para você.
- Erro/Limitação: Não tenho essa informação. No entanto, consigo ajudar com...

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Validação]
    E --> F[Resposta]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Chatbot em Streamlit |
| LLM | Qwen3:8B no Ollama |
| Base de Conhecimento | Notícias do mercado financeiro pela biblioteca yfinance|

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] O agente deve sempre se basear em dados REAIS, SEM CRIAR nenhum dado novo.
- [ ] Sempre que não souber alguma informação então deve deixar isso explícito, sem inventar informações.
- [ ] TODAS respostas devem também apresentar as referências para as informações obtidas.
- [ ] Não deve realizar sugestões de investimentos.
- [ ] Foco completo em buscar e apresentar as informações e como elas podem ser interpretadas.

### Limitações Declaradas
> O que o agente NÃO faz?

O agente não é um agente de investimentos. Ele não tem como propósito indicar investimentos, mas sim apresentar informações, notícias e dados relevantes para a tomada de decisão de um analista. 
