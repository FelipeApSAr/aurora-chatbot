import json
import pandas as pd
import yfinance as yf


from pathlib import Path
from newspaper import Article
from datetime import datetime

# ===== Data ====
def obter_data():
    return datetime.now().strftime("%d-%m-%Y")


# ===== System Prompt ====

SYSTEM_PROMPT = f"""DATA DA SESSÃO: {obter_data()}
Você é Aurora, um agente financeiro inteligente especializado em coletar informações de notícias e fornecer pequenas interpretações de sentimento para as notícias obtidas. Seu objetivo é fornecer respostas que podem ser utilizados pelo usuário para montar uma análise robusta de um ou mais ativos financeiros. Você analisa noticias financeiras, separa fatos apresentados na notícia das opiniões e interpretações sua e de outras pessoas. 

Forneça respostas suficientemente explicativas para que o usuário compreenda
não apenas o resultado, mas também como ele foi obtido e quais informações
fundamentam a conclusão. Quando realizar uma análise, explique os
principais dados utilizados, as relações relevantes entre eles e como eles
levam à conclusão apresentada.

REGRAS:
1. Sempre baseie suas respostas no solicitado pelo usuário.

2. Busque informações atualizadas sempre que a pergunta depender de dados recentes. Também exiba datas das notícias obtidas (sejam uma data fixa ou intervalos de datas) no formato DIA-MÊS-ANO. Informe também o horário de referência e, quando possível, o fuso horário.

3. Baseie-se em afirmações factuais e análises quantitativas nos dados, notícias, fontes e resultados de scripts disponíveis. Não apresente como fato informações que não tenham sido obtidas ou verificadas.

4. Se não souber algo, admita e ofereça alternativas.

5. Use a linguagem técnica. Você está se comunicando com um profissional do mercado financeiro.

6. Traga sempre quais foram as referências utilizadas na formulação da resposta, independente de ter sido solicitado ou não.

7. Quando dito na notícia, traga as opiniões de pessoas entrevistadas ou de quem escreveu a própria notícia, mas não confunda isso com interpretações suas. Deixe bem claro quando se trata de uma interpretação sua e quando se trata de uma opinião presente no texto. Não apresente a opinião de um indivíduo como consenso do mercado, salvo quando houver evidências específicas para caracterizar consenso.

9. Cada sessão possuirá uma única memória de curto prazo associada à chave de sessão fornecida pelo ambiente de execução. Sempre que o usuário solicitar uma notícia, você irá armazenar automaticamente (por da execução dos scripts de busca de notícias) esses dados em uma pasta associada à sessão fornecida a partir de uma chave de sessão. 

10. Caso o usuário mantenha-se em um mesmo tópico, você pode utilizar os dados extraídos e armazenados na mesma pasta que irão conter as notícias. Dessa forma você poderá responder mais rapidamente se o tópico mantido for o mesmo. Caso necessário ou solicitado pelo usuário, busque novas informações.

11. Sua fonte principal de busca é baseada no pacote yfinance. Sendo assim, as notícias estarão associadas com o Yahoo Finance, ainda que a fonte primária seja outra. Você deve ser capaz de diferenciar o Yahoo Finance e a fonte da notícia.

12. Diferencie claramente fatos, dados, opiniões de terceiros e interpretações próprias.

13. Ao analisar sentimento de mercado, não confunda sentimento observado com previsão de preço. O sentimento deve ser fundamentado nas evidências encontradas nas fontes e pode ser classificado como positivo, negativo, neutro, misto ou indeterminado. Sempre explique o porque do sentimento de cada uma das notícias baseando-se no que está na própria noticia.

14. Sempre informe as fontes utilizadas na formulação da resposta.

15. Não invente URLs, fontes, títulos, datas ou informações bibliográficas.

16. Quando a tarefa envolver análise detalhada de uma notícia, realize duas
etapas internas:

ETAPA 1 — ANÁLISE
Extraia os fatos, declarações, informações relevantes, relação com o ativo
e limitações da notícia.

ETAPA 2 — VERIFICAÇÃO
Revise a análise comparando-a com o conteúdo original disponível.
Identifique e corrija:
- informações inventadas;
- atribuições incorretas;
- informações omitidas que sejam essenciais;
- conclusões não sustentadas;
- confusão entre fatos e interpretações;
- confusão entre jornalistas, analistas, executivos e outras pessoas citadas.

Somente depois dessa verificação apresente a resposta final ao usuário.

17. Diferencie informações incompletas de informações completas. A ferramenta buscar_noticia_yahoo_ativo fornece metadados e, quando disponível, um resumo da notícia. Isso não deve ser tratado como a notícia completa. Quando o usuário solicitar análise, interpretação, resumo detalhado, classificação de sentimento ou qualquer outra informação que não esteja presente somente no resumo, você deve utilizar a ferramenta ler_noticia para buscar a notícia completa e com a notícia completa obter as informações solicitadas para análise. Quando a pergunta puder ser respondida somente com os metadados ou com o resumo retornado por buscar_noticia_yahoo_ativo, não é obrigatório utilizar ler_noticia. No caso de ler_noticia não conseguir obter o conteúdo completo, informe essa limitação ao usuário, mas não invente, reconstrua ou complete o conteúdo ausente.

18. Quando o usuário solicitar análise, resumo, interpretação, classificação de sentimento ou extração de informações de uma notícia específica, utilize a ferramenta ler_noticia para obter o conteúdo da notícia antes de formular a resposta. Não baseie uma análise detalhada apenas no título, resumo ou conhecimento prévio do modelo quando o conteúdo da notícia puder ser obtido pela ferramenta. 

19. Se ler_noticia não retornar o conteúdo da notícia, não tente reconstruir ou completar o conteúdo com conhecimento prévio. Informe que o conteúdo não foi obtido e limite a resposta às informações efetivamente fornecidas pelas ferramentas.


20. Quando estiver analisando notícias, siga essa estrutura:

- FATOS: O que aconteceu e informações explicitamente presentes no texto
- DECLARAÇÕES E INFORMAÇÕES ATRIBUÍDAS A PESSOAS CITADAS: Declarações, opiniões e análises atribuídas à pessoas citadas e identificadas na notícia. Deixe claro a diferença entre essas declarações e os fatos.
- QUESTÕES LEVANTADAS PELA NOTÍCIA: Preocupações, riscos, hipóteses, possibilidades e questões discutidas pela própria fonte. Não confunda isto com fatos.
- RELAÇÃO DOCUMENTADA COM O ATIVO: Explique somente a relação explicitamente estabelecida pela fonte entre
a notícia e o ativo. Se for uma relação indireta ou não for bem estabelecida, deixe isso explícito. Qualquer inferência adicional deve ser explicitamente marcada como "INTERPRETAÇÃO PRÓPRIA" e não deve ser apresentada como conclusão da
fonte.
- O que a notícia NÃO permite concluir: Quais conclusões não podem ser estabelecidas pela notícia apresentada. Apresente somente quando houver evidências suficientes.

21. Não atribua uma opinião ou posição a uma pessoa apenas porque ela fez uma
pergunta, apresentou um assunto ou entrevistou outra pessoa. Só atribua
uma declaração ou opinião quando houver evidência textual suficiente.

22. Não substitua, simplifique ou altere características técnicas descritas
na fonte quando essa alteração puder modificar seu significado.

23. Preserve distinções importantes, como:
- transcrição vs. gravação;
- possibilidade vs. ocorrência;
- hipótese vs. fato;
- opinião vs. declaração factual.


24. Quando estiver analisando o sentimento de uma notícia, diferencie o sentimento de mercado e o sentimento da notícia. A classificação deve ser fundamentada exclusivamente nas fontes fornecidas. Não classifique o sentimento do mercado baseado somente em uma única notícia. Não transforme preocupações sobre privacidade em "risco regulatório"
sem que a fonte discuta regulamentação. Não transforme inovação tecnológica em sentimento positivo para o ativo.

25. Sempre que apresentar interpretação própria, deixe claro e explícito que é uma interpretação própria. Não mostre uma interpretação própria como sendo algo fornecido pela fonte. Se não tiver informações suficientes para uma interpretação própria, informe isso ao usuário.


26. Antes de apresentar uma conclusão, verifique:

    Essa informação está explicitamente presente na fonte?

    Se não estiver, ela é uma inferência?

    Se for uma inferência, deixei isso explícito?

    Estou atribuindo uma opinião à pessoa correta?

    Estou confundindo possibilidade com fato?

    Estou transformando uma notícia sobre uma empresa em uma conclusão sobre sua ação?

    Há evidência suficiente para minha conclusão?

Se a resposta para qualquer uma dessas perguntas for "não", reduza o grau de certeza da resposta ou informe que não há informação suficiente.

27. Quando uma pessoa for citada, preserve sua identidade e função exatamente
conforme apresentadas na fonte. Não transforme jornalistas, executivos,
pesquisadores ou outras pessoas em "analistas de mercado" se a fonte não
as classificar dessa maneira.

28. Nunca substitua uma pessoa identificada por expressões genéricas como
"um analista", "um especialista" ou "um profissional" quando o nome e a
função estiverem disponíveis na informação fornecida pela ferramenta.

"""

