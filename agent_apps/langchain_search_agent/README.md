# ⛓️ LangChain Web Search Agent
This is a **Streamlit** app that uses a **LangChain** agent to search the internet for queries using **Tavily Search**.  It demonstrates how to create a basic **LangChain** agent with tool use.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/57d183d0-e622-4102-b5e6-3facdfd7631f

## Features
- Ask questions that require recent information
- Receive accurate responses from the agent
- View tool calls and model steps

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/langchain_search_agent
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Get your [Tavily Search API key](https://tavily.com/) and add it to your environment
```bash
export TAVILY_API_KEY=tvly-dev-x3TY0W*******************
```

### 4. Run the Streamlit app
```bash
streamlit run langchain_search_agent.py
```

## How it works

- A **LangChain** agent is created with a **ChatOpenAI** client as the model provider.
- The **ChatOpenAI** client's model is pointed to the **Tenstorrent** instance.
- The **Tavily** search engine tool is added to the available tools for the model.
- **LangChain** handles the function calls and feeding the context back to the model.
- The app displays the answer to the user's question in the **Streamlit** UI.
