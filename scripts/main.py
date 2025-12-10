from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever

# model definition
model = OllamaLLM(model='llama3.2') 

# Financial Analyst prompt
template = '''
You are a Tech Investment Skeptic and Financial Analyst. 
Your goal is to investigate the "AI Bubble" hypothesis by analyzing the provided 10-Q reports.

Focus on:
1. Capital Expenditures (CapEx): massive spending on servers/infrastructure.
2. Cloud Revenue Growth: Is Azure (Microsoft) or Google Cloud growing faster?
3. AI Monetization: Specific mentions of revenue from "Copilot" or "Gemini".

Warning: Microsoft's "Q1 FY26" corresponds to the same calendar period as Alphabet's "Q3 2025" (both quarter ending Sept 30). Treat them as comparable.

Here is the context: {context}

here is the user Question: {question}
Answer:
'''

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# iniciate the retriver (RAG logic)
retriever = get_retriever() 

# Interaction loop
while True:
    print('\n' + '='*50)
    question = input('Ask your question to the Financial Analyst (q to quit): ')
    
    if question.lower() == 'q':
        break
    
    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)
    
    # Preparing the text for the LLM (combining the content of the chunks)
    formatted_context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # Generate ansewr
    response = chain.invoke({'context': formatted_context, 'question': question})
    
    print(f"\nAnswer:\n\n{response}")
    
    # Showing the source of the information
    unique_sources = set()
    for doc in retrieved_docs:
        source_name = doc.metadata.get('source', 'Unknown').split('/')[-1] # Just grabs the filename.
        page_num = doc.metadata.get('page', '?')
        # Creates a unique string to avoid repeating the same source multiple times.
        source_info = f" {source_name} (Page. {int(page_num) + 1})"
        unique_sources.add(source_info)
    
    for source in unique_sources:
        print(source)