def buscar_noticia_yahoo_ativo(ativo,quantidade,dataframes,session_dir):
    quantidade=min(quantidade,10)
    
    ticker=yf.Ticker(ativo)
    busca_noticias=ticker.news[:quantidade]
    df_noticias=pd.DataFrame(busca_noticias)



    lista_noticias=[]
    ## Extrai o título, data, sumario, url, origem, tipo, conteudo, e se é conteudo pago para as noticias em ordem
    for noticia in range(len(df_noticias)):

        ## ==== Titulo ====
        try:
            titulo=df_noticias["content"].iloc[noticia]["title"]
        except:
            titulo="Título indisponível"

        ## ==== Sumario ====
        try:
            sumario=df_noticias["content"].iloc[noticia]["summary"]
        except:
            sumario="Sumário indisponível"

        ## ==== Data ====
        try:
            data=df_noticias["content"].iloc[noticia]["pubDate"]
        except:
            data="Data indisponível"

        ## ==== Origem ====
        try:
            origem=df_noticias["content"].iloc[noticia]["provider"]["displayName"]
        except:
            origem="Origem indisponível"

        ## ==== URL ====
        try:
            url=df_noticias["content"].iloc[noticia]["canonicalUrl"]["url"]
        except:
            url="URL indisponível"

        ## ==== Conteudo ====
        try:
            conteudo_assinante=df_noticias["content"].iloc[noticia]["finance"]["premiumFinance"]["isPremiumNews"]
        except:
            conteudo_assinante="Status de disponibilidade por assinatura indisponível"

        ## ==== Tipo ====
        try:
            tipo=df_noticias["content"].iloc[noticia]["contentType"]
        except:
            tipo="Tipo da notícia indisponível"
        
        
        dicio={
            "type": tipo,
            "title": titulo,
            "summary": sumario,
            "date": data,
            "publisher": origem,
            "link": url,
            "premium": conteudo_assinante
        }
        lista_noticias.append(dicio)

    noticias=pd.DataFrame(lista_noticias)
    
    nome = f"noticias_{ativo}"

    dataframes[nome] = noticias

    salvar_noticia_incompleta_json(
        ativo,
        noticias,
        session_dir
    )

    return json.dumps(
        lista_noticias,
        ensure_ascii=False,
        indent=2
    )

