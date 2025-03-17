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
    # Get the request body
    body = await request.json()
    
    # Get headers, but exclude host which will be set by httpx
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
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