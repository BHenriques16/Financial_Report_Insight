import streamlit as st
import time

# Importar a nossa lógica do outro ficheiro
from processing import (
    carregar_modelo_embeddings, 
    extrair_texto_pdf, 
    criar_base_vetorial,
    carregar_llm  # Continua a ser preciso
)

# --- A IMPORTAÇÃO QUE FALHAVA (RetrievalQA) FOI REMOVIDA ---
# --- Esta importação (PromptTemplate) FUNCIONAVA e é necessária ---
from langchain_core.prompts import PromptTemplate

# --- 1. Configuração da Página ---
st.set_page_config(
    page_title="Document-QA",
    page_icon="📄",
    layout="wide"
)

# --- 2. Título Principal ---
st.title("✅ Document-QA (Versão Manual - Plano B)") # Mudei o título para sabermos que está atualizado
st.markdown("""
Bem-vindo ao Document-QA. 
Esta aplicação permite-lhe carregar um documento PDF e fazer perguntas sobre o seu conteúdo.
""")

# --- 3. Barra Lateral (Sidebar) para Upload ---
# (Esta secção é IDÊNTICA à anterior)
with st.sidebar:
    st.header("O seu Documento")
    uploaded_file = st.file_uploader(
        "Carregue o seu ficheiro .pdf aqui:", 
        type=["pdf"]
    )

    if "vector_db" not in st.session_state:
        st.session_state.vector_db = None
    if "llm" not in st.session_state: 
        st.session_state.llm = None

    if uploaded_file is not None:
        st.info(f"Ficheiro carregado: {uploaded_file.name}")
        
        if st.button("Processar Documento"):
            embeddings = carregar_modelo_embeddings()
            texto_documento = extrair_texto_pdf(uploaded_file)
            
            if texto_documento:
                st.session_state.vector_db = criar_base_vetorial(texto_documento, embeddings)
                st.session_state.llm = carregar_llm() 
                
                if st.session_state.vector_db and st.session_state.llm:
                    st.success("Documento processado e IA carregada. Pronto para perguntas!")
    else:
        st.warning("Por favor, carregue um documento PDF para começar.")


# --- 4. Área Principal de Chat ---
st.header("Faça uma Pergunta")

# (Esta secção é IDÊNTICA à anterior)
if st.session_state.vector_db is None or st.session_state.llm is None:
    st.info("Por favor, carregue e processe um documento na barra lateral para começar.")
    query = st.text_input(
        "Sobre o que quer saber?", 
        placeholder="Aguardando processamento do documento...",
        disabled=True,
        label_visibility="collapsed"
    )
else:
    query = st.text_input(
        "Sobre o que quer saber?", 
        placeholder="Escreva a sua pergunta aqui...",
        disabled=False,
        label_visibility="collapsed"
    )

# Espaço reservado para a Resposta
st.subheader("Resposta")
answer_container = st.container(border=True, height=200)

# Espaço reservado para as Fontes
st.subheader("Fontes do Documento")
source_container = st.container(border=True, height=250)

# --- NOVO (FASE 3 - MANUAL) ---
# Aqui está a nossa "outra maneira". Substituímos o RetrievalQA.
if query and st.session_state.vector_db and st.session_state.llm:
    
    with st.spinner("A pensar (com o Phi-3)..."):
        
        # 1. O Prompt (A Instrução) - MUITO MELHORADO
        # Este prompt encoraja a SÍNTESE, não a EXTRAÇÃO.
        template = """
        <|user|>
        Use os seguintes trechos de um documento para responder à pergunta.
        A sua resposta deve ser clara, concisa e escrita como um assistente prestável.
        Responda em Português.
        Se os trechos não contiverem a resposta, diga "Peço desculpa, mas não encontrei essa informação no documento."
        
        Contexto (Trechos do Documento):
        {context}
        
        Pergunta:
        {question}
        <|end|>
        <|assistant|>
        Resposta: 
        """
        PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
        
        # 2. O Retriever (O Pesquisador) - VOLTAMOS A K=3
        # O Phi-3 tem uma janela de 4k tokens, ele consegue aguentar mais contexto.
        retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": 3})

        # 3. Executar o "Retrieval" (Recuperação)
        docs = retriever.invoke(query)
        
        # 4. Formatar os Chunks de Contexto
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # 5. Formatar o Prompt Final
        prompt_final = PROMPT.format(context=context_text, question=query)
        
        # 6. Chamar o LLM (O Cérebro)
        resultado_bruto = st.session_state.llm.invoke(prompt_final)
        
        # 7. Limpar a Resposta (O Phi-3 pode repetir o prompt)
        # Precisamos de extrair apenas o texto depois do nosso "Resposta:"
        try:
            # O resultado pode incluir o prompt, vamos limpar
            if "<|assistant|>" in resultado_bruto:
                 # Encontra a nossa tag "Resposta:" e pega em tudo o que vem a seguir
                resultado_limpo = resultado_bruto.split("Resposta:")[1].strip()
            else:
                resultado_limpo = resultado_bruto
        except Exception as e:
            print(f"Erro ao limpar a resposta: {e}")
            resultado_limpo = resultado_bruto # Mostra a resposta bruta se a limpeza falhar

        
        # 8. Mostrar os Resultados
        answer_container.markdown(resultado_limpo)
        
        source_container.empty()
        for i, doc in enumerate(docs):
            source_container.markdown(f"**Fonte {i+1} (do Documento):**")
            source_container.info(f"_{doc.page_content}_")
            
elif not query:
    answer_container.write("A resposta do documento aparecerá aqui.")
    source_container.write("Os trechos do documento usados para a resposta aparecerão aqui.")