import os
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError

load_dotenv()

class SlackMessageArgs(BaseModel):
    """Pydantic model for Slack message arguments"""
    message: str
    
    # Config is optional - without it, extra fields will cause validation errors
    # With it, extra fields are ignored making the function more robust
    class Config:
        extra = "ignore"

def send_slack_message(args: dict):
    """Send a message to Slack using a webhook URL."""
    try:
        # MUST use **args to unpack the dictionary into the Pydantic model
        # This validates the input and creates a typed object
        validated_args = SlackMessageArgs(**args)
        
        # Now you can access the validated field directly
        message = validated_args.message
    except ValidationError as e:
        return f"Invalid arguments: {e}"
    
    webhook_url = os.getenv('SLACK_WEBHOOK')
    
    if not webhook_url:
        return "Error: SLACK_WEBHOOK not set"
    
    try:
        response = requests.post(webhook_url, json={"text": message})
        response.raise_for_status()
        return f"Message sent to Slack: '{message}'"
    except requests.exceptions.RequestException as e:
        return f"Failed to send to Slack: {str(e)}"
