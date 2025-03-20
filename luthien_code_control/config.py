"""
Configuration module for Luthien Code Control.

This module contains configuration settings for the LCC application.
"""

import os
from typing import Optional

# Default API URL (Anthropic API with OpenAI compatibility)
DEFAULT_TARGET_URL = "https://api.anthropic.com/v1"

# Get target URL from environment variable, or use default
TARGET_URL = os.getenv("LCC_TARGET_URL", DEFAULT_TARGET_URL)

# API Key configuration
API_KEY = os.getenv("LCC_API_KEY")
API_KEY_ENV = os.getenv("LCC_API_KEY_ENV", "ANTHROPIC_API_KEY")
API_KEY_HEADER = os.getenv("LCC_API_KEY_HEADER", "x-api-key")

# Default values for various providers
API_PROVIDER = os.getenv("LCC_API_PROVIDER", "anthropic")
DEFAULT_HEADER_MAP = {
    "anthropic": "x-api-key",
    "anthropic-openai": "Authorization",  # For OpenAI compatibility endpoint
    "openai": "Authorization",
}


# Function to get the API key - first check LCC_API_KEY, then the provider-specific env var
def get_api_key() -> Optional[str]:
    """
    Get the API key for the target API.

    Returns:
        The API key if found, None otherwise
    """
    if API_KEY:
        return API_KEY

    # If LCC_API_KEY isn't set, try the provider-specific env var
    provider_key = os.getenv(API_KEY_ENV)
    if provider_key:
        # For OpenAI, prepend 'Bearer ' if not already present
        if API_PROVIDER.lower() == "openai" and not provider_key.startswith("Bearer "):
            return f"Bearer {provider_key}"
        return provider_key

    return None


# Function to get the appropriate header name for the API key
def get_auth_header() -> str:
    """
    Get the appropriate authorization header name for the API provider.

    Returns:
        The header name to use for the API key
    """
    return API_KEY_HEADER or DEFAULT_HEADER_MAP.get(API_PROVIDER.lower(), "x-api-key")


# Configuration for logging
LOG_LEVEL = os.getenv("LCC_LOG_LEVEL", "INFO")
