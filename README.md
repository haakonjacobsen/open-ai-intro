# OpenAI Chatbot Workshop

## How to Run

1. Create a virtual environment:

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
   python chatbot.py
   ```
   Type 'quit', 'exit', or 'bye' to stop the chatbot.

## Workshop Tasks

### Task 1: Add Conversation History

Our chatbot can answer questions, but it doesn't remember what we've discussed earlier. Each message is treated as a new conversation, making follow-up questions impossible.

**Your Mission:**
Implement conversation history so the chatbot can remember previous messages and have natural back-and-forth dialogue.

**Steps:**

1. Store conversation history in your app
2. Send previous messages along with new ones to the OpenAI API
3. Test with follow-up questions

**Resources:** [OpenAI Chat API Docs](https://platform.openai.com/docs/guides/chat-completions)

**Hint:** The `messages` parameter accepts an array of message objects, not just one!
