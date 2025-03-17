"""
Configuration module for Luthien Code Control.

This module contains configuration settings for the LCC application.
"""
import os

# Default API URL (Anthropic OpenAI-compatible API)
DEFAULT_TARGET_URL = "https://api.anthropic.com/v1"

# Get target URL from environment variable, or use default
TARGET_URL = os.getenv("LCC_TARGET_URL", DEFAULT_TARGET_URL)

# Configuration for logging
LOG_LEVEL = os.getenv("LCC_LOG_LEVEL", "INFO")
