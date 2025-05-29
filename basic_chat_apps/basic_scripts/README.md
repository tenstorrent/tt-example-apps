# Basic Scripts
These are minimal, barebones scripts that demonstrate how to run inference on a **Tenstorrent** instance on **Koyeb**.

To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).  

> **_NOTE:_** Automatic tool calling must be enabled on the instance's vLLM server for the [agno_agent.py](https://github.com/tenstorrent/tt-example-apps/tree/main/basic_chat_apps/basic_scripts/agno_agent.py) script  to work.  Please refer to [vLLM's Tool Calling docs](https://docs.vllm.ai/en/stable/features/tool_calling.html#automatic-function-calling) for the required flags.  One-click deploy models will have these flags enabled if the LLM supports tool calling. (i.e. Llama and Qwen models)

* You will need to replace `tt_base_url` and `model_id` with your instance values to run these scripts.  
* The `agno_agent.py` script uses an API key to fetch the weather from https://www.weatherapi.com.
