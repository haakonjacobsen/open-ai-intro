# Claude API Tools Workshop

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

4. Create a `.env` file with your Anthropic API key:

   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. Run the assistant:
   ```bash
   python assistant.py
   ```
   Type 'quit', 'exit', or 'bye' to stop the assistant.

## What's Happening Under the Hood?

Tools are how Claude does things beyond writing text. There are two kinds, and both are passed in the same `tools` parameter to `client.messages.create()`:

- **Server tools** (like web search) run on Anthropic's servers. You declare them, and the results show up inside the response. Nothing to implement.
- **Custom tools** (like sending a Slack message) run in **your** code. Claude can't call your function directly - it can only *ask*. The response comes back with `stop_reason == "tool_use"` and a `tool_use` block telling you which tool to run and with which input. You run it, send the result back, and Claude continues.

That request → tool call → result → request cycle is the **agent loop**, and in this workshop you build it yourself. Here is what the conversation looks like on the wire for a single tool call:

```python
# 1. Claude asks to use a tool
response.stop_reason  # "tool_use"
response.content      # [TextBlock(...), ToolUseBlock(id="toolu_01...", name="send_slack_message", input={"message": "Hi!"})]

# 2. You add Claude's reply to the history, run the tool, and add the result
messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": [{"type": "tool_result", "tool_use_id": "toolu_01...", "content": "Message sent to Slack: 'Hi!'"}],
})

# 3. Call the API again with the updated history. Claude now knows what happened
#    and answers the user, this time with stop_reason == "end_turn".
```

**Resources:** [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) · [Handling stop reasons](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons)

## Workshop Tasks

### Task 1: Give Your Chatbot the Ability to Search the Web

Your assistant can chat and remember conversations, but it's stuck in the past with its training data. Let's connect it to the real world by giving it web search superpowers! 🌐

**Your Mission:**
Enable your chatbot to search the internet for current information, news, and real-time data using Claude's built-in web search tool.

**The Power of Real-Time Information:**
Transform your assistant from a knowledge time capsule into a current-events expert that can answer questions about today's news, latest stock prices, recent sports scores, and trending topics.

**Steps:**

1. Add the `tools` parameter to your `client.messages.create()` call
2. Include web search in your tools list: `tools=[{"type": "web_search_20260209", "name": "web_search"}]`
3. Test with questions that require current information.

**Test Ideas:**

- "What's the latest news about AI?"
- "Who won the latest football match?"
- "What are the current stock prices for tech companies?"
- "What happened in the world today?"

**Resources:** [Claude Web Search Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)

**Hint:** Look for the `#TODO: Add assistant tools` comment in `assistant.py` - that's where you'll add the tools parameter! Web search is a server tool, so `response.content` will now contain `server_tool_use` and `web_search_tool_result` blocks alongside the `text` blocks. Try printing `response.content` once to see it.

### Task 2: Show Sources from Web Search

Your chatbot searches the web, but users can't see where the information comes from. Let's add the sources to the assistant's response for transparency! 🔍

**Your Mission:**
Append the sources that the AI consulted to the assistant's response text, so users know where their information came from.

**Steps:**

1. Look at the `text` blocks in `response.content`. When Claude used web search, each one has a `citations` list
2. Each citation with `type == "web_search_result_location"` has a `url` and a `title`
3. Extract the domain names from the URLs and append them to the assistant's message before displaying it

**Example Output:**

```
🤖 Assistant: The weather in Paris is currently 15°C with light rain...
...
📚 Sources: weather.com, bbc.com, accuweather.com
```

**Resources:** [Claude Web Search Tool - Response](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)

**Hint:** Citations come back automatically with web search - you don't need to ask for them. There is a `get_sources` helper in `utils/get_sources.py` you can use or look at for inspiration.

### Task 3: Add Custom Function Calling - Send Slack Messages

Now it's time to go beyond built-in tools and create your own custom tools! Let's give your assistant the ability to send messages to Slack using Claude's tool use capabilities. 💬

**Your Mission:**
Enable your chatbot to send messages to Slack by implementing custom tool calling with the `send_slack_message` function that's already been created for you in the `tools/` folder.

**The Power of Custom Tools:**
Transform your assistant from just a conversational AI into an action-taking assistant that can interact with external services.

**Steps:**

1. **Add your Slack webhook** to the `.env` file:

   ```
   SLACK_WEBHOOK=your_slack_webhook_url_here
   ```

2. **Import the Slack function** at the top of `assistant.py`:

   ```python
   from tools.send_slack_message import send_slack_message
   ```

3. **Define your tool schema** - Add this tool definition to your tools list:

   ```python
   {
       "name": "send_slack_message",
       "description": "Send a message to a Slack channel via webhook",
       "input_schema": {
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

4. **Build the agent loop** - When Claude wants to call your tool, you need to:

   - check if `response.stop_reason == "tool_use"`
   - add Claude's full reply to the message history: `{"role": "assistant", "content": response.content}`
   - for each block in `response.content` with `type == "tool_use"`, read the tool `name` and `input`
   - a tip here is to create a lookup table that maps the name to the actual function
   - call your actual function with the `input` you got (it's already a dict)
   - add the result to the message history as a user message containing a `tool_result` block, with `tool_use_id` set to the `id` of the `tool_use` block
   - ask Claude for a new response with the tool result you have added
   - do this until `stop_reason` is no longer `"tool_use"`, then return the response

**Test Ideas:**

- "Send a message to Slack saying 'Hello from Claude!'"
- "Notify the team about something you can search for (using the web search tool)"
- "Send a Slack message with today's weather summary"

**Example Output:**

```

🫵 User: Send a message to Slack saying "Meeting starts in 5 minutes!"
🔧 Calling tool: send_slack_message with arguments: {'message': 'Meeting starts in 5 minutes!'}
🤖 Assistant: I've sent the message to Slack successfully: "Meeting starts in 5 minutes!"

```

**Resources:**

- [Claude Tool Use Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)
- [Implementing tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)

**Hints:**

- Look at the existing `send_slack_message.py` in the `tools/` folder to understand the function signature
- Claude can ask for several tools in one reply. Run them all and send **all** the `tool_result` blocks back in a single user message
- If a web search runs long, the response can come back with `stop_reason == "pause_turn"`. Add the reply to the history and call the API again - Claude picks up where it left off
- Put a cap on the number of loop iterations so a confused model can't loop forever
- Stuck? `solution.py` has a complete agent loop

### Task 4: Create Your Own Custom Tool

Now it's your turn to be creative! 🚀

**Your Mission:**
Design and implement your own custom tool that the assistant can call. Think about what would be useful - APIs that would be fun to hook up. It could be nice to ask the user for permission in the chat before running tools.

**Steps:**

1. Create a new Python file in the `tools/` folder
2. Define your function with proper parameters and return values
3. Add the tool schema to your tools list and the function to your lookup table
4. Test it with your assistant

**Ideas:** Calculator, todo list manager, random joke generator, unit converter, or anything you can imagine!
