## 🌦️ AI Weather Agent
This **Streamlit** app retrieves the current weather in a given location based on natural language input and suggests what kind of clothing to wear.  It demonstrates how to use tool calls with the OpenAI client to create a very simple agent workflow.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).

## Demo

https://github.com/user-attachments/assets/d5c34f55-31e2-4c72-b5ba-77a0761d614e

### Features
- Fetches current weather for the requested location.
- Analyzes conditions like temperature, rain, and wind.
- Recommends what to wear based on the user’s question and the weather.

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/weather_agent
```

### 2. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your Weather API key
Sign up for a [Weather API account](https://www.weatherapi.com) and obtain your API key needed for real-time weather information.

### 4. Run the Streamlit app
```bash
streamlit run weather_agent.py
```

### How it works
- The LLM running on a **Tenstorrent** instance extracts search parameters from user input.
- These parameters are passed to the **Weather API** function, which retrieves the current weather from a specific area.
- Search results are fed back to the LLM to generate a final, accurate response.
