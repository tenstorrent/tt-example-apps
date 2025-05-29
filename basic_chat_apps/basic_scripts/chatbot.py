"""This is an extremely simple chatbot that streams its responses and remembers previous messages."""

from openai import OpenAI

tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"

client = OpenAI(base_url=tt_base_url, api_key="null")

conversation = [
    {"role": "system", "content": "You are a helpful assistant."}
]

print("Ask anything\n")

while True:
    user_query = input("You: ").strip()

    conversation.append({"role": "user", "content": user_query})

    response = client.chat.completions.create(
        model=model_id,
        messages=conversation,
        stream=True
    )

    assistant_reply = ""
    print("Assistant:", end=" ", flush=True)

    for chunk in response:
        delta = chunk.choices[0].delta.content or ""
        print(delta, end="", flush=True)
        assistant_reply += delta

    print("\n")
    conversation.append({"role": "assistant", "content": assistant_reply})
