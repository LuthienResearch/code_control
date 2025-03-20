"""Tests for the control module."""

import pytest
from fastapi.responses import JSONResponse

from luthien_code_control import control


def test_analyze_request() -> None:
    """Test the analyze_request function."""
    request_data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "Hello"}],
    }
    allowed, reason, modified_data = control.analyze_request(request_data)

    # Basic test for now - just make sure it doesn't crash
    assert allowed is True
    assert reason == "Request allowed"
    assert modified_data == request_data


def test_analyze_response() -> None:
    """Test the analyze_response function with a chat completion response."""
    response_data = {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-4",
        "system_fingerprint": "fp_44709d6fcb",
        "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello there! How can I help you today?",
                },
                "logprobs": None,
                "finish_reason": "stop",
            }
        ],
    }
    allowed, reason, modified_data = control.analyze_response(response_data)

    # Basic test for now - just make sure it doesn't crash
    assert allowed is True
    assert reason == "Response allowed"
    assert isinstance(modified_data, JSONResponse)
    assert modified_data.body == JSONResponse(content=response_data).body
