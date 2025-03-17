"""
Proxy module for handling API requests.

This module is responsible for proxying requests to the OpenAI API
and applying security controls.
"""
from typing import Any, Dict

import httpx
from fastapi import Request


async def proxy_request(request: Request, target_url: str) -> Dict[str, Any]:
    """
    Proxy a request to the target URL.
    
    Args:
        request: The incoming FastAPI request
        target_url: The target URL to proxy the request to
        
    Returns:
        The response from the target URL
    """
    from luthien_code_control.config import get_api_key, get_auth_header
    
    # Get the request body
    body = await request.json()
    
    # Get headers, but exclude host which will be set by httpx
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    # Add API key from config if available and not already in headers
    api_key = get_api_key()
    auth_header = get_auth_header()
    
    if api_key and auth_header.lower() not in {k.lower(): True for k in headers}:
        headers[auth_header] = api_key
    
    # Forward the request to the target URL
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            json=body,
            headers=headers,
        )
        
    # Return the response as a dictionary
    return response.json()