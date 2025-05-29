# 📈 AI Investment Agent
This is a **Streamlit** app that uses an **Agno** agent to to analyze a company's income statements and generate detailed reports.  There is also a command line version that includes reasoning.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/face5ea9-0750-4c02-8cb4-35b39420425d

## Features
- Retrieves real-time financial data for any publicly traded stock.
- Generates detailed report analyzing performance, valuation, and growth.

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/investment_agent
```

### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run investment_agent.py
```

_To execute the command line version, update the following variables at the top of_ `cli_investment_agent.py`_, for example:_
```
tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"
stock = "NVDA"
```

_Then run:_ `python cli_investment_agent.py`

## How it works

- An **Agno** agent is created with an **OpenAILike** client as the model provider.
- The **OpenAILike** client's model is pointed to the **Tenstorrent** instance.
- The **YFinance** (Yahoo Finance) tool is added to the available tools for the model to retrieive current stock information.
- **Agno** handles the function calls and feeding the context back to the model.
- The model generates a report on the chosen stock.
- The final response is displayed in the **Streamlit** UI.

_This application is meant to strictly demonstrate the technical implementation of an LLM agent using different tools, and its output should not be taken as financial advice._
