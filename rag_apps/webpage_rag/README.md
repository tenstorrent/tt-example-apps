# 🌐 Chat with a webpage using RAG
This is a **Streamlit** app that allows you to chat with any public webpage using an LLM and Retrieval Augmented Generation (RAG).  

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).

## Demo

https://github.com/user-attachments/assets/325570dc-8a95-4b6c-a5e9-75ce76037a0c

## Features
- Input a webpage URL
- Ask questions about the content of the webpage
- Receive accurate answers using RAG

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/rag_apps/webpage_rag
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run webpage_rag.py
```

## How it works

- The app loads the webpage data using **WebBaseLoader** and splits it into chunks using **RecursiveCharacterTextSplitter**.
- It creates **Ollama** embeddings and a vector store using **Chroma**.
- The app sets up a RAG (Retrieval-Augmented Generation) chain, which retrieves relevant documents based on the user's question.
- The langauge model is called to generate an answer using the retrieved context.
- The app displays the answer to the user's question.
