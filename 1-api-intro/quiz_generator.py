import json

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude client. It reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

# The model we send our requests to
MODEL = "claude-opus-5"


# The model for the quiz we want to generate
class Quiz(BaseModel):
    pass


def create_quiz(content):
    """Send the text content to Claude and return the generated quiz"""
    response = client.messages.create(
        model=MODEL,
        max_tokens=16000,
        messages=[
            {
                "role": "user",
                "content": f"Create a multiple-choice quiz based on this text:\n\n{content}",
            }
        ],
        # TODO: Switch to client.messages.parse() and pass the Quiz model as output_format
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main():
    """Main quiz generator loop"""
    # File path to generate the quiz from
    file_path = input("🫵 Enter the file path to generate the quiz from: ")
    print(f"🤖 Generating quiz from {file_path}...")

    # Read the text to generate the quiz from
    with open(file_path) as f:
        content = f.read()

    # Create the quiz
    quiz = create_quiz(content)

    # Save the quiz to a JSON file
    # TODO: Once create_quiz returns a Quiz object, save quiz.model_dump() instead
    with open("quiz.json", "w") as f:
        json.dump(quiz, f)

    # TODO: Implement a way for users to play the quiz


if __name__ == "__main__":
    main()
