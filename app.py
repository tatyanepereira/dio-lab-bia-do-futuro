import streamlit as st
import pandas as pd
from google import genai
from google.genai import types

# 1. Configuração da API do Gemini
# Substitua pelo seu token real gerado no Google AI Studio
API_KEY = ""
client = genai.Client(api_key=API_KEY)

# 2. Função para carregar a base de dados (CSV)
@st.cache_data
def carregar_historico_financeiro():
    try:
        df = pd.read_csv("transacoes.csv")
        return df.to_string(index=False)
    except FileNotFoundError:
        return "Erro: Arquivo transacoes.csv não encontrado na pasta."

dados_csv = carregar_historico_financeiro()

# 3. Engenharia de Prompt: Persona e Segurança (Anti-Alucinação)
PROMPT_SISTEMA = f"""
Você é a Olívia, uma consultora financeira familiar inteligente, acolhedora e proativa.
Seu papel é ajudar o usuário a analisar seus gastos e atingir suas metas de forma leve e educacional.

Aqui está o histórico real e atualizado de transações da família:
\"\"\"
{dados_csv}
\"\"\"

DIRETRIZES CRÍTICAS DE SEGURANÇA E COMPORTAMENTO:
1. Responda às perguntas do usuário baseando-se ESTREITAMENTE nas transações fornecidas no bloco de texto acima.
2. Se o usuário perguntar por dados, saldos de contas, investimentos específicos ou informações que NÃO estão explicitamente listados no texto acima, você deve responder rigidamente:
   "Desculpe, mas não tenho acesso a essa informação na minha base de dados atual."
3. Nunca invente nenhuma transação, valor, estabelecimento ou data. Não alucine.
4. Caso note que o usuário gastou muito com 'alimentacao' (várias compras de Ifood), faça um alerta amigável de forma proativa se ele perguntar como estão as finanças de forma geral.
"""

# 4. Configuração Visual da Interface (Streamlit)
st.set_page_config(page_title="Olívia - Inteligência Financeira", page_icon="💳")
st.title("💳 Olívia - Finanças Familiares")
st.markdown("---")

# Inicializa o histórico de mensagens na memória da sessão para o chat funcionar
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Renderiza o histórico de mensagens na tela (apenas usuário e modelo)
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Caixa de entrada para a pergunta do usuário
if pergunta_usuario := st.chat_input("Pergunte sobre seus gastos recentes..."):
    
    # Exibe a pergunta do usuário na tela
    with st.chat_message("user"):
        st.write(pergunta_usuario)
    st.session_state.chat_history.append({"role": "user", "content": pergunta_usuario})

    # Resposta da IA
    with st.chat_message("assistant"):
        resposta_placeholder = st.empty()
        
        try:
            # Configuração do prompt do sistema usando a estrutura do Gemini
            config = types.GenerateContentConfig(
                system_instruction=PROMPT_SISTEMA,
                temperature=0.3 # Baixa temperatura para evitar alucinações matemáticas
            )
            
            # Convertendo o histórico do Streamlit para o formato que o Gemini espera
            contents = []
            for m in st.session_state.chat_history:
                role_gemini = "user" if m["role"] == "user" else "model"
                contents.append(types.Content(role=role_gemini, parts=[types.Part.from_text(text=m["content"])]))
            
            # Chamada oficial utilizando o modelo estável e rápido Gemini 2.5 Flash
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=config
            )
            
            resposta_final = response.text
            resposta_placeholder.write(resposta_final)
            st.session_state.chat_history.append({"role": "model", "content": resposta_final})
            
        except Exception as e:
            st.error(f"Ocorreu um erro na chamada da API do Gemini: {e}")
