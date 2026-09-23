# Claude API Workshop

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

4. Create a `.env` file with your Anthropic API key:

   ```
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   ```

5. Run the chatbot:
   ```bash
   python chatbot.py
   ```
   Type 'quit', 'exit', or 'bye' to stop the chatbot.

## What's Happening Under the Hood?

Every call to Claude goes through one endpoint: the **Messages API** (`POST /v1/messages`). The Python SDK wraps it as `client.messages.create()`. You send a request and get a response back. That's it - the API has no memory, no state, no magic.

**The request** has three parts you'll use in this workshop:

```python
response = client.messages.create(
    model="claude-opus-5",   # which model answers
    max_tokens=4096,         # the maximum length of the reply (required)
    system="...",            # optional: instructions for how Claude should behave
    messages=[               # the conversation so far, alternating user/assistant turns
        {"role": "user", "content": "Hello!"},
    ],
)
```

**The response** is a `Message` object. The interesting part is `response.content`: a **list of content blocks**, not a single string. A plain text answer looks like this:

```python
response.content     # [TextBlock(type="text", text="Hello! How can I help?")]
response.stop_reason # "end_turn" - Claude finished on its own
```

Later you'll see other block types show up in that list (`thinking`, `tool_use`, ...). That's why the starter code picks out the text blocks instead of assuming there is exactly one:

```python
assistant_text = "".join(block.text for block in response.content if block.type == "text")
```

**Resources:** [Messages API reference](https://platform.claude.com/docs/en/api/messages)

## Workshop Tasks

### Task 1: Give Your Chatbot Personality

Your chatbot works, but it's a bit... boring. It answers like a generic AI assistant. Let's spice things up by giving it some personality!

**Your Mission:**
Use the system prompt to transform your chatbot into a character with a unique personality and speaking style.

**Choose a personality (or create your own):**

- 🎭 **Sarcastic Comedian** - Answers everything with witty sarcasm and dry humor
- 🏆 **Motivational Speaker** - Turns every response into an inspirational speech with enthusiasm
- 🕵️ **Sherlock Holmes** - Responds with deductive reasoning and Victorian-era eloquence
- 🏴‍☠️ **Pirate Captain** - Speaks like a swashbuckling sea captain with nautical terms
- 👑 **Shakespeare** - Answers in Elizabethan English with poetic flair

**Steps:**

1. Add a `system` parameter to `client.messages.create()` with your chosen personality instructions
2. Test different questions to see how the personality affects responses
3. Fine-tune the personality prompt for better results

**Resources:** [Giving Claude a role with a system prompt](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts)

**Hint:** The system prompt is not part of the `messages` list. It's a separate top-level parameter that sets the behavior for the whole conversation - like giving the AI a personality!

### Task 2: Add Conversation History

Our chatbot can answer questions, but it doesn't remember what we've discussed earlier. Each message is treated as a new conversation, making follow-up questions impossible.

**Your Mission:**
Implement conversation history so the chatbot can remember previous messages and have natural back-and-forth dialogue.

**Steps:**

1. Store conversation history in your app's memory (a list of messages)
2. Send all previous messages along with the new one to the Claude API
3. After each reply, add Claude's answer to the list as an `assistant` message
4. Test with follow-up questions

**Resources:** [Messages API reference - messages parameter](https://platform.claude.com/docs/en/api/messages)

**Hint:** The `messages` parameter accepts a list of message objects with `role` set to `"user"` or `"assistant"`. Roles must alternate, and the first message must be from the user. The API is stateless - if you don't send the history, Claude has never seen it. You can add Claude's reply to the history as `{"role": "assistant", "content": response.content}`.

### Task 3: Give Your Chatbot Eyes

Your chatbot can chat and remember conversations, but it's still blind to the visual world. Let's give it the power of sight! 👁️

**Your Mission:**
Transform your text-only chatbot into a multimodal AI that can see and analyze images from URLs.

**The Vision:**
After a user asks a question, prompt them to optionally share an image URL. Your chatbot will then analyze both the text question and the image together, creating richer, more contextual responses.

**Steps:**

1. After each user message, ask if they want to include an image
2. If yes, prompt for an image URL
3. Send both the text and the image to Claude in the same user message
4. Test with different types of images (photos, diagrams, memes, artwork)

**Fun Test Ideas:**

- Ask "What's in this image?" with a photo
- "Explain this meme" with a funny image
- "Help me with this math problem" with a screenshot
- "What's the mood of this artwork?" with a painting

**Resources:** [Claude Vision Guide](https://platform.claude.com/docs/en/build-with-claude/vision)

**Hint:** So far `content` has been a plain string. It can also be a list of content blocks, just like in the response. Combine a `text` block and an `image` block:

```python
{
    "role": "user",
    "content": [
        {"type": "image", "source": {"type": "url", "url": image_url}},
        {"type": "text", "text": user_input},
    ],
}
```

### Task 4: Build a Quiz Generator with Structured Outputs

Time to move beyond chatbots! Let's create something completely different - an AI-powered quiz generator that transforms any text into educational quizzes with perfect structure. 📝

**Your Mission:**
Switch to the `quiz_generator.py` file and build a system that takes a .txt file and generates structured multiple-choice quizzes using Pydantic models.

**What Makes This Special:**
Instead of getting messy, unstructured text responses, you'll use Claude's structured outputs to get perfectly formatted quiz objects that your code can work with reliably.

**Steps:**

1. **Switch files**: Open `quiz_generator.py` (it's partially implemented)
2. **Define Pydantic models**: Create `QuizQuestion` and `Quiz` classes with proper fields
3. **Implement structured generation**: Use `client.messages.parse()` with `output_format=Quiz` and read the result from `response.parsed_output`
4. **Test with coffee science content**: You can use the `coffee_science_content.txt` to test, or create your own content.

**Key Features to Implement:**

- Multiple choice questions (4 options each)
- Correct answer tracking
- Explanations for each answer
- Automatic quiz title generation
- User-friendly display formatting

**Test Ideas:**

- Wikipedia articles about science topics
- News articles about current events
- Documentation from your favorite programming language
- Short stories or book chapters

**(Optional)**: Create a way to play the quiz after it is generated in the terminal.

**Resources:** [Claude Structured Outputs Guide](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Hint:** `client.messages.parse()` takes the same parameters as `create()`, plus `output_format`. Under the hood it turns your Pydantic model into a JSON schema that Claude's output is guaranteed to follow, then validates the reply back into a `Quiz` instance for you. Use `quiz.model_dump()` when saving it to JSON.
