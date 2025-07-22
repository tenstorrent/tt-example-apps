# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
import json
import os

from openai import OpenAI
import requests


def fetch_weather(location):
    """Function to fetch current forecasts from weatherAPI."""

    # The commented code below is for demonstrating if the agent's iterative process works.
    # A simple test is to add the state to the end of the city.
    # For example set the user query to: 'I'm going to Anchorage, Alaska, how should I dress?'
    # The agent should fail, then retry again with fetch_weather(location="Anchorage")
    # -------------------------------------------------------------------------------
    # valid_locations = ["Anchorage", "Chicago", "Los Angeles"]
    # if location not in valid_locations:
    #     raise ValueError(f"Invalid location. Location must be in {valid_locations}. Do not include the state. Call 'fetch_weather' again without the state name.")
    # -------------------------------------------------------------------------------

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
            Examples:
            - "It's cold and windy, wear a warm coat and a scarf."
            - "Expect rain, bring an umbrella and wear waterproof shoes."
            You must repeat the weather data so the user knows the exact forecast.
            """
    }

    # Number of times to let agent try to fix itself
    retries = 5

    messages = [system_message, user_message]

    for turn in range(retries):
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        msg = response.choices[0].message

        try:
            tool_call = msg.tool_calls[0]
            parameters = json.loads(tool_call.function.arguments)

            print(f"[TOOL CALL] Parameters: {parameters}")

            # Handle getting parameters and calling functions manually
            tool_output = fetch_weather(**parameters)
            print(f"[TOOL CALL] Output: {tool_output}")

            # Append tool call and tool result to message history
            messages.append({
                "role": "assistant",
                "tool_calls": [{
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }]
            })

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output
            })

            # Stream final answer
            print("[INFO] Generating final response...\n")
            stream = client.chat.completions.create(
                model=model_id,
                messages=messages,
                stream=True
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                print(delta, end="", flush=True)

            return  # Successful exit

        except Exception as e:
            if 'tool_call' in locals() and tool_call is not None:
                # Tool call failed. Provide feedback so agent can retry
                print(f"[ERROR] Tool failed: {e}")

                messages.append({
                    "role": "assistant",
                    "tool_calls": [{
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    }]
                })

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"Tool execution failed: {str(e)}"
                })
            else:
                # No tool was called
                messages.append({
                    "role": "tool",
                    "content": f"Tool execution failed: {str(e)}. You must call the 'fetch_weather' function to get the forecast."
                })


if __name__ == "__main__":
    main()
