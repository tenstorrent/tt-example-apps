from urllib.parse import urljoin

from openai import OpenAI
import streamlit as st


def main():
    st.title("🤖 Streaming Chatbot with Memory")

    if "tt_base_url" not in st.session_state:
        st.session_state.tt_base_url = ""

    st.session_state.tt_base_url = st.text_input(
        "Enter the public URL of your Tenstorrent instance on Koyeb.",
        value=st.session_state.tt_base_url
    )

    if st.session_state.tt_base_url:
        client = OpenAI(base_url=urljoin(st.session_state.tt_base_url, "v1"), api_key="null")

        if "model_id" not in st.session_state:
            models = client.models.list()
            st.session_state.model_id = models.data[0].id

        st.info(f"Using model: {st.session_state.model_id}", icon="✅")

        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if user_query := st.chat_input("Ask anything"):
            st.session_state.messages.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.markdown(user_query)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state.model_id,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
