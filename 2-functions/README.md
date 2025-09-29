# OpenAI API Functions/Tools Workshop

## How to Run

1. Create a virtual environment in the `2-functions` folder:

   ```bash
   cd 2-functions
   ```

   ```bash
   python -m venv venv
   ```

   or

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. Run the chatbot:
   ```bash
   python assistant.py
   ```
   Type 'quit', 'exit', or 'bye' to stop the chatbot.

## Workshop Tasks

### Task 1: Give Your Chatbot the Ability to Search the Web

Your assistant can chat and remember conversations, but it's stuck in the past with its training data. Let's connect it to the real world by giving it web search superpowers! 🌐

**Your Mission:**
Enable your chatbot to search the internet for current information, news, and real-time data using OpenAI's built-in web search tool.

**The Power of Real-Time Information:**
Transform your assistant from a knowledge time capsule into a current-events expert that can answer questions about today's news, latest stock prices, recent sports scores, and trending topics.

**Steps:**

1. Add the `tools` parameter to your `client.responses.create()` call
2. Include web search in your tools array: `tools=[{"type": "web_search"}]`
3. Test with questions that require current information.

**Test Ideas:**

- "What's the latest news about AI?"
- "Who won the latest football match?"
- "What are the current stock prices for tech companies?"
- "What happened in the world today?"

**Resources:** [OpenAI Tools Guide - Web Search](https://platform.openai.com/docs/guides/tools?api-mode=responses&tool-type=web-search)

**Hint:** Look for the `#TODO: Add assistant tools` comment in `assistant.py` - that's where you'll add the tools parameter!

### Task 2: Show Sources from Web Search

Your chatbot searches the web, but users can't see where the information comes from. Let's add the sources to the assistant's response for transparency! 🔍

**Your Mission:**
Append the sources that the AI consulted to the assistant's response text, so users know where their information came from.

**Steps:**

1. Add `include=["web_search_call.action.sources"]` to your API call to get source data [(as described in the docs)](https://platform.openai.com/docs/guides/tools-web-search#sources)
2. Extract sources from `response.output` where `type == "web_search_call"`
3. Append the sources to the assistant's message before displaying it

**Example Output:**

```
🤖 Assistant: The weather in Paris is currently 15°C with light rain...
...
📚 Sources: weather.com, bbc.com, accuweather.com
```

**Resources:** [OpenAI Web Search - Sources](https://platform.openai.com/docs/guides/tools-web-search#sources)

**Hint:** You need to tell the API to include sources data, then extract domain names from the source URLs for clean display!
