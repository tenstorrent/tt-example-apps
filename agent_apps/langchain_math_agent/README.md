# ➕ LangChain Math Agent
This is a **Streamlit** app that uses a **LangChain** agent to add, subtract, multiply, or divide two numbers before returning an answer.  It demonstrates how to use custom functions with a **LangChain** agent to get accurate answers on tasks that LLMs typically struggle with.  Both the agent output and model output (without tools) is returned to show the difference in accuracy.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/66985cf3-3589-4936-829e-f28325286d95

## Features
- Ask for an operation on two numbers in natural language
- Receive accurate calculations from agent tool use
- View responses from both agent and model to show difference in accuracy

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/langchain_math_agent
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run langchain_math_agent.py
```

## How it works

- A **LangChain** agent is created with a **ChatOpenAI** client as the model provider.
- The **ChatOpenAI** client's model is pointed to the **Tenstorrent** instance.
- Functions are defined to add, subtract, multiply, and divide two numbers.
- **LangChain** handles the function calls and feeding the context back to the model.
- The app displays the agent's calculation and the original model's calculation in the **Streamlit** UI.
