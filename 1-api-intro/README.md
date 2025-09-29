# OpenAI API Workshop

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

### Task 3: Give Your Chatbot Eyes

Your chatbot can chat and remember conversations, but it's still blind to the visual world. Let's give it the power of sight! 👁️

**Your Mission:**
Transform your text-only chatbot into a multimodal AI that can see and analyze images from URLs.

**The Vision:**
After a user asks a question, prompt them to optionally share an image URL. Your chatbot will then analyze both the text question and the image together, creating richer, more contextual responses.

**Steps:**

1. After each user message, ask if they want to include an image
2. If yes, prompt for an image URL
3. Send both the text and image to OpenAI's vision-capable model (e.g. "gpt-4o")
4. Test with different types of images (photos, diagrams, memes, artwork)

**Fun Test Ideas:**

- Ask "What's in this image?" with a photo
- "Explain this meme" with a funny image
- "Help me with this math problem" with a screenshot
- "What's the mood of this artwork?" with a painting

**Resources:** [OpenAI Vision Guide](https://platform.openai.com/docs/guides/images-vision?api-mode=responses#analyze-images)

**Hint:** You'll need to format the user messages content as an array of both `input_text` and `input_image`. See the **Analyze images** under the Image and vision section.

### Task 4: Build a Quiz Generator with Structured Outputs

Time to move beyond chatbots! Let's create something completely different - an AI-powered quiz generator that transforms any text into educational quizzes with perfect structure. 📝

**Your Mission:**
Switch to the `quiz_generator.py` file and build a system that takes a .txt file and generates structured multiple-choice quizzes using Pydantic models.

**What Makes This Special:**
Instead of getting messy, unstructured text responses, you'll use OpenAI's structured outputs to get perfectly formatted quiz objects that your code can work with reliably.

**Steps:**

1. **Switch files**: Open `quiz_generator.py` (it's partially implemented)
2. **Define Pydantic models**: Create `QuizQuestion` and `Quiz` classes with proper fields
3. **Implement structured generation**: Use `client.responses.parse()` with `text_format=Quiz`
4. **Test with coffee science content**: You can use the `coffee_science_content.txt`to test, or create your own content.

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

**Resources:** [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs)

**Hint:** Use `response_format` parameter with your Quiz Pydantic model!
