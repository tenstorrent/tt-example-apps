from urllib.parse import urljoin

import streamlit as st
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings


@st.cache_data
def get_available_models(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})
    return res


def load_webpage(url):
    loader = WebBaseLoader(url)
    return loader.load()


def split_documents(docs, chunk_size=500, overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap, separators=["\n\n", "\n", ".", " ", ""])
    return splitter.split_documents(docs)


def create_vectorstore(splits):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return Chroma.from_documents(documents=splits, embedding=embeddings)


def combine_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def call_chat_completion(question, context):
    system_message = {
        "role": "system",
        "content":
            f"""
            You are a helpful assistant. \n
            When answering user questions, use the provided information below to answer the user question accurately.\n
            Base your responses on the retrieved context, especially for summary or factual queries.\n
            If the context does not contain the answer, respond honestly that you do not know.

            {context}
            """
    }
    user_message = {"role": "user", "content": question}

    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "messages": [system_message, user_message],
        "max_tokens": 200
    }

    CHAT_ENDPOINT = "/v1/chat/completions"
    res = requests.post(urljoin(tt_base_url, CHAT_ENDPOINT), headers=headers, json=payload)

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
st.caption(f"Chat with a webpage using LLM + RAG")

tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

if tt_base_url:
    model_id_response = get_available_models(tt_base_url)  # Model names will be fetched from Tenstorrent instance

    if model_id_response.status_code != 200:
        st.write("Error fetching model name from instance.")
        model_id = st.text_input("Enter the name of the model")
    else:
        available_models = [m['id'] for m in model_id_response.json()['data']]
        model_id = st.selectbox("Select the LLM to use.", available_models, help=f"These are the available models on {tt_base_url}")

    webpage_url = st.text_input("Enter Webpage URL")

    if webpage_url:
        docs = load_webpage(webpage_url)
        splits = split_documents(docs)
        vectorstore = create_vectorstore(splits)
        st.success(f"Loaded {webpage_url} successfully!")

        question = st.text_input("Ask a question about the webpage.")
        if question:
            response = answer_question(vectorstore, question)
            st.write(response)
