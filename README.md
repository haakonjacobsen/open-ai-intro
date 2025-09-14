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

### Task 1: Give Your Chatbot Personality

Your chatbot works, but it's a bit... boring. It answers like a generic AI assistant. Let's spice things up by giving it some personality!

**Your Mission:**
Use the developer message to transform your chatbot into a character with a unique personality and speaking style.

**Choose a personality (or create your own):**

- 🎭 **Sarcastic Comedian** - Answers everything with witty sarcasm and dry humor
- 🏆 **Motivational Speaker** - Turns every response into an inspirational speech with enthusiasm
- 🕵️ **Sherlock Holmes** - Responds with deductive reasoning and Victorian-era eloquence
- 🏴‍☠️ **Pirate Captain** - Speaks like a swashbuckling sea captain with nautical terms
- 👑 **Shakespeare** - Answers in Elizabethan English with poetic flair

**Steps:**

1. Add a developer message with your chosen personality instructions
2. Test different questions to see how the personality affects responses
3. Fine-tune the personality prompt for better results

**Resources:** [OpenAI Message Roles Guide](https://platform.openai.com/docs/guides/text#message-roles-and-instruction-following)

**Hint:** Setting instructions, or adding a developer message will set the behavior - they're like giving the AI a personality!

### Task 2: Add Conversation History

Our chatbot can answer questions, but it doesn't remember what we've discussed earlier. Each message is treated as a new conversation, making follow-up questions impossible.

**Your Mission:**
Implement conversation history so the chatbot can remember previous messages and have natural back-and-forth dialogue.

**Steps:**

1. Store conversation history in your apps memory
2. Send previous messages along with new ones to the OpenAI API
3. Test with follow-up questions

**Resources:** [OpenAI - Message roles and insructions](https://platform.openai.com/docs/guides/text#message-roles-and-instruction-following)

**Hint:** The `input` parameter accepts an array of message objects. Check what the `response.output_text` returns.
