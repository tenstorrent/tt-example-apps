from urllib.parse import urljoin

import requests
import streamlit as st
import pypdf
import chromadb


@st.cache_data
def get_available_models(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})
    return res


@st.cache_resource
def setup_chromadb():
    chroma = chromadb.Client()
    col = chroma.get_or_create_collection("pdf_rag")
    return col


def process_pdf(pdf, col):
    chunks = chunk(extract_text(pdf))

    # Clear DB if uploading new PDF file
    col_ids = col.get()["ids"]
    if col_ids:
        col.delete(ids=col_ids)

    col.add(documents=chunks, ids=[str(i) for i in range(len(chunks))])


def extract_text(pdf):
    return "".join(p.extract_text() for p in pypdf.PdfReader(pdf).pages)


def chunk(text, size=100, overlap=30):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size - overlap)]


def call_chat_completion(query, context, model_id, tt_base_url):
    system_message = {
        "role": "system",
        "content":
            f"""
            You are a helpful assistant. \n
            When answering user questions, use the provided information below to answer the user question accurately.\n
            Base your responses on the retrieved context, especially for summary or factual queries.\n
            Provide clear and concise answers.

            {context}
            """
    }

    user_message = {"role": "user", "content": query}

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


def main():
    st.title("📄 PDF RAG")
    st.caption("Chat with a PDF using LLM + RAG")

    col = setup_chromadb()

    tt_base_url = st.text_input(
        "Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        # Fetch available models from Tenstorrent instance
        model_id_response = get_available_models(tt_base_url)

        if model_id_response.status_code != 200:
            st.write("Error fetching model names from instance.")
            model_id = st.text_input("Enter the name of the model")
        else:
            available_models = [m['id'] for m in model_id_response.json()['data']]

            model_id = st.selectbox(
                "Select the LLM to use.",
                available_models,
                help=f"These are the available models on {tt_base_url}"
            )

        # PDF upload
        pdf = st.file_uploader("Upload a PDF", type="pdf")

        if "pdf_processed" not in st.session_state:
            st.session_state['pdf_processed'] = False
            st.session_state['last_filename'] = None

        if pdf:
            if pdf.name != st.session_state['last_filename']:
                st.session_state['pdf_processed'] = False
                st.session_state['last_filename'] = pdf.name

            if not st.session_state['pdf_processed']:
                with st.spinner("🗂️ Processing PDF..."):
                    process_pdf(pdf, col)
                    st.session_state['pdf_processed'] = True
                    st.session_state['query_input'] = ""
                st.success("PDF indexed!")

            # User question
            query = st.text_input("Ask a question about the PDF", key='query_input')
            if query:
                with st.spinner("💬 Generating answer..."):
                    docs = col.query(query_texts=[query], n_results=3)['documents'][0]
                    context = "\n".join(docs)

                    response = call_chat_completion(query, context, model_id, tt_base_url)

                    st.markdown("**Answer:**")
                    st.write(response)


if __name__ == "__main__":
    main()
