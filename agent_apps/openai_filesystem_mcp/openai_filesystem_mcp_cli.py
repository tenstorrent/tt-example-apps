# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
import asyncio
import os
import shutil

from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.mcp import MCPServer, MCPServerStdio


async def run(mcp_server: MCPServer):
    # Update TT/Koyeb base url and model ID below
    # ---------------------------------------------------------
    tt_base_url = "https://<...>.koyeb.app/v1"
    model_id = "..."
    # ---------------------------------------------------------

    custom_client = AsyncOpenAI(base_url=tt_base_url, api_key="null")
    set_tracing_disabled(True)

    agent = Agent(
        name="Assistant",
        model=OpenAIChatCompletionsModel(model=model_id, openai_client=custom_client),
        instructions="Use the tools to read the filesystem and answer questions based on those files. Only operate within the allowed directories given by the MCP server.",
        mcp_servers=[mcp_server]
    )

    # List the files it can read
    message = "List all my sample files"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask about books
    message = "What is #1 in my list of favorite books?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

    # Ask a question that reads then reasons
    message = "Look at the list of my favorite songs. Suggest one new song that I might like."
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)


async def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")

    async with MCPServerStdio(
        name="Filesystem Server, via npx",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        await run(server)


if __name__ == "__main__":
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")

    asyncio.run(main())
