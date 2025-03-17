"""Tests for the control module."""
import pytest

from luthien_code_control import control


def test_analyze_request():
    """Test the analyze_request function."""
    request_data = {"model": "gpt-4", "messages": [{"role": "user", "content": "Hello"}]}
    allowed, reason, modified_data = control.analyze_request(request_data)
    
    # Basic test for now - just make sure it doesn't crash
    assert allowed is True
    assert reason == "Request allowed"
    assert modified_data == request_data


def test_analyze_response():
    """Test the analyze_response function."""
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
    allowed, reason, modified_data = control.analyze_response(response_data)
    
    # Basic test for now - just make sure it doesn't crash
    assert allowed is True
    assert reason == "Response allowed"
    assert modified_data == response_data