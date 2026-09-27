# Base de Conhecimento

## Dados Utilizados

| Fonte | Utilização no Agente |
|--------|---------------------|
| Pacote yfinance | Coleta de notícias sobre o mercado financeiro |



---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Não irei utilizar os dados fornecidos, mas sim adaptar o uso de bibliotecas para que o agente seja capaz de coletá-las.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.
O agente terá a capacidade de chamar uma lista de funções. Dentro dessa lista, há funções de coleta de notícias via yfinance (que fornece um resumo) e de coleta da notícia completa pelo link do yfinance.


### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são digitados pelo usuário. No caso, é utilizado um Ticker compatível com o yfinance. Com isso o modelo coleta notícias e é capaz de interpretá-las.

---


