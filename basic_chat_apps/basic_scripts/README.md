# Basic Scripts
These are minimal, barebones scripts that demonstrate how to run inference on a **Tenstorrent** instance on **Koyeb**.

To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

## 1. Chat Completion - [chat_completion.py](https://github.com/tenstorrent/tt-example-apps/blob/main/basic_chat_apps/basic_scripts/chat_completion.py)
This script shows how to run a chat completion using the Tenstorrent instance and OpenAI client interface.

Replace `tt_base_url` and `model_id` with your instance values.
```python
tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"
```

> **Tip:** Don't forget the `/v1` endpoint at the end of the `base_url` parameter of the OpenAI client.  Otherwise, the chat completion endpoint will not be found.

The model ID for an instance can be found next to the [one-click deploy buttons](https://github.com/koyeb/tenstorrent-examples/tree/main/tt-models), in the Koyeb interface or logs, or by querying the `/v1/models` endpoint.

## 2. Chatbot - [chatbot.py](https://github.com/tenstorrent/tt-example-apps/blob/main/basic_chat_apps/basic_scripts/chatbot.py)

This is a simple chatbot that streams its responses and remembers previous messages.  

The inference fundamentals are the same as `chat_completion.py`: the OpenAI client is initialized with a Tenstorrent instance as the `base_url` and the same `client.chat.completions.create()` function is called to send the request to our instance.  

However, this time a list of messages is sent to the model during each chat completion, allowing the model to refer to previous messages.  Also, when calling the completion, `stream` is set to `True` to provide a responsive interface.

```python
conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Ask anything\n")

while True:
    user_query = input("You: ").strip()

    conversation.append({"role": "user", "content": user_query})

    response = client.chat.completions.create(
        model=model_id,
        messages=conversation,
        stream=True
    )

    ...

    conversation.append({"role": "assistant", "content": assistant_reply})
```

## 3. Agent - [agno_agent.py](https://github.com/tenstorrent/tt-example-apps/blob/main/basic_chat_apps/basic_scripts/agno_agent.py)

This script demonstrates how to create an Agno agent that uses a custom function to retrieve context before responding.  In this example, the model will retrieve current weather conditions in a location and use that information to recommend clothing.

The weather API used here is from https://www.weatherapi.com.

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for the [agno_agent.py](https://github.com/tenstorrent/tt-example-apps/tree/main/basic_chat_apps/basic_scripts/agno_agent.py) script  to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

### Walkthrough
Agno, OpenAI, and Requests are the only third-party dependencies used in this script.
```python
import os
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools import tool
import requests
```

First, we define our function to retrieve context for the model.  In this case, the function fetches the current temperature and weather conditions in a location, then returns a string with this information.  The [`@tool` decorator](https://docs.agno.com/tools/tool-decorator) from Agno is used to control what happens before and after this tool is called.  Seting `show_result=True` will show the output of the tool call in the agent’s response.

The function looks for an environment variable named `WEATHER_API_KEY`, which should be your [Weather API Key](https://www.weatherapi.com).

```python
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
```

In the `main` function, you will need to first replace `tt_base_url` and `model_id` with your instance values.

```python
tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"
```

The agent is initialized with the [OpenAILike](https://docs.agno.com/models/openai-like#openai-like) class, which allows us to use an external server for inference.  The `fetch_weather` function is passed to the agent in the list of available tools it can run, and the `instructions` list guides the model's behavior.  This should be customized for the specific use-case and desired output.

```python
agent = Agent(
    model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
    tools=[fetch_weather],
    instructions=[
        "You are a helpful assistant that gives practical outfit recommendations based on the current weather conditions.",
        "Your only function available is fetch_weather.  Use your existing knowledge for outfit recommendations."
    ],
    markdown=True
)
```

Set the `user_query` variable as your desired input.
```python
user_query = "I'm going to Chicago, how should I dress?"
```

We then print the model's response, setting `stream=True` to print the model's output as it arrives.
```python
agent.print_response(user_query, stream=True)
```

When running a query, the LLM will decide if it should call the `fetch_weather` function.  Agno handles the logic of calling the function, retrieving the output, then feeding that context back to the LLM before it generates a final response.
