## 🗺️ AI Travel Guide
This **Streamlit** app is an AI-powered travel guide that searches the web to find restaurants, shops, or attractions around a specific location.  It demonstrates how to use tool calls to create a very simple agent workflow.

This example requires an active Tenstorrent instance running on Koyeb.  To deploy your first service using Tenstorrent instances on Koyeb, refer to Koyeb's [tenstorrent-examples repository](https://github.com/koyeb/tenstorrent-examples).

## Demo

https://github.com/user-attachments/assets/d642d76f-1b83-49fb-9c90-65bf4eacd10d

### Features
- Searches the web for up-to-date information.
- Responds conversationally to travel-related queries.
- Summarizes structured search results with ratings and descriptions.

## Getting started

### 1. Clone the GitHub repository
```bash
git clone https://github.com/tenstorrent/tt-example-apps.git
cd tt-example-apps/agent_apps/travel_guide
```

### 2. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 3. Get your SerpAPI Key
Sign up for a [SerpAPI account](https://serpapi.com/) and obtain your API key needed for real-time web searches.

### 4. Run the Streamlit app
```bash
streamlit run travel_guide.py
```

### How it works
- The LLM running on a **Tenstorrent** instance extracts search parameters from user input.
- These parameters are passed to the **SerpAPI** function, which performs a **Google** web search to retrieve local results from a specific area.
- Search results are fed back to the LLM to generate a final, accurate response.