# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
import os

from agno.team import Team
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools import tool
from agno.tools.wikipedia import WikipediaTools
import requests


@tool(show_result=True)
def fetch_weather(location: str) -> str:
    params = {
        "q": location,
        "key": os.environ["WEATHER_API_KEY"]
    }
    base_url = "http://api.weatherapi.com/v1/current.json"

    res = requests.get(base_url, params=params)
    data = res.json()
    current_data = data['current']

    temp_string = f"{current_data['temp_f']} °F"
    
    condition_string = current_data['condition']['text']
    location_string = f"{data['location']['name']}, {data['location']['region']}"

    return f"Weather in {location_string}: {temp_string}, {condition_string}.\n"


def main():
    tt_base_url = os.environ["TT_BASE_URL"]
    model_id = "meta-llama/Llama-3.1-8B-Instruct"

    weather_agent = Agent(
        name="Weather Agent",
        role="Expert at fetching current weather conditions.",
        model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
        tools=[fetch_weather],
        instructions=[
            "You are a helpful assistant that fetches current weather conditions for a location."
        ]
    )

    researcher = Agent(
        name="Researcher",
        role="Expert at finding information from Wikipedia",
        instructions=[
            "You are a helpful assistant that searches Wikipedia for information.",
            "Respond with the information retrieved from Wikipedia."
        ],
        tools=[WikipediaTools()],
        model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
    )

    agent_team = Team(
        name="Support Team",
        mode="route",
        model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
        members=[weather_agent, researcher],
        instructions=[
            "You are the leader of a team of specialized agents.",
            "When a user asks a question, your job is to choose the most appropriate teammate to handle it based on their skill.",
            "Do not answer the question yourself.",
            "Simply forward the task to the agent best suited to respond, and return their answer directly to the user."
        ],
        markdown=True,
        show_members_responses=True
    )

    # Example queries
    # user_query = "What's the weather in Boston?"  # Task should be given to Weather Agent
    user_query = "What happened in the 2025 NBA Finals?"  # Task should be given to Researcher

    agent_team.print_response(user_query, stream=True)


if __name__ == "__main__":
    main()
