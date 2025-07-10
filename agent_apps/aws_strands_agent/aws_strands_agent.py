# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import file_read
import streamlit as st
import requests

from urllib.parse import urljoin


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


def main():
    st.title("AWS Strands Agent")
    st.caption("Ask questions about the contents of a file.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.info(f"Using model: {model_id}", icon="✅")

        user_query = st.text_input("Ask about the contents of a file.", placeholder="Read example_env.txt and tell me what version of PyTorch is used")

        if user_query:
            with st.spinner("💬 Reading file and thinking..."):
                model = OpenAIModel(
                    client_args={
                        "api_key": "null",
                        "base_url": urljoin(tt_base_url, "v1")
                    },
                    model_id=model_id
                )

                agent = Agent(
                    model=model, 
                    tools=[file_read]
                )

                response = agent(user_query)

                st.markdown(response)


if __name__ == "__main__":
    main()
