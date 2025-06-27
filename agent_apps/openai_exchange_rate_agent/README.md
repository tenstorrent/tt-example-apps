# 💱 Exchange Rate Agent
This is a **Streamlit** app that creates an agent using the **OpenAI Agents SDK** to fetch currency exchange rates and return an accurate answer.  It demonstrates how to use custom functions with an **OpenAI** agent, while running all the LLM inference on **Tenstorrent** hardware.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/b8847f4d-b689-481c-bebf-e6881122e832

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/openai_exchange_rate_agent
```

### 2. Create a virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Get a free API Key from [ExchangeRate-API](https://www.exchangerate-api.com) and add your key as an environment variable named `EXCHANGE_RATE_API_KEY`.
```bash
export EXCHANGE_RATE_API_KEY=8g70d5f9...
```

### 4. Run the Streamlit app
```bash
streamlit run openai_exchange_rate_agent.py
```

## How it works

- An **OpenAI Agent** is created that uses a custom **AsyncOpenAI** client that points to the **Tenstorrent** instance endpoint as the base URL.
- **OpenAI Agents SDK** handles the function calls and feeding the context back to the model.
    - The model can call the `exchange_rates` function to get real-time exchange rates for different currencies.
- The app displays the agent's response in the **Streamlit** UI.
