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

### Task 3: Add Custom Function Calling - Send Slack Messages

Now it's time to go beyond built-in tools and create your own custom functions! Let's give your assistant the ability to send messages to Slack using OpenAI's function calling capabilities. 💬

**Your Mission:**
Enable your chatbot to send messages to Slack by implementing custom function calling with the `send_slack_message` function that's already been created for you in the `tools/` folder.

**The Power of Custom Functions:**
Transform your assistant from just a conversational AI into an action-taking assistant that can interact with external services.

**Steps:**

1. **Import the Slack function** at the top of `assistant.py`:

   ```python
   from tools.send_slack_message import send_slack_message
   ```

2. **Define your function schema** - Add this function definition to your tools array:

   ```python
   {
       "type": "function",
       "name": "send_slack_message",
       "description": "Send a message to a Slack channel via webhook",
       "parameters": {
           "type": "object",
           "properties": {
               "message": {
                   "type": "string",
                   "description": "The message to send to Slack"
               }
           },
           "required": ["message"],
           "additionalProperties": False,
       },
       "strict": True,
   }
   ```

3. **Handle function calls** - When the model wants to call your function, you need to:

   - for each item in response.output, check if the item has the `type == "function_call"`
   - if so, add the item to the message history and call the function by extracting the function `name` and `arguments`
   - a tip here is to ceate a lookup table that maps the name to the actual function
   - call your actual function with the `arguments` you got (remember to parse them to a dict)
   - add the ouput of the function to the message history, and ask the model for a new response with the function results we have added
   - do this until we no longer get function responses, then just return the response

**Test Ideas:**

- "Send a message to Slack saying 'Hello from OpenAI Assistant!'"
- "Notify the team about something you can google (using the web search tool)"
- "Send a Slack message with today's weather summary"

**Example Output:**

```

🫵 User: Send a message to Slack saying "Meeting starts in 5 minutes!"
🤖 Assistant: I've sent the message to Slack successfully: "Meeting starts in 5 minutes!"

```

**Resources:**

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [OpenAI Tools Guide - Function Calling](https://platform.openai.com/docs/guides/tools?tool-type=function-calling)

**Hints:**

- Look at the existing `send_slack_message.py` in the `tools/` folder to understand the function signature
- You'll need to handle the function call response and execute the actual function when the model requests it
- Don't forget to add the function result back to the conversation flow!

### Task 4: Create Your Own Custom Function

Now it's your turn to be creative! 🚀

**Your Mission:**
Design and implement your own custom function that the assistant can call. Think about what would be useful - APIs that would be fun to hook up. It could be nice to ask the user for permission in the chat before running functions.

**Steps:**

1. Create a new Python file in the `tools/` folder
2. Define your function with proper parameters and return values
3. Add the function schema to your tools array
4. Test it with your assistant

**Ideas:** Calculator, todo list manager, random joke generator, unit converter, or anything you can imagine!
