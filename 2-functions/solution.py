import anthropic
from dotenv import load_dotenv
from tools.send_slack_message import send_slack_message
from utils.get_sources import get_sources

# Load environment variables from .env file
load_dotenv()

# Initialize the Claude client. It reads ANTHROPIC_API_KEY from the environment.
client = anthropic.Anthropic()

# The model we send our requests to
MODEL = "claude-opus-5"

SYSTEM_PROMPT = (
    "You are a helpful assistant with access to tools, to help the user with their requests."
)

# Maps tool names (as Claude sees them) to the Python functions that implement them
tool_lookup = {
    "send_slack_message": send_slack_message,
}

tools = [
    # Built-in server tool: runs on Anthropic's servers, nothing for us to implement
    {"type": "web_search_20260209", "name": "web_search"},
    # Custom tool: Claude asks us to run it, and we send the result back
    {
        "name": "send_slack_message",
        "description": "Send a message to a Slack channel via webhook",
        "input_schema": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to send to Slack",
                }
            },
            "required": ["message"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]


def chat_with_bot(messages):
    """Run the agent loop: call Claude, run any tools it asks for, repeat until it is done"""
    max_iterations = 10

    for _ in range(max_iterations):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,
            tools=tools,
        )

        # 1. Always add Claude's full reply to the history, including any tool_use blocks.
        #    The tool results we add afterwards must match these tool_use blocks.
        messages.append({"role": "assistant", "content": response.content})

        # 2. A server tool (web search) paused mid-turn. Calling again resumes it.
        if response.stop_reason == "pause_turn":
            continue

        # 3. Claude did not ask for any tools, so this is the final answer
        if response.stop_reason != "tool_use":
            return response

        # 4. Claude wants to call one or more of our tools. Run them all.
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            print(f"🔧 Calling tool: {block.name} with arguments: {block.input}")

            if block.name in tool_lookup:
                function_to_call = tool_lookup[block.name]
                result = function_to_call(block.input)
                tool_results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": str(result)}
                )
            else:
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": f"Unknown tool: {block.name}",
                        "is_error": True,
                    }
                )

        # 5. Send all tool results back in one user message, then loop to get Claude's next reply
        messages.append({"role": "user", "content": tool_results})

    raise RuntimeError("Max iterations reached, please try again.")


def main():
    """Main assistant loop"""
    print("🤖 Simple Claude Assistant with Tools")
    print("Type 'bye' or 'quit' to stop assistant\n")

    messages = []

    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("👋 Goodbye!")
            break

        # 3. Add user message to messages list
        messages.append({"role": "user", "content": user_input})

        # 4. Run the agent loop. It adds Claude's replies and tool results to `messages` for us.
        try:
            response = chat_with_bot(messages)
        except anthropic.APIError as e:
            print(f"I got an error: {e}")
            continue

        # 5. Display the text of the final response, plus the web sources it used
        assistant_text = "".join(block.text for block in response.content if block.type == "text")
        print("🤖 Assistant:", assistant_text + get_sources(response))


if __name__ == "__main__":
    main()
