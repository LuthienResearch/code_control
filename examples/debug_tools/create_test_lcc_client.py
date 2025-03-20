#!/usr/bin/env python
"""
Simple LCC test client that directly uses httpx.

This script bypasses the OpenAI SDK to help debug raw HTTP interactions.
"""
import asyncio
import json
import os

import httpx

# Base URL of LCC proxy
LCC_URL = "http://localhost:8000"

# API key (we'll use a dummy one since the server should handle the real key)
API_KEY = "client_1234"


async def test_direct_request() -> None:
    """Test a direct API request to the LCC server."""
    # Create a chat completions request
    url = f"{LCC_URL}/chat/completions"

    # Request data
    data = {
        "model": "claude-3-5-sonnet-20240620",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! What's the capital of France?"},
        ],
        "max_tokens": 100,
    }

    # Headers
    headers = {
        "Content-Type": "application/json",
        # We're using a dummy key since the server should inject its own
        "Authorization": f"Bearer {API_KEY}",
    }

    print(f"Sending request to: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {json.dumps(data, indent=2)}")

    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(
                url=url, json=data, headers=headers, timeout=30.0
            )

            # Print response details
            print(f"\nResponse status: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")

            try:
                response_json = response.json()
                print(f"Response body: {json.dumps(response_json, indent=2)}")
            except Exception as e:
                print(f"Failed to parse response as JSON: {e}")
                print(f"Raw response: {response.text}")

    except Exception as e:
        print(f"Request failed: {e}")


async def main() -> None:
    """Run the test."""
    await test_direct_request()


if __name__ == "__main__":
    asyncio.run(main())
