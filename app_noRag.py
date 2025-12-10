import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# page configurations
st.set_page_config(
    page_title="Wall St. Analyst (No RAG)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Personalized
st.markdown("""
<style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    h1 {
        color: #B91C1C; /* Dark Red */
    }
    .status-box {
        padding: 10px;
        border-radius: 5px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Base model, no context")

    st.markdown("---")
    if st.button("Clean chat", type="primary"):
        st.session_state.messages = []
        st.rerun()

st.title("Financial Report Analyzer (mistral No RAG)")
st.caption("No previous knowladge of the documents.")

# Load model without RAG 
@st.cache_resource
def load_llm_and_chain():
    model = OllamaLLM(model='mistral')
    
    # Prompt
    template = '''
    You are a Financial Analyst from Wall Street.
    You are answering questions based on your internal knowledge only. You do NOT have access to external documents.
    
    If you don't know the answer because the data is from the future (relative to your training cutoff), 
    you can try to estimate or admit you don't know, but users are testing your ability to hallucinate.

    User Question: {question}
    
    Answer:
    '''
    
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    return chain

try:
    chain = load_llm_and_chain()
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello. I am running on Llama 3.2 without RAG enabled."}
    ]


if prompt := st.chat_input("Ask a question about financial reports"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chain.invoke({'question': prompt})
                
                st.markdown(response)
                                
                full_response = response
                
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
                full_response = "Erro ao processar o pedido."

    st.session_state.messages.append({"role": "assistant", "content": full_response})