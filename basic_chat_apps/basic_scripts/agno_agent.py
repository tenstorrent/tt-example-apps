"""
This script demonstrates how to create an Agno agent that uses a custom function 
to retrieve context before responding.  In this example, the model will retrieve
current weather conditions in a location and use that information to recommend 
clothing.

The weather API used here is from https://www.weatherapi.com 
"""

import os

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools import tool
import requests

@tool(show_result=True)
def fetch_weather(location):
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
    tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
    model_id = "meta-llama/Llama-3.1-8B-Instruct"

    agent = Agent(
        model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
        tools=[fetch_weather],
        instructions=[
            "You are a helpful assistant that gives practical outfit recommendations based on the current weather conditions."
        ],
        markdown=True
    )

    user_query = "I'm going to Chicago, how should I dress?"

    agent.print_response(user_query, stream=True)


if __name__ == "__main__":
    main()
