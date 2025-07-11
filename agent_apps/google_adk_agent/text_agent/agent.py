# SPDX-FileCopyrightText: (c) 2025 Tenstorrent AI ULC
#
# SPDX-License-Identifier: Apache-2.0
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

def count_words(text: str) -> int:
    """Return the number of words in the input text."""
    return len(text.split())

def reverse_text(text: str) -> str:
    """Return the reversed version of the input text."""
    return text[::-1]

def count_characters(text: str) -> int:
    """Return the number of characters in the text."""
    return len(text)

# Update TT/Koyeb base url and model ID below
# ---------------------------------------------------------
tt_base_url = "https://<...>.koyeb.app/v1"
model_id = "hosted_vllm/..."
# ---------------------------------------------------------

root_agent = LlmAgent(
    model=LiteLlm(
        model=model_id,
        api_base=tt_base_url
    ),
    name="text_agent",
    instruction="You are a helpful assistant that can analyze or transform text using simple tools.",
    description="An agent that manipulates and inspects user text.",
    tools=[count_words, reverse_text, count_characters]
)
