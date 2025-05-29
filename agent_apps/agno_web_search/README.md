# 🔎 Web Search Agent
This is a **Streamlit** app that uses an **Agno** agent to search the internet for queries using **DuckDuckGo**.  It demonstrates how to create a basic **Agno** agent with tool use.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/8395336b-04d3-43a5-93e2-48b1f5eba141

## Features
- Request headlines, news, and articles
- Receive up-to-date, relevant information

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/agno_web_search
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run agno_web_search.py
```

## How it works

- An **Agno** agent is created with an **OpenAILike** client as the model provider.
- The **OpenAILike** client's model is pointed to the **Tenstorrent** instance.
- The **DuckDuckGoTools** search engine tool is added to the available tools for the model.
    - The agent can call one of two [DuckDuckGo toolkit functions](https://docs.agno.com/tools/toolkits/search/duckduckgo#toolkit-functions): search for a query or get the latest news.
- **Agno** handles the function calls and feeding the context back to the model.
- The app displays the answer to the user's question in the **Streamlit** UI.
