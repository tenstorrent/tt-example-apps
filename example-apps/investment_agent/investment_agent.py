from urllib.parse import urljoin

import streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools
import requests


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


def main():
    st.title("📈 AI Investment Agent")
    st.caption("This app allows you to generate detailed reports based on a company's income statement.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.info(f"Using model {model_id}", icon="✅")

        assistant = Agent(
            model=OpenAILike(id=model_id, api_key="null", base_url=urljoin(tt_base_url, "v1")),
            tools=[
                YFinanceTools(income_statements=True)
            ],
            description="You are an expert investment analyst that analyzes company income statements.",
            instructions=[
                "Retrieve the company's income statement, then base your response off that information.",
                "Format your response using markdown and use tables to display data where possible."
            ],
            stream_intermediate_steps=True,
            show_tool_calls=True
        )

        stock = st.text_input("Enter stock symbol (e.g. AAPL)")

        if stock:
            query = f"Make a detailed report for an investor trying to invest in {stock}."
            with st.spinner("🔍 Analyzing..."):
                response_stream = assistant.run(query, stream=True)
                response_text = ""
                report_placeholder = st.empty()

                for chunk in response_stream:
                    response_text += chunk.content
                    report_placeholder.markdown(response_text + "▌")

                report_placeholder.markdown(response_text)


if __name__ == "__main__":
    main()
