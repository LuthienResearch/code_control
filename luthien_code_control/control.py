"""
Control module for implementing security policies.

This module is responsible for determining which requests are safe to pass on,
which should be modified, and which should be rejected.
"""

from typing import Any, Dict, Tuple, Union

from fastapi.responses import JSONResponse


def analyze_request(request_data: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Analyze a request to determine if it should be allowed, modified, or rejected.

    Args:
        request_data: The request data to analyze

    Returns:
        A tuple containing:
        - allowed: Whether the request is allowed
        - reason: The reason for allowing, modifying, or rejecting
        - modified_data: The modified request data (if any)
    """
    # Placeholder implementation - in a real system this would implement
    # security controls and policies
    return True, "Request allowed", request_data


def analyze_response(response_data: Dict[str, Any]) -> Tuple[bool, str, JSONResponse]:
    """
    Analyze a response to determine if it should be allowed, modified, or rejected.

    Args:
        response_data: The response data to analyze

    Returns:
        A tuple containing:
        - allowed: Whether the response is allowed
        - reason: The reason for allowing, modifying, or rejecting
        - modified_data: The modified response data as a JSONResponse
    """
    # Check for Anthropic error and translate it to OpenAI format if needed
    if isinstance(response_data, dict) and response_data.get("type") == "error":
        error = response_data.get("error", {})
        error_type = error.get("type", "unknown_error")
        error_message = error.get("message", "Unknown error")

        # Convert to OpenAI-compatible error format
        converted_error = {
            "error": {
                "message": f"{error_type}: {error_message}",
                "type": "invalid_request_error",
                "code": "anthropic_error",
            }
        }
        print(f"Converted Anthropic error format to OpenAI format")
        return True, "Converted error format", JSONResponse(content=converted_error)

    # If we have an Anthropic response, convert it to OpenAI format
    if (
        isinstance(response_data, dict)
        and "content" in response_data
        and "model" in response_data
    ):
        # This looks like an Anthropic Messages API response
        try:
            content_blocks = response_data.get("content", [])
            content_text = ""

            # Extract text from content blocks
            if isinstance(content_blocks, list):
                for block in content_blocks:
                    if block.get("type") == "text":
                        content_text += block.get("text", "")

            # Create OpenAI-compatible format
            openai_format = {
                "id": response_data.get("id", "chatcmpl-anthropic"),
                "object": "chat.completion",
                "created": response_data.get("stop_timestamp", 0),
                "model": response_data.get("model", "claude"),
                "usage": {
                    "prompt_tokens": response_data.get("usage", {}).get(
                        "input_tokens", 0
                    ),
                    "completion_tokens": response_data.get("usage", {}).get(
                        "output_tokens", 0
                    ),
                    "total_tokens": (
                        response_data.get("usage", {}).get("input_tokens", 0)
                        + response_data.get("usage", {}).get("output_tokens", 0)
                    ),
                },
                "choices": [
                    {
                        "message": {"role": "assistant", "content": content_text},
                        "finish_reason": response_data.get("stop_reason", "stop"),
                        "index": 0,
                    }
                ],
            }
            print("Converted Anthropic response format to OpenAI format")
            return (
                True,
                "Converted response format",
                JSONResponse(content=openai_format),
            )
        except Exception as e:
            print(f"Error converting Anthropic response to OpenAI format: {e}")
            # If conversion fails, just return the original

    # Placeholder implementation - in a real system this would implement
    # security controls and policies
    return True, "Response allowed", JSONResponse(content=response_data)
