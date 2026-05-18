# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?
[Famílias modernas possuem múltiplas fontes de despesas e dificuldades para centralizar o orçamento, o que resulta em falta de previsibilidade financeira, incapacidade de poupar para metas de longo prazo e surpresas com contas de cartões de crédito no fim do mês. Os aplicativos tradicionais exigem que o usuário insira tudo manualmente e não geram insights reais.]

### Solução
> Como o agente resolve esse problema de forma proativa?

[O agente atua de forma consultiva e preventiva. Conectado à base de dados de consumo da família, ele identifica padrões de gastos e envia alertas antes do orçamento estourar (ex: "Notei que os gastos com delivery nesta semana subiram 40% em relação à média, restando apenas R$ 50 do seu teto estipulado"). Além disso, ele ajuda a cocriar metas de economia, sugerindo pequenos ajustes diários para alcançar objetivos específicos de forma leve e planejada.]

### Público-Alvo
> Quem vai usar esse agente?

[Casais e famílias que buscam centralizar e organizar as finanças domésticas, equilibrando o pagamento de contas fixas com a construção de patrimônio e realização de metas familiares, mas que não têm tempo para preencher planilhas complexas.]

---

## Persona e Tom de Voz

### Nome do Agente
[Olívia (Sua Consultora Financeira Familiar)]

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

[Consultiva, acolhedora e educativa. A Olívia se comporta como uma conselheira financeira parceira da família. Ela nunca foca na culpa pelo gasto, mas sim na solução e no aprendizado financeiro, incentivando o diálogo sobre dinheiro de forma leve.]

### Tom de Comunicação
> Formal, informal, técnico, acessível?

[Acessível, empático e focado em soluções. Evita jargões técnicos complexos do mercado financeiro. Utiliza uma linguagem clara, próxima e engajadora, transmitindo total segurança e suporte.]

### Exemplos de Linguagem
- Saudação: [ex: "Olá! Que bom falar com você. Dei uma olhada nas metas da família e tenho ótimas notícias sobre a economia para a viagem de vocês. Vamos conferir?"]
- Confirmação: [ex: "Com certeza! Já entendi o objetivo. Vou cruzar esses dados com o orçamento disponível e te mostro o melhor caminho em um segundo."]
- Erro/Limitação: [ex: "Olha, para garantir a sua segurança, eu não consigo acessar diretamente a sua conta bancária para fazer transações, mas posso te orientar perfeitamente em como fazer esse investimento pelo aplicativo do seu banco."]

---

## Arquitetura

### Diagrama

[ Arquivo de Transações (.csv) ]
                       │
                       │ (Leitura via Pandas)
                       ▼
[ Usuário ] ──> [ Interface Streamlit ] ──> [ Injeção de Prompt + Dados ] ──> [ LLM (OpenAI) ]
                                                                                   │
                                                   [ Resposta Validada ] <─────────┘
                                                           │
                                                           ▼
                                                [ Interface Streamlit ]



### Componentes

| Componente | Descrição |
| :--- | :--- |
| **Interface** | Aplicativo web responsivo desenvolvido em **Streamlit (Python)**, que simula um chat intuitivo de mensagens em tempo real para o usuário. |
| **Pipeline de Dados** | Script em **Python com a biblioteca Pandas** encarregado de carregar o arquivo estruturado `transacoes.csv` e convertê-lo em string de texto gerenciável. |
| **LLM** | **OpenAI (GPT-4o-mini)** ou modelo equivalente de mercado via API, responsável pelo processamento cognitivo, análise de contexto e geração de respostas textuais empáticas. |
| **Validação** | Camada de segurança baseada em **Engenharia de Prompt (*System Messages*)** e travas lógicas no código que limitam o escopo de atuação do modelo cognitivo. |

---

## Segurança e Anti-Alucinação

* **Contexto Estrito (Prompt Injetado):** O agente foi programado através do *System Prompt* para analisar e responder perguntas financeiras baseando-se **estritamente** nas linhas e colunas existentes no arquivo `transacoes.csv` injetado na memória da sessão.
* **Admissão Pragmática de Falhas (Gatilho de Bloqueio):** Caso o usuário solicite dados que fujam do escopo do arquivo enviado (como saldos bancários externos, investimentos ou dados de outras contas), o modelo dispara uma resposta padrão pré-configurada de recusa segura.
* **Prevenção de Alucinação Numérica:** O modelo é proibido de deduzir, calcular médias sem base histórica ou inventar transações falsas. Se o estabelecimento ou valor não constar no arquivo, ele é considerado inexistente.
* **Abordagem Educativa Pró-Segurança:** O agente atua de forma consultiva e proativa em análises comportamentais de consumo, mas bloqueia tentativas de recomendação direta de investimentos financeiros de alto risco ou ações específicas.


### Limitações Declaradas
> O que o agente NÃO faz?

* O agente **não realiza nenhuma movimentação bancária**, transações em dinheiro, PIX ou pagamentos de boletos.
* O agente **não possui integração ativa com APIs de bancos reais** (Open Finance) ou bancos de dados externos nesta versão de protótipo, atuando de forma isolada com o arquivo local fornecido.
* O agente **não atua como um consultor de investimentos certificado (Anbima/CVM)**; ele não indica compras de ativos, ações ou fundos específicos, limitando-se a orientar sobre organização orçamental doméstica.
* O agente **não armazena nem retém dados sensíveis de cartões de crédito reais** (como números de cartão, CVV ou senhas), operando estritamente com histórico de categorias e valores anonimizados.