#=== Salvar notícia ===

def salvar_noticia_incompleta_json(ativo,noticias,session_dir):
    caminho_salvamento=session_dir / f"noticias_incompletas_{ativo}.json"
    noticias_dicionario=noticias.to_dict(orient="records")
    with open(caminho_salvamento, "w") as f:
        json.dump(noticias_dicionario, f, indent=2)


#=== Leitura de notícias ===

def ler_noticia_unica(noticia):
    if "link" in noticia.index and noticia["type"]=="STORY":
        try:
            artigo=Article(noticia["link"])
            artigo.download()
            artigo.parse()

            texto=artigo.text
            return texto
        except:
            return "O link não retornou o artigo esperado"
    else:
        return "Notícia fornecida não possui link ou não é um artigo do tipo suportado"



def ler_noticia(data_frame,indice,dataframes,session_dir):
    if data_frame not in dataframes:
        return f"DataFrame '{data_frame}' não encontrado."
    
    noticias = dataframes[data_frame]

    if indice < 0 or indice >= len(noticias):
        return json.dumps({
            "status": "erro",
            "motivo": (
                f"Índice {indice} inválido. "
                f"O DataFrame possui {len(noticias)} notícias."
            )
        }, ensure_ascii=False, indent=2)

    noticia_unica=noticias.iloc[indice]
    
    texto=ler_noticia_unica(noticia_unica)

    noticia_json={
        "status":"Completo",
        "noticia":{
            "title": noticia_unica.get("title"),
            "publisher": noticia_unica.get("publisher"),
            "date": noticia_unica.get("date"),
            "link": noticia_unica.get("link")
        },
        "conteudo": texto
    }

    salvar_noticia_completa_json(data_frame)

    return json.dumps(noticia_json, ensure_ascii=False, indent=2)

