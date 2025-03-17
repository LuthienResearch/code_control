"""
Proxy module for handling API requests.

This module is responsible for proxying requests to the API
and applying security controls.
"""
from typing import Any, Dict, Optional
import json
import asyncio

from fastapi import Request
from openai import AsyncOpenAI, OpenAI

from luthien_code_control.config import get_api_key, get_auth_header


async def proxy_request(request: Request, target_url: str) -> Dict[str, Any]:
    """
    Proxy a request to the target API using the OpenAI client.
    
    Args:
        request: The incoming FastAPI request
        target_url: The target URL to proxy the request to
        
    Returns:
        The response from the target API
    """
    # Get API key from config
    api_key = get_api_key()
    if not api_key:
        return {"error": "API key not configured on server"}
    
    # Get request path and data
    path_parts = target_url.split("/")
    endpoint = path_parts[-1] if path_parts else ""
    
    try:
        # Parse request body
        request_data = await request.json() if request.method in ["POST", "PUT"] else {}
        
        if endpoint == "chat/completions":
            # Handle chat completions
            return await handle_chat_completion(api_key, request_data, target_url)
        else:
            # For other endpoints, use a generic approach
            return {"error": f"Endpoint not supported: {endpoint}"}
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {"error": f"Error processing request: {str(e)}"}


async def handle_chat_completion(api_key: str, request_data: Dict[str, Any], target_url: str) -> Dict[str, Any]:
    """Handle a chat completion request."""
    # Extract parameters from request
    model = request_data.get("model", "claude-3-5-sonnet-20240620")
    messages = request_data.get("messages", [])
    max_tokens = request_data.get("max_tokens", 1024)
    temperature = request_data.get("temperature", 0.7)
    
    # Extract any additional parameters
    extra_params = {k: v for k, v in request_data.items() 
                   if k not in ["model", "messages", "max_tokens", "temperature"]}
    
    print(f"Forwarding chat completion request for model: {model}")
    print(f"Using API base URL: {target_url.rsplit('/', 1)[0]}")
    
    # Create an AsyncOpenAI client
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=target_url.rsplit('/', 1)[0] + "/",  # Get base URL without the endpoint
    )
    
    try:
        # Make the request to the API
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **extra_params  # Include any additional parameters
        )
        
        # Convert response to dict and return
        response_dict = response.model_dump()
        print(f"Response received with {len(response_dict.get('choices', []))} choices")
        return response_dict
        
    except Exception as e:
        print(f"Error in chat completion: {str(e)}")
        return {"error": f"API request failed: {str(e)}"}