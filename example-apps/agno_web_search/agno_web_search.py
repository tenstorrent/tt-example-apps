from urllib.parse import urljoin
import requests

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


def main():
    st.title("🔎 Web Search Agent")
    st.caption("Use an Agno agent to retrieve search results on a query.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")
    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.write("Using model:", model_id)

        user_query = st.text_input("Search for anything")
        if user_query:
            agent = Agent(
                model=OpenAILike(id=model_id, api_key="null", base_url=urljoin(tt_base_url, "v1")),
                tools=[DuckDuckGoTools()],
                instructions=[
                    "You are a helpful assistant.",
                    "Search the web for real-time information."
                ],
                markdown=True
            )

            with st.spinner("🔍 Searching the web for the latest information..."):
                response = agent.run(user_query)
                st.write(response.content)


if __name__ == "__main__":
    main()
