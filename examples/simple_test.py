#!/usr/bin/env python
"""
Direct test of Anthropic's OpenAI compatible API.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

# Create a client
client = OpenAI(
    api_key=api_key,  # Anthropic API key
    base_url="https://api.anthropic.com/v1/",  # Anthropic's API endpoint
)

# Make a request
response = client.chat.completions.create(
    model="claude-3-5-sonnet-20240620",  # Anthropic model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello! What's the capital of France?"}
    ],
    max_tokens=100,
)

# Print the response
print(response)
print("\nContent:", response.choices[0].message.content)