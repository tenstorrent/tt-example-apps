# 📄 AWS Strands File-Read Agent
This is a **Streamlit** app that creates an agent using the [**AWS Strands Agents SDK**](https://strandsagents.com/latest/) to read a local file and return a response based on its content.  It demonstrates how to use tools with a **Strands** agent, while running all the LLM inference on **Tenstorrent** hardware.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Demo

https://github.com/user-attachments/assets/d2d13407-b70f-45a8-be58-5114c61250c6

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/aws_strands_agent
```

### 2. Create a virtual environment and install the required dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Streamlit app
```bash
streamlit run aws_strands_agent.py
```

> For a simpler version of this app with minimal code and easy reuse, see the CLI version: [`aws_strands_agent_cli.py`](./aws_strands_agent_cli.py)

## How it works

- A **Strands Agent** is created that uses a custom **OpenAIModel** client that points to the **Tenstorrent** instance endpoint as the base URL.
- **Strands Agents SDK** handles the function calls and feeding the context back to the model.
    - The model can call the `file_read` function, which is a built-in function to Strands, to read the contents of a local file.
    - There is an example file in this directory titled `example_env.txt`, which has a list of Python libraries and versions defining an environment.
- The agent will read the file, then return an accurate response in the **Streamlit** UI.
