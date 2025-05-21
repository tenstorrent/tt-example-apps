from urllib.parse import urljoin
import json
import re

from openai import OpenAI
import requests
import streamlit as st


@st.cache_data
def get_available_models(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})
    return res


def get_weather(location, unit, api_key):
    params = {
        "q": location,
        "key": api_key
    }
    base_url = "http://api.weatherapi.com/v1/current.json"
    res = requests.get(base_url, params=params)
    data = res.json()
    current_data = data['current']

    if unit == "celsius":
        temp_string = f"{current_data['temp_c']} °C"
    else:
        temp_string = f"{current_data['temp_f']} °F"
    
    condition_string = current_data['condition']['text']
    location_string = f"{data['location']['name']}, {data['location']['region']}"

    return f"Weather in {location_string}: {temp_string}, {condition_string}"


def main():
    st.title("🌦️ Weather Agent")
    st.caption("Get clothing recommendations based on live weather forecasts in a specific area.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")
    if tt_base_url:
        model_name_response = get_available_models(tt_base_url)

        if model_name_response.status_code != 200:
            st.write("Error fetching model names from instance.")
            model_name = st.text_input("Enter the name of the model")
        else:
            available_models = [m['id'] for m in model_name_response.json()['data']]

            model_name = st.selectbox(
                "Select the LLM to use.",
                available_models,
                help=f"These are the available models on {tt_base_url}"
            )
        
        weather_api_key = st.text_input("Enter your Weather API key.", type="password")
        if weather_api_key:
            openai_api_key = st.text_input("Enter your OpenAI API key.", type="password")
            if openai_api_key:
                client = OpenAI(base_url=urljoin(tt_base_url, "v1"), api_key=openai_api_key)

                tools = [{
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string", 
                                    "description": "The city, region, or place, like 'Austin, TX', 'New York City', or 'Barcelona'"
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                    "description": "The standard unit of temperature measurement used in the location."
                                }
                            },
                            "required": ["location", "unit"],
                            "additionalProperties": False
                        }
                    }
                }]

                user_query = st.text_input("Ask for the weather in a specific location (i.e. What's the weather like in Anchorage in Fahrenheit?)")
                if user_query:
                    with st.spinner("💬 Calling function to extract search parameters..."):
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=[{"role": "user", "content": user_query}],
                            tools=tools,
                            tool_choice={"type": "function", "function": {"name": "get_weather"}}
                        )
                    st.success("✅ Retrieved response.")

                    tool_call = response.choices[0].message.tool_calls[0]
                    cleaned_args = json.loads(re.sub(r"<\|.*?\|>", "", tool_call.function.arguments).strip())
                    parameters = cleaned_args['parameters']

                    with st.spinner("🌦️ Getting real-time weather data..."):
                        context = get_weather(parameters['location'], parameters['unit'], weather_api_key)
                    st.success(context)

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
                            Avoid repeating the weather data; focus on actionable advice.
                            """
                    }

                    user_message = {"role": "user", "content": user_query}
                    tool_call_message = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": context
                    }

                    with st.spinner("💬 Generating final answer..."):
                        res = client.chat.completions.create(
                            model=model_name,
                            messages=[system_message, user_message, tool_call_message]
                        )

                        final_response = json.loads(res.to_json())['choices'][0]['message']['content'].strip()

                    st.success("✅ Done!")
                    st.write(final_response)


if __name__ == "__main__":
    main()
