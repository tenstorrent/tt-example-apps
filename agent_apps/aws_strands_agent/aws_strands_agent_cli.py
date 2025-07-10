# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
"""
This is a simplified version of the Streamlit app that runs in the terminal.
"""
from strands import Agent
from strands.models.openai import OpenAIModel
from strands_tools import file_read

tt_base_url = "https://<...>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"

model = OpenAIModel(
    client_args={
        "api_key": "null",
        "base_url": tt_base_url
    },
    model_id=model_id
)

agent = Agent(
    model=model, 
    tools=[file_read]
)

response = agent("Read example_env.txt and tell me what version of PyTorch is used?")  # torch==2.7.0
