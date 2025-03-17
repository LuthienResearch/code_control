"""Tests for the proxy module."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request

from luthien_code_control import proxy


@pytest.mark.asyncio
async def test_proxy_request():
    """Test the proxy_request function."""
    # Create a mock request
    mock_request = AsyncMock(spec=Request)
    mock_request.method = "POST"
    mock_request.headers = {"Content-Type": "application/json", "Authorization": "Bearer test"}
    mock_request.json = AsyncMock(return_value={"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]})
    
    # Create expected response data
    response_data = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "model": "gpt-4",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello there! How can I help you today?",
                },
                "finish_reason": "stop",
            }
        ],
    }
    
    # Create a mock response that's not an AsyncMock
    mock_response = MagicMock()
    mock_response.json.return_value = response_data
    
    # Patch the httpx client
    with patch("httpx.AsyncClient") as mock_client:
        mock_client_instance = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        mock_client_instance.request.return_value = mock_response
        
        # Call the function
        result = await proxy.proxy_request(mock_request, "https://api.example.com/v1/chat/completions")
        
        # Check the result
        assert result == response_data
        
        # Check that the client was called correctly
        mock_client_instance.request.assert_called_once()