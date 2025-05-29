from urllib.parse import urljoin
import json
import re

import requests
import serpapi
import streamlit as st


@st.cache_data
def get_available_models(base_url):
    res = requests.get(urljoin(base_url, "/v1/models"), headers={"accept": "application/json"})
    return res


def search_web(query, location, api_key):
    search_response = serpapi.search(q=query, engine="google_local", location=location, serp_api_key=api_key)
    return search_response['local_results']


def call_tool_completion(endpoint, payload):
    return requests.post(
        endpoint,
        headers={"Content-Type": "application/json"},
        json=payload
    )


def call_final_response(user_query, endpoint, model_id, context, tool_call):
    system_message = {
        "role": "system",
        "content":
            """
            You are a helpful assistant that takes a user's travel-related query (such as 'coffee shops in Austin, TX')\n
            and uses structured search results to generate a useful and accurate response.\n
            You will be provided with search context, including titles, addresses, ratings, and short descriptions of relevant places.\n
            They will be formatted in rows with the following schema: title ||| address ||| rating ||| description\n 
            Your goal is to summarize and recommend the most suitable options clearly and concisely.\n
            Prioritize clarity, accuracy, and helpfulness. Do not make up any places and do not mix fields from different rows.\n
            Use only the provided context. If no good results are available, say so clearly.
            """
    }

    user_message = {"role": "user", "content": user_query}
    tool_call_message = {
        "role": "tool",
        "tool_call_id": tool_call["id"],
        "content": context
    }

    payload = {
        "model": model_id,
        "messages": [system_message, user_message, tool_call_message],
        "max_tokens": 200
    }

    res = requests.post(endpoint, headers={"Content-Type": "application/json"}, json=payload)

    if res.status_code != 200:
        return f"Error: {res.status_code} - {res.text}"
    return res.json()["choices"][0]["message"]["content"].strip()


def get_search_tool():
    return {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for type of place the user is looking for and the location to search in.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What the user is looking for, like 'coffee shops', 'bookstores', 'pizza places'"
                    },
                    "location": {
                        "type": "string",
                        "description": "The city, region, or place to search in, like 'Austin, TX', 'New York City', or 'Barcelona'"
                    }
                },
                "required": ["query", "location"],
                "additionalProperties": False
            }
        }
    }


def get_tool_payload(model_id, user_query):
    search_tool = get_search_tool()

    tool_choice = {
        "type": "function",
        "function": {
            "name": "search_web"
        }
    }

    tool_payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": user_query}
        ],
        "tools": [search_tool],
        "tool_choice": tool_choice
    }

    return tool_payload


def main():
    st.title("🗺️ Travel Guide")
    st.caption("Ask for the best attractions in a city.")

    tt_base_url = st.text_input("Enter the public URL of your Tenstorrent instance on Koyeb.")

    CHAT_ENDPOINT = urljoin(tt_base_url, "/v1/chat/completions")

    if tt_base_url:
        model_id_response = get_available_models(tt_base_url)

        if model_id_response.status_code != 200:
            st.write("Error fetching model names from instance.")
            model_id = st.text_input("Enter the name of the model")
        else:
            available_models = [m['id'] for m in model_id_response.json()['data']]

            model_id = st.selectbox(
                "Select the LLM to use.",
                available_models,
                help=f"These are the available models on {tt_base_url}"
            )
        
        serp_api_key = st.text_input("Enter your SerpAPI API key.", type="password")

        if serp_api_key:
            user_query = st.text_input("Enter a query. (i.e. Find the best coffee shops in Austin, TX)")

            if user_query:
                with st.spinner("💬 Calling function to extract search parameters..."):
                    tool_payload = get_tool_payload(model_id, user_query)
                    tool_response = call_tool_completion(CHAT_ENDPOINT, tool_payload)
                st.success("✅ Retrieved response.")

                with st.spinner("📄 Parsing response..."):
                    tool_call = tool_response.json()['choices'][0]['message']['tool_calls'][0]
                    raw_args = tool_call['function']['arguments']
                    cleaned_args = re.sub(r"<\|.*?\|>", "", raw_args).strip()

                    parameters = json.loads(cleaned_args)['parameters']
                    query = parameters['query']
                    location = parameters['location']
                st.success("✅ Parsed parameters.")
                
                with st.spinner("🔎 Searching the web..."):
                    search_results = search_web(query, location, serp_api_key)

                    context = ""
                    for result in search_results:
                        title = result['title']
                        address = result['address']
                        rating = result['rating']
                        description = result['description']

                        context += f"{title} ||| {address} ||| {rating} stars ||| {description}\n"
                st.success("✅ Retrieved search results and prepared context!")

                with st.spinner("💬 Generating final answer..."):
                    final_response = call_final_response(user_query, CHAT_ENDPOINT, model_id, context, tool_call)
                    st.write(final_response)
                st.success("✅ Done!")


if __name__ == "__main__":
    main()
