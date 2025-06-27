# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
import asyncio
import os
import json
from urllib.parse import urljoin

import requests
import streamlit as st
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool


@st.cache_data
def get_model_id(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})

    if res.status_code != 200:
        st.error("Error fetching model name from instance.", icon="🚨")
    else:
        return res.json()['data'][0]['id']


@function_tool
def exchange_rates(currency):
    """
    Get the latest conversion rates for the given base currency.

    Args:
        currency (str): The base currency code (e.g. 'USD', 'JPY', 'EUR').

    Returns:
        dict: A mapping of other currency codes to their conversion rate from the base.
    """
    api_key = os.environ["EXCHANGE_RATE_API_KEY"]
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"

    response = requests.get(url)

    conversion_rates = json.loads(response.content)['conversion_rates']
    
    return conversion_rates


async def run_agent(agent, user_query):
    result = await Runner.run(agent, user_query)
    return result.final_output


def main():
    st.title("💱 Exchange Rate Agent")
    st.caption("Ask in natural language about exchange rates between currencies.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    if tt_base_url:
        model_id = get_model_id(tt_base_url)
        st.info(f"Using model: {model_id}", icon="✅")

        user_query = st.text_input("Ask a question about exchange rates.", placeholder="What is 1,000 USD worth in JPY?")

        if user_query:
            custom_client = AsyncOpenAI(base_url=urljoin(tt_base_url, "v1"), api_key="null")
            set_tracing_disabled(True)

            agent = Agent(
                name="Exchange Rate Agent",
                model=OpenAIChatCompletionsModel(model=model_id, openai_client=custom_client),
                tools=[exchange_rates],
                instructions="""
                    You provide help with currency exchange rates.
                    You must call the 'exchange_rates' function to get recent conversion rates for a single currency.
                    When responding to the user, include the exact conversion value from 1 unit of the base currency to the target
                    in the format: '<base> 1 = <target> <rate>'.
                    Use that to explain the answer to the user's query.
                """
            )

            with st.spinner("🤖 Running agent..."):
                response = asyncio.run(run_agent(agent, user_query))

                st.markdown(response)


if __name__ == "__main__":
    main()
