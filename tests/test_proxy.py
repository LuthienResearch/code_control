from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Request

from luthien_code_control.proxy import handle_chat_completion, proxy_request


@pytest.mark.asyncio
async def test_proxy_request_missing_api_key() -> None:
    """Test proxy_request when API key is not configured"""
    mock_request = MagicMock(spec=Request)
    mock_request.method = "POST"

    with patch("luthien_code_control.proxy.get_api_key", return_value=None):
        response = await proxy_request(
            mock_request, "https://api.example.com/chat/completions"
        )
        assert response == {"error": "API key not configured on server"}


@pytest.mark.asyncio
async def test_proxy_request_unsupported_endpoint() -> None:
    """Test proxy_request with an unsupported endpoint"""
    mock_request = MagicMock(spec=Request)
    mock_request.method = "POST"
    mock_request.json = AsyncMock(return_value={})

    with patch("luthien_code_control.proxy.get_api_key", return_value="test-key"):
        response = await proxy_request(
            mock_request, "https://api.example.com/unsupported"
        )
        assert response == {"error": "Endpoint not supported: unsupported"}


@pytest.mark.asyncio
async def test_handle_chat_completion_success() -> None:
    """Test successful chat completion request"""
    mock_response = MagicMock()
    mock_response.model_dump.return_value = {
        "choices": [{"message": {"content": "Test response"}}]
    }

    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("luthien_code_control.proxy.AsyncOpenAI", return_value=mock_client):
        request_data = {
            "model": "claude-3-5-sonnet-20240620",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 100,
            "temperature": 0.7,
        }

        response = await handle_chat_completion(
            "test-key", request_data, "https://api.example.com/chat/completions"
        )

        assert "choices" in response
        assert len(response["choices"]) == 1


@pytest.mark.asyncio
async def test_handle_chat_completion_error() -> None:
    """Test chat completion request with API error"""
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))

    with patch("luthien_code_control.proxy.AsyncOpenAI", return_value=mock_client):
        request_data = {
            "model": "claude-3-5-sonnet-20240620",
            "messages": [{"role": "user", "content": "Hello"}],
        }

        response = await handle_chat_completion(
            "test-key", request_data, "https://api.example.com/chat/completions"
        )

        assert "error" in response
        assert "API request failed" in response["error"]
