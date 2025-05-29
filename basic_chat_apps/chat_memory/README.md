## 🤖 Streaming Chatbot with Memory 
This **Streamlit** app is a helpful assistant that can be asked anything.  It demonstrates how to use streaming and chat history, enabling a natural, familiar interface.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).

## Demo

https://github.com/user-attachments/assets/60617d74-e645-4167-9538-e08d26443e36

### Features
- Responds in real-time for an interactive experience.
- Remembers previous messages to support follow-up questions.
- Performs LLM inference on **Tenstorrent** hardware for high efficiency and throughput.

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/basic_chat_apps/chat_memory
```

### 2. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app
```bash
streamlit run chat_memory.py
```

### How it works
- A **Tenstorrent-powered** LLM generates an answer to the user’s query and streams it back in real time.
- Text is parsed and displayed as it arrives, then the full response is stored after completion.
- The entire conversation history is fed back into the model’s context window to support follow-up questions.
