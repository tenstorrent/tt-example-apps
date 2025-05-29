from urllib.parse import urljoin

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import streamlit as st
import requests


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


def main():
    st.title("⛓️ LangChain Search Agent")
    st.caption("Ask questions and have an agent search the web.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.info(f"Using model: {model_id}", icon="✅")

        model = ChatOpenAI(
            model=model_id,
            base_url=urljoin(tt_base_url, "v1"),
            api_key="null"
        )

        search = TavilySearchResults(max_results=2)
        tools = [search]
        agent_executor = create_react_agent(model, tools)

        config = {"configurable": {"thread_id": "abc123"}}

        user_query = st.text_input("Ask anything")
        if user_query:
            user_message = [HumanMessage(content=user_query)]

            with st.spinner("💬 Researching and thinking..."):
                for step in agent_executor.stream({"messages": user_message}, config, stream_mode="values"):
                    message = step["messages"][-1]
                    content = message.content
                    message_type = message.type.upper()
                    if content:
                        st.markdown(f"**{message_type}:** {content}")


if __name__ == "__main__":
    main()
