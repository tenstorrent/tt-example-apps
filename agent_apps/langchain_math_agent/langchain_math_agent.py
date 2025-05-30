from urllib.parse import urljoin

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import streamlit as st
import requests


@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b


@tool
def divide(a: int, b: int) -> int:
    """Divide a and b."""
    return a / b


@tool
def add(a: int, b: int) -> int:
    """Add a and b."""
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract a and b."""
    return a - b


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


def main():
    st.title("➗ LangChain Math Agent")
    st.caption("Ask in natural language to add, subtract, multiply, or divide two numbers.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.info(f"Using model: {model_id}", icon="✅")

        example_str = "What is 12,852 divided by 4,284?"  # 3
        user_query = st.text_input(label="Ask for an operation on two numbers.", placeholder=example_str)
        if user_query:
            model = ChatOpenAI(
                model=model_id,
                base_url=urljoin(tt_base_url, "v1"),
                api_key="null"
            )

            tools = [multiply, divide, add, subtract]
            agent = create_react_agent(model, tools)

            with st.spinner("🤖 Running agent with tools..."):
                agent_response = agent.invoke({"messages": HumanMessage(user_query)})
                st.markdown(f"**Agent response:** {agent_response['messages'][-1].content}\n\n")
            
            with st.spinner("💬 Running model without tools..."):
                model_response = model.invoke(user_query)
                st.markdown(f"**Model response (no tools)**: {model_response.content}")


if __name__ == "__main__":
    main()
