# 📄 Chat with a PDF using RAG
This is a **Streamlit** app that allows you to chat with a PDF file using an LLM and Retrieval Augmented Generation (RAG).  

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).

## Demo

https://github.com/user-attachments/assets/3db8e3af-3d4b-4d4a-b0ec-32d86f2b5e6d

## Features
- Upload a PDF file
- Ask questions about the content of the file
- Receive accurate answers using RAG

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/rag_apps/pdf_rag
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run pdf_rag.py
```

## How it works

- PDF file contents are loaded using **PyPDF2** and split into chunks.
- Embeddings are created and stored using **Chroma**.
- Relevant context is retrieved based on the user's query, then added to the LLM input message.
- A request containing the input message and context is sent to the Tenstorrent instance, which runs the LLM inference.
- The app receives the response and displays the generated text.
