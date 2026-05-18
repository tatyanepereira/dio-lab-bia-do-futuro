# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

* **Criação de Massa de Dados Sintética:** Para fins de validação do protótipo (PoC), foi gerado um arquivo `transacoes.csv` com dados mockados que simulam o comportamento financeiro real de uma família.
* **Gatilho de Comportamento (Viés de Teste):** Foram inseridas intencionalmente múltiplas transações consecutivas na categoria de `alimentacao_e_delivery` (compras repetidas no aplicativo *iFood* na mesma semana). Essa modificação foi feita estrategicamente para testar a capacidade do agente de identificar anomalias e atuar de forma **proativa**, alertando o usuário sobre o risco de estourar o orçamento daquela categoria.

---

## Estratégia de Integração

### Como os dados são carregados?
> Os dados não dependem de bancos de dados externos complexos nesta fase. Ao iniciar a aplicação no **Streamlit**, um pipeline em Python utilizando a biblioteca **Pandas** (`pd.read_csv`) faz a leitura do arquivo `transacoes.csv`. Esse arquivo é processado, limpo e convertido integralmente em uma string de texto estruturada que permanece armazenada no cache da memória da sessão (`st.cache_data`).

### Como os dados são usados no prompt?
> Os dados convertidos vão diretamente dentro do **System Prompt (Prompt de Sistema)** da LLM logo na abertura da sessão. Eles funcionam como o "limite do mundo" do agente. Toda vez que o usuário envia uma mensagem, o histórico completo do CSV é enviado junto como contexto fixo, permitindo que a IA consulte as linhas de forma dinâmica e imediata para responder, sem a necessidade de realizar novas requisições de leitura de disco.

---

## Exemplo de Contexto Montado

> Abaixo está o exemplo real de como o pipeline em Python formata e entrega os dados estruturados dentro do prompt de sistema para que a LLM possa interpretar:

```text
Você é a Olívia, uma consultora financeira familiar inteligente.
Aqui está o histórico real e atualizado de transações da família:

data       estabelecimento        categoria              valor
2026-05-10 Supermercado Nova Era  alimentacao_e_delivery 450.00
2026-05-12 Ifood *Burgers         alimentacao_e_delivery 120.00
2026-05-14 Uber *Corrida          transporte              35.00
2026-05-15 Ifood *Doces           alimentacao_e_delivery  85.00
2026-05-16 Posto de Combustivel   transporte             200.00
2026-05-17 Ifood *Pizza           alimentacao_e_delivery 110.00
2026-05-18 Academia Mensalidade   lazer                  130.00
2026-05-18 Cinema Shopping        lazer                   60.00

Responda às perguntas baseando-se estritamente nestes dados.

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
