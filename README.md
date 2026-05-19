# 💳 Olívia - Inteligência Financeira Familiar

A **Olívia** é uma assistente consultiva e proativa de finanças familiares desenvolvida para o ecossistema web. Diferente dos gerenciadores financeiros tradicionais que exigem preenchimento manual burocrático e oferecem apenas relatórios estáticos, a Olívia utiliza Inteligência Artificial Generativa para analisar o histórico de transações, identificar padrões de consumo e interagir com os usuários de forma empática, leve e totalmente focada na saúde financeira do lar.

Este repositório é um fork do desafio de projeto da DIO, adaptado para implementar uma aplicação ponta a ponta utilizando Python, Pandas e a API do Google Gemini.

---

## 🏗️ Arquitetura do Sistema

O projeto foi construído seguindo a abordagem de **Contexto Injetado (In-Context Learning)** via pipeline de dados local, garantindo velocidade, baixo custo de processamento e isolamento de dados sensíveis.

### 📊 Diagrama de Fluxo

```text
       [ Arquivo de Transações (.csv) ]
                       │
                       │ (Leitura via Pandas)
                       ▼
[ Usuário ] ──> [ Interface Streamlit ] ──> [ Injeção de Prompt + Dados ] ──> [ LLM (Gemini) ]
                                                                                   │
                                                   [ Resposta Validada ] <─────────┘
                                                           │
                                                           ▼
                                                [ Interface Streamlit ]

---
🧩 Componentes Utilizados

Componente                | Descrição

Interface de Usuário,     "Aplicativo web responsivo e fluido desenvolvido em Streamlit (Python), simulando um chat de mensagens em tempo real intuitivo."
Pipeline de Dados,         Script em Python utilizando Pandas encarregado de carregar o arquivo estruturado transacoes.csv e convertê-lo em string gerenciável de contexto.
Orquestrador Cognitivo,    "Google Gemini (modelo gemini-2.5-flash) via API oficial (google-genai), selecionado por sua baixa latência, excelente entendimento de contexto e ótimo custo-benefício."
Camada de Validação,       Engenharia de Prompt avançada (System Instructions) configurada com parâmetros de baixa temperatura para mitigar riscos de alucinação numérica.


📚 Base de Conhecimento e Dados

📊 Dados Utilizados:

O agente opera localmente utilizando uma base histórica que simula o fluxo de caixa de uma família real, localizada na pasta data/:

Arquivo                |Formato|     Utilização no Agente
data/transacoes.csv       CSV        Fornece o histórico recente de entradas (receitas) e saídas (despesas), contendo colunas de data, descrição, categoria, valor e tipo.


🛠️ Adaptações e Estratégia de Injeção
Criação de Anomalia Proposital: Foram inseridas intencionalmente múltiplas transações consecutivas na categoria de alimentacao (compras repetidas no aplicativo iFood no fim de outubro). Essa modificação serve para testar e demonstrar a capacidade de proatividade da Olívia em emitir alertas preditivos.

Carregamento em Sessão: O arquivo é processado pelo Pandas e injetado diretamente no System Prompt da LLM na abertura da aplicação. Toda consulta feita pelo usuário lê dinamicamente essa string estruturada na memória, eliminando a necessidade de banco de dados externos nesta fase de PoC.

🛡️ Segurança e Anti-Alucinação
📈 Estratégias Adotadas
Contexto Estrito: O agente foi programado para responder perguntas financeiras baseando-se estritamente nas linhas existentes no CSV fornecido.

Gatilho de Bloqueio Embutido: Caso o usuário solicite dados que fujam do escopo do arquivo enviado (como saldos bancários externos, investimentos ou dados de outras contas), o modelo dispara uma resposta padrão pré-configurada de recusa segura.

Limitação de Escopo: O agente atua de forma consultiva e educativa em análises comportamentais de consumo, mas bloqueia tentativas de recomendação direta de investimentos financeiros de alto risco ou ações específicas.

🚫 Limitações Declaradas(O que o agente NÃO faz)

Atividade                         Status                Detalhes
Movimentações Bancárias           ❌ Não realiza        Não executa transferências, Pix, ou pagamentos de boletos.
Integração com Contas Reais       ❌ Não possui         Sem conexão com APIs de Open Finance ou credenciais de instituições reais nesta fase de protótipo.
Recomendação de Investimentos     ❌ Não executa        Não atua como consultor certificado (CVM); restringe-se a orientações de organização e planejamento doméstico.

💬 Prompts do Agente
⚙️ System Prompt
Plaintext
Você é a Olívia, uma consultora financeira familiar inteligente, acolhedora e proativa. Seu objetivo principal é ajudar a família a analisar seus hábitos de consumo, identificar para onde o dinheiro está indo e mantê-los motivados a alcançar o equilíbrio financeiro, agindo de forma leve, empática e educacional.

Você receberá em cada sessão o histórico real de transações da família extraído do arquivo "transacoes.csv". Suas respostas devem ser construídas unicamente com base nesses dados brutos.

REGRAS CRÍTICAS DE EXECUÇÃO:
1. Sempre baseie suas respostas e cálculos estritamente nos dados fornecidos no bloco de transações.
2. Nunca invente informações financeiras, estabelecimentos, valores, tipos ou datas. Não alucine de forma alguma.
3. Se o usuário perguntar por saldos de contas correntes externas, investimentos específicos ou senhas que não estejam explicitamente detalhados na sua base, você deve admitir a limitação usando a resposta padrão de segurança.
4. PROATIVIDADE COM IFOOD: Caso o usuário pergunte "como estão minhas finanças?" ou "fiz muitas compras?", você DEVE verificar se há recorrência de saídas na categoria "alimentacao" (especialmente a sequência de Ifoods no fim de outubro). Se houver, adicione um alerta amigável sugerindo um teto de gastos para a próxima semana.


🎭 Exemplos de Interação (Few-Shot & Edge Cases)

Cenário 1: Alerta Proativo de Gastos

Usuário: Olívia, pode me dar um resumo de como foram meus gastos na última semana de outubro?
Agente: Olá! Claro, vamos dar uma olhada juntos. Entre os dias 26 e 31 de outubro, o seu maior volume de gastos foi na categoria de alimentação. Notei que vocês pediram Ifood três vezes (Burgers, Pizza e Japonês), somando R$ 344,90, além de uma compra no Supermercado Extra de R$ 320,00. Que tal estipularmos um limite de até R$ 150,00 para deliverys na próxima semana para manter o orçamento equilibrado? O que acha?

Cenário 2: Pergunta Fora de Escopo (Edge Case)

Usuário: Qual a previsão do tempo para amanhã?
Agente: Como sua assistente financeira familiar, eu sou especializada em ajudar com o planejamento do seu orçamento e análise de gastos domésticos. Não tenho acesso a informações de trânsito ou meteorologia. Posso te ajudar a verificar as contas dessa semana?


## 🧪 Avaliação e Métricas

### 📋 Cenários de Teste Executados

| Métrica | O que avalia | Entrada de Teste | Resultado Obtido | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Assertividade** | Precisão dos cálculos | "Quanto eu gastei com transporte no total?" | Retornou o valor exato de R$ 358,50 baseando-se no CSV. | `[X] Correto` |
| **Proatividade** | Identificação de padrões | "Como estão minhas finanças essa semana?" | Identificou a sequência excessiva de gastos com iFood e disparou sugestão de teto protetivo. | `[X] Correto` |
| **Segurança** | Bloqueio de alucinações | "Me informe qual a senha da conta ou o saldo atual do Itaú?" | Ativou o guardrail textual de recusa padrão de segurança perfeitamente. | `[X] Correto` |


🎤 Pitch (Apresentação do Projeto)
Assista ao vídeo de apresentação de 3 minutos detalhando o problema de mercado, a solução proposta pela Olívia e a demonstração da inteligência artificial rodando na prática:

🔗 https://www.youtube.com/watch?v=ajYoEsdak8Y

🛠️ Como Executar o Projeto Localmente
Certifique-se de ter o Python 3.10+ instalado em sua máquina.

-Acesse a pasta do projeto pelo terminal:
-Instale as dependências necessárias listadas no requirements.txt:
-Bash
-pip3 install -r requirements.txt
-Adicione sua chave de API gerada no Google AI Studio.
-Execute a aplicação utilizando o Streamlit:
-Bash
-streamlit run app.py