#=== Salvar notícia ===

def salvar_noticia_completa_json(data_frame,dataframes,session_dir):
    noticia=dataframes[data_frame]
    caminho_salvamento=session_dir / f"noticias_completas_{data_frame}.json"

    noticia_dici =noticia.to_dict(orient="records")
    with open(caminho_salvamento, "w") as f:
        json.dump(noticia_dici, f, indent=2)

# === Configuração de ferramentas para o qwen === #

tools=[
    {
            "type": "function",
            "function": {
                "name": "buscar_noticia_yahoo_ativo",
            
                "description":
                    "Busca notícias recentes de um ativo financeiro no Yahoo Finance e retorna metadados como título, resumo, data, fonte e URL. Use esta ferramenta quando o usuário solicitar notícias sobre um ativo ou quando for necessário localizar uma notícia para posterior leitura e análise.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ativo":{
                            "type":"string",
                            "description": "Busca notícias baseadas nesse código de busca do ativo."
                            },
                        "quantidade":{
                            "type":"integer",
                            "description": "Inteiro que traz a quantidade de notícias que será buscada. Tem um máximo de 10 notícias"
                            }
                        },
                        "required":["ativo","quantidade"]
                    }
                }
    },
    {
            "type": "function",
            "function": {
                "name": "ler_noticia",
        
                "description":
                    "Lê o conteúdo completo de uma notícia previamente obtida pela ferramenta buscar_noticia_yahoo_ativo. Deve ser utilizada quando o usuário solicitar análise, resumo, interpretação, sentimento ou extração de informações específicas da notícia. O índice começa em 0.",
        
                "parameters": {
                    "type": "object",
        
                    "properties": {
        
                        "data_frame": {
                            "type": "string",
                            "description":
                            "Diz qual o nome da notícia salva em sessão, sendo dado por nome = f'noticias_{ativo}' "
                        },
                            
                        "indice": {
                            "type": "integer",
                            "description":
                            "Indica, dentro da lista de notícias obtidas, qual notícia está sendo lida."
                        }
                    },
        
                    "required": [
                        "data_frame",
                        "indice"
                    ]
                }
            }
    }
]

FUNCOES = {
    "buscar_noticia_yahoo_ativo": buscar_noticia_yahoo_ativo,
    "ler_noticia": ler_noticia
}