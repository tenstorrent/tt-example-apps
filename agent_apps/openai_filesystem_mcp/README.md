# 🗂️ OpenAI Filesystem MCP Agent
This is a simple command-line Python script that demonstrates how to use the [filesystem MCP server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) (running locally via `npx`) with the [**OpenAI Agents SDK**](https://openai.github.io/openai-agents-python/), while running all the LLM inference on **Tenstorrent** hardware.  

It is based on the [filesystem MCP example](https://github.com/openai/openai-agents-python/tree/main/examples/mcp/filesystem_example) from the [OpenAI Agents SDK GitHub repo](https://github.com/openai/openai-agents-python).  The [sample files](./sample_files) from the repo are also included here for demonstration purposes.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for this demo to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/openai_filesystem_mcp
```

### 2. Create a virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install openai-agents
```

### 3. Update [`openai_filesystem_mcp_cli.py`](./openai_filesystem_mcp_cli.py) with your Tenstorrent instance URL and model ID
```python
# Update TT/Koyeb base url and model ID below
# ---------------------------------------------------------
tt_base_url = "https://<...>.koyeb.app/v1"
model_id = "..."
# ---------------------------------------------------------
```
> Ensure `tt_base_url` ends with `/v1`

Three example user queries are provided in the `run` function that will accomplish the following tasks respectively:
1. List all the files in the [sample_files](./sample_files) directory.
    * _favorite_books.txt_
    * _favorite_cities.txt_
    * _favorite_songs.txt_
2. Read [favorite_books.txt](./sample_files/favorite_books.txt) and return the first entry: _To Kill a Mockingbird – Harper Lee_.
3. Read [favorite_songs.txt](./sample_files/favorite_songs.txt) and recommend a similar song.

**You will need to adjust the model instructions and/or the prompt for reliable responses when using smaller LLMs.**

Adjust the user queries to your desired use-case.

### 4. Run the Python script
```bash
python openai_filesystem_mcp_cli.py
```

## How it works

* A local MCP filesystem server is started using `npx`, exposing only the `sample_files` directory. It uses the `MCPServerStdio` transport mechanism, which launches the server as a subprocess and communicates via standard input/output.

* The server provides tools like `list_directory` and `read_file`, which are automatically registered with the agent when the MCP server is passed to it. During execution, the SDK fetches available tool schemas and runs the tool selected by the LLM.

* The agent uses a **Tenstorrent** instance as the backend that implements the OpenAI-compatible `/v1/chat/completions` API. It’s accessed using a custom `AsyncOpenAI` client that points to the instance endpoint as its base url.

* Since inference is handled by a custom endpoint and not the OpenAI platform, `set_tracing_disabled(True)` is used to disable OpenAI’s trace reporting.

* Three queries are ran, with OpenAI Agents SDK orchestrating the MCP and tool calling functionality.
