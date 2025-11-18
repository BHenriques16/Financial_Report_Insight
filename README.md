# **📄 Document QA com Arquitetura RAG (Retrieval-Augmented Generation)**

**Processamento de Linguagem Natural (PLN)** **Universidade da Beira Interior (UBI)** **Ano Letivo:** 2025/2026

## **📋 Sobre o Projeto**

Este repositório contém a implementação de um sistema de **Question Answering (QA)** sobre documentos não estruturados, desenvolvido como trabalho final para a unidade curricular de Processamento de Linguagem Natural.

O objetivo principal foi criar uma aplicação robusta capaz de ultrapassar as limitações de contexto dos LLMs tradicionais, utilizando uma arquitetura **RAG (Retrieval-Augmented Generation)**. O sistema ingere documentos técnicos longos (ex: relatórios financeiros, manuais técnicos, artigos científicos), fragmenta-os e permite que o utilizador interaja com os mesmos através de linguagem natural, com garantia de rastreabilidade da informação (citação de fontes).

### **🚀 Funcionalidades Principais**

* **Ingestão de Múltiplos Documentos:** Suporte para leitura e processamento em lote de ficheiros PDF.  
* **Vetorização Persistente:** Criação de uma base de dados vetorial (Vector Store) local para evitar o reprocessamento de dados.  
* **LLM 100% Local:** Utilização de modelos Open Source (Llama 3.2 ou Mistral) via Ollama, garantindo privacidade dos dados.  
* **Interface Interativa:** Aplicação web desenvolvida em Streamlit com chat histórico e gestão de contexto.  
* **Prevenção de Alucinações:** O sistema indica explicitamente o documento e o número da página de onde a resposta foi extraída.

## **🛠️ Stack Tecnológica**

O projeto foi desenvolvido em **Python** utilizando as seguintes bibliotecas e ferramentas:

| Componente | Tecnologia | Descrição |
| :---- | :---- | :---- |
| **LLM Server** | [Ollama](https://ollama.com/) | Execução local de modelos Llama/Mistral. |
| **Orquestração** | [LangChain](https://www.langchain.com/) | Framework para ligar o LLM aos dados. |
| **Vector Store** | [ChromaDB](https://www.trychroma.com/) | Base de dados para armazenamento de embeddings. |
| **Embeddings** | mxbai-embed-large | Modelo de vetorização de texto de alto desempenho. |
| **Interface** | [Streamlit](https://streamlit.io/) | Frontend para interação com o utilizador. |
| **PDF Parsing** | pypdf | Extração de texto e metadados dos ficheiros. |

## **⚙️ Instalação e Configuração**

### **1\. Pré-requisitos**

Certifique-se de que tem instalado:

* Python 3.8 ou superior.  
* [Ollama](https://ollama.com/) (para correr o modelo localmente).

### **2\. Configuração do Modelo (Ollama)**

No seu terminal, descarregue os modelos necessários:

\# Modelo de Linguagem (Chat)  
ollama pull llama3.2

\# Modelo de Embeddings (Vetorização)  
ollama pull mxbai-embed-large

### **3\. Instalação de Dependências**

Recomenda-se a criação de um ambiente virtual. Instale as bibliotecas Python necessárias:

pip install langchain langchain-community langchain-ollama langchain-chroma streamlit pypdf

## **💻 Como Utilizar**

O fluxo de trabalho divide-se em duas fases: **Ingestão de Dados** e **Interação**.

### **Passo 1: Preparação dos Dados (Ingestão)**

1. Coloque os seus ficheiros PDF na pasta data/.  
2. Execute o script de vetorização. Este script irá ler os documentos, dividir o texto em fragmentos (chunks) e guardar os embeddings no ChromaDB.

python vector.py

*Nota: Execute este passo apenas na primeira vez ou sempre que adicionar novos documentos à pasta data.*

### **Passo 2: Executar a Aplicação**

Inicie a interface web Streamlit:

streamlit run app.py

A aplicação ficará disponível no seu navegador em http://localhost:8501.

## **📂 Estrutura do Repositório**

.  
├── data/                     \# Diretório para colocar os ficheiros PDF de entrada  
├── chroma\_db\_financas/       \# Base de dados vetorial (gerada automaticamente)  
├── vector.py                 \# Script de pipeline ETL (Extract, Transform, Load)  
├── app.py                    \# Aplicação principal (Frontend Streamlit \+ RAG Chain)  
└── README.md                 \# Documentação do projeto

## **🧩 Detalhes de Implementação**

### **Estratégia de Chunking**

Para lidar com documentos extensos, foi utilizado o RecursiveCharacterTextSplitter com:

* **Chunk Size:** 1500 caracteres (otimizado para capturar tabelas financeiras e parágrafos completos).  
* **Overlap:** 300 caracteres (para manter o contexto semântico entre cortes).

### **Recuperação (Retrieval)**

Utiliza-se o algoritmo **MMR (Maximal Marginal Relevance)** na recuperação de documentos para garantir diversidade nas fontes citadas e evitar que um único documento domine a janela de contexto do LLM.

## **👤 Autor**

**Nome do Aluno** Número de Aluno: XXXXX

Engenharia Informática / Ciência de Dados

Universidade da Beira Interior