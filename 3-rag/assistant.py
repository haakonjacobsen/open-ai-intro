import json
import os
from openai import NotGiven, OpenAI
from dotenv import load_dotenv
from openai.types.responses import ResponseInputParam

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def print_to_console(args: dict):
    """Print a message to the console"""
    print(args['message'])
    return f"Message {args['message']} printed to console"

tool_lookup = {
    "print_to_console": print_to_console
}

tools = [
    {
        "type": "function",
        "name": "print_to_console",
        "description": "Print a message to the console",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The message to print to the console"
                }
            },
            "required": ["message"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

def chat_with_bot(messages: str | ResponseInputParam | NotGiven):
    """Send user input to OpenAI and return the response"""
    try:
        keep_going = True
        max_iterations = 4
        iterations = 0
        while keep_going:
            response = client.responses.create(
                model="gpt-4.1",
                input=messages,
                tools=[
                    *tools,
                ],
            )
            # Check if the model wanted to call a function
            for item in response.output:
                messages.append(item)
                if item.type == 'function_call' and item.name in tool_lookup.keys():
                    try:
                        function_to_call = tool_lookup[item.name]
                        args = json.loads(item.arguments)
                        # Add the function call to the messages list
                        print('Calling function: ', item.name, ' with arguments: ', args)
                        function_result = function_to_call(args)
                        # 4. Add function call output to the messages list
                        messages.append({
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": json.dumps(function_result)
                        })
                        iterations += 1
                    except Exception as e:
                        return f"Error: {str(e)}"
                else:
                    return response
            if iterations >= max_iterations:
                return 'Max iterations reached, please try again.'
        return response
    except Exception as e:
        return 'I got an error: ' + str(e)

def main():
    """Main chatbot loop"""
    print("🤖 Simple OpenAI Assistant with Tools")
    print("Type 'bye' or 'quit' to stop assistant\n")

    messsages = [
        {
            "role": "developer",
            "content": "You are a helpful assitant with access to tools, to help the user with their requests."
        }
    ]
    
    while True:
        # 1. Get user input
        user_input = input("🫵 User: ").strip()

        # 2. Check if user wants to quit
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        # 3. Add user message to messages list
        messsages.append({
            "role": "user",
            "content": user_input
        })

        # 4. Get assistant response
        bot_response = chat_with_bot(messsages)
        
        # 6. Show sources used in web search
        assistant_answer = bot_response.output[0].content[0].text

        # 5. Display the response
        print("🤖 Assistant:", assistant_answer)
        
        
        # 7. Add to conversation history
        messsages.append({
            "role": "assistant",
            "content": assistant_answer
        })

if __name__ == "__main__":
    main()
