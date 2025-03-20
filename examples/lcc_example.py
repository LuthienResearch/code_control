#!/usr/bin/env python
"""
Test script for Luthien Code Control (LCC) proxy.

This script sends test requests through the LCC proxy to verify functionality.
It uses the OpenAI SDK but points it to the local LCC server.
"""
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file (look in project root by default)
project_root = Path(__file__).parents[1]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# LCC proxy URL
LCC_URL = os.getenv("LCC_URL", "http://localhost:8000")

# Get client API key (optional - the server now handles API keys)
CLIENT_API_KEY = os.getenv("CLIENT_API_KEY", "client_1234")


def create_client() -> OpenAI:
    """Create an OpenAI client pointing to the LCC proxy."""
    return OpenAI(
        base_url=LCC_URL,
        api_key=CLIENT_API_KEY,  # Just a client identifier, not the actual provider API key
        # Disable SSL verification since we're using HTTP locally
        http_client=httpx.Client(verify=False),
    )


def test_chat_completion() -> Dict[str, Any]:
    """Test chat completion API."""
    client = create_client()

    try:
        response = client.chat.completions.create(
            model="claude-3-5-sonnet-20240620",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello! What's the capital of France?"},
            ],
            max_tokens=100,
        )
        print("\n--- Chat Completion Test ---")
        print(f"Success! Response: {response.choices[0].message.content}")
        return {"success": True, "response": response.model_dump()}
    except Exception as e:
        print(f"Error in chat completion: {e}")
        return {"success": False, "error": str(e)}


def main() -> None:
    """Run all tests."""
    print(f"Testing LCC proxy at {LCC_URL}")
    print(f"Using client identifier: {CLIENT_API_KEY}")
    print("The actual provider API key is managed by the LCC server")

    # Run tests
    chat_result = test_chat_completion()

    # Summary
    print("\n=== Test Summary ===")
    print(f"Chat Completions: {'✅ Passed' if chat_result['success'] else '❌ Failed'}")


if __name__ == "__main__":
    main()
