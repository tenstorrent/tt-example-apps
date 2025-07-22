# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
import json
import os

from openai import OpenAI
import requests


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
    """
    1. Define tools in JSON schema
    2. Create user and system messages
    3. Call completion to get tool call parameters
    4. Run function with tool call parameters
    5. Give tool call and tool output back to model as context
    6. Run final chat completion for final response.
    """
    tt_base_url = os.environ["TT_BASE_URL"]  # "https://<...>.koyeb.app/v1"

    client = OpenAI(base_url=tt_base_url, api_key="null")
    models = client.models.list()
    model_id = models.data[0].id

    tools = [{
        "type": "function",
        "function": {
            "name": "fetch_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string", 
                        "description": "The city, region, or place, like 'Austin', 'New York City', or 'Barcelona'"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }]

    user_message = {
        "role": "user", 
        "content": "I'm going to Anchorage, how should I dress?"
    }

    system_message = {
        "role": "system",
        "content":
            """
            You are a helpful assistant that gives practical outfit recommendations based on the current weather conditions provided.\n
            When given details like temperature, rain, wind, and other weather factors, suggest appropriate clothing items and accessories for comfort.\n
            Keep your suggestions concise, relevant, and user-friendly.\n
            Example:
            - "It's cold and windy, wear a warm coat and a scarf."
            - "Expect rain, bring an umbrella and wear waterproof shoes."
            You must repeat the weather data so the user knows the exact forecast.
            """
    }

    tool_call_response = client.chat.completions.create(
        model=model_id,
        messages=[system_message, user_message],
        tools=tools,
        tool_choice="auto"
    )

    tool_call = tool_call_response.choices[0].message.tool_calls[0]

    parameters = json.loads(tool_call.function.arguments)

    print(f"[TOOL CALL] Parameters: {parameters}")

    context = fetch_weather(**parameters)

    print(f"[TOOL CALL] Output: {context}")

    assistant_message = {
        "role": "assistant",
        "tool_calls": [{
            "id": tool_call.id,
            "type": "function",
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }
        }]
    }

    tool_call_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": context
    }

    messages = [system_message, user_message, assistant_message, tool_call_message]

    stream = client.chat.completions.create(
        model=model_id,
        messages=messages,
        stream=True
    )

    print("Generating final response...\n")

    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)


if __name__ == "__main__":
    main()
