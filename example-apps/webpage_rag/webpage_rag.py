from urllib.parse import urljoin

import streamlit as st
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


# Configuration
BASE_URL = ""
MODEL = "Qwen/Qwen2.5-7B-Instruct"


def load_webpage(url):
    loader = WebBaseLoader(url)
    return loader.load()


def split_documents(docs, chunk_size=500, overlap=10):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_documents(docs)


def create_vectorstore(splits):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(documents=splits, embedding=embeddings)


def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def call_chat_completion(question, context):
    prompt = f"Answer the question based on the context.\n\nContext:\n{context}\n\nQuestion: {question}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }

    CHAT_ENDPOINT = "/v1/chat/completions"
    res = requests.post(urljoin(BASE_URL, CHAT_ENDPOINT), headers=headers, json=payload)

    if res.status_code != 200:
        return f"Error: {res.status_code} - {res.text}"
    return res.json()["choices"][0]["message"]["content"].strip()


def answer_question(vectorstore, question):
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(question)
    context = combine_docs(docs)
    return call_chat_completion(question, context)


# Streamlit UI
st.title("Chat with Webpage 🌐")
st.caption(f"Chat with a webpage using {MODEL.split('/')[-1]} + RAG")

url = st.text_input("Enter Webpage URL")

if url:
    docs = load_webpage(url)
    splits = split_documents(docs)
    vectorstore = create_vectorstore(splits)
    st.success(f"Loaded {url} successfully!")

    question = st.text_input("Ask a question about the webpage.")
    if question:
        response = answer_question(vectorstore, question)
        st.write(response)
