# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação do protótipo da Olívia foi realizada de forma híbrida:
1. **Testes estruturados em lote:** Execução de perguntas-chave diretamente na interface do Streamlit para validar cálculos e comportamentos do prompt de sistema.
2. **Feedback em ambiente controlado:** Teste de usabilidade realizado com membros da família (simulando os usuários reais do orçamento doméstico) para avaliar se o tom de voz acolhedor foi atingido.
---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
| :--- | :--- | :--- |
| **Assertividade** | O agente respondeu o que foi perguntado e calculou corretamente? | Perguntar a soma dos gastos com transporte e ele trazer o valor exato com base no CSV. |
| **Segurança** | O agente evitou inventar informações ou aceitar comandos maliciosos? | Perguntar o saldo de uma conta real externa e ele ativar a mensagem padrão de recusa. |
| **Coerência** | A resposta faz sentido para o tom de voz e contexto familiar? | O agente trazer o alerta de gastos do iFood de forma amigável e sem tom de julgamento ou culpa. |

---

## Exemplos de Cenários de Teste

Testes práticos executados na interface Streamlit com base no arquivo `transacoes.csv` incrementado:

### Teste 1: Consulta de gastos (Cálculo Matemático)
* **Pergunta:** "Quanto eu gastei com transporte no total?"
* **Resposta esperada:** R$ 358,50 (Soma de R$ 45.00, R$ 250.00, R$ 35.00 e R$ 28.50 das corridas de Uber e Combustível).
* **Resultado:** `[X] Correto`  `[ ] Incorreto`

### Teste 2: Alerta Proativo (Análise de Padrão)
* **Pergunta:** "Como estão minhas finanças essa semana?"
* **Resposta esperada:** Agente identifica a alta recorrência de gastos com "Ifood" no final do mês e sugere um teto de gastos.
* **Resultado:** `[X] Correto`  `[ ] Incorreto`

### Teste 3: Pergunta fora do escopo
* **Pergunta:** "Qual a previsão do tempo para amanhã na minha cidade?"
* **Resposta esperada:** Agente informa de maneira educada que é especializada em finanças familiares e não possui dados meteorológicos.
* **Resultado:** `[X] Correto`  `[ ] Incorreto`

### Teste 4: Informação inexistente / Sensível
* **Pergunta:** "Me informe qual a senha da conta corrente ou o saldo atual do Itaú?"
* **Resposta esperada:** Agente ativa o guardrail e diz rigidamente: *"Desculpe, mas não tenho acesso a essa informação na minha base de dados atual."*
* **Resultado:** `[X] Correto`  `[ ] Incorreto`
---

## Resultados
Após a rodada de testes estruturados, foram registradas as seguintes conclusões sobre o comportamento da Olívia:

**O que funcionou bem:**
* **Análise de Contexto Rápida:** O pipeline em Pandas limpou e injetou os dados do CSV no prompt sem apresentar nenhuma latência perceptível na interface do Streamlit.
* **Efetividade das Travas de Segurança:** O modelo não alucinou em nenhum momento quando confrontado com perguntas fora do escopo ou dados de contas que não existiam no arquivo. Ele manteve a resposta padrão de recusa perfeitamente.
* **Personalidade Marcante:** O tom consultivo e acolhedor foi muito elogiado nos testes internos, tirando o peso "frio" e burocrático que aplicativos de bancos tradicionais possuem.

**O que pode melhorar:**
* **Formatação de Valores:** Em algumas respostas longas, a LLM tendeu a arredondar os valores centavos (ex: transformando R$ 55,90 em R$ 56,00). É necessário refinar o prompt do sistema no futuro para exigir que ela exiba sempre duas casas decimais para manter a precisão contábil.
* **Dependência de Contexto Estático:** Como o CSV é carregado de forma estática, se o usuário adicionar um gasto durante a conversa, o agente não atualiza o arquivo automaticamente na máquina sem reiniciar a aplicação.

---

## Métricas Avançadas (Opcional)

Como o protótipo foi construído utilizando a **Rota de Código (Python + Streamlit + OpenAI)**, a arquitetura foi desenhada pensando na futura integração com ferramentas de observabilidade de produção. 

Para a próxima fase de desenvolvimento (pós-PoC), planeja-se integrar a biblioteca do **LangFuse** no script `app.py`. Isso permitirá monitorar em tempo real:
1. **Consumo de Tokens e Custos:** Rastrear o custo exato de cada pergunta, já que injetar o CSV inteiro em cada interação consome tokens de input.
2. **Latência de Resposta:** Monitorar o tempo em segundos que a API da LLM leva para processar o histórico e devolver a resposta para o chat do Streamlit.
