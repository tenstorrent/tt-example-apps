"""Basic chat completion."""

from openai import OpenAI

tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"

client = OpenAI(api_key="null", base_url=tt_base_url)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Tell me a joke.",
        }
    ],
    model=model_id,
    max_tokens=30,
)

print(chat_completion.to_json(indent=4))
