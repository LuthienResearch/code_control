#!/usr/bin/env python
"""
Debug script for Luthien Code Control.

This script tests API key functionality directly.
"""
import os
from luthien_code_control.config import get_api_key, get_auth_header, TARGET_URL

def debug_config():
    """Debug the configuration."""
    print("=== LCC Configuration Debug ===")
    print(f"Target URL: {TARGET_URL}")
    
    # Check API key
    api_key = get_api_key()
    auth_header = get_auth_header()
    
    if api_key:
        # Show only parts of the key for security
        masked_key = f"{api_key[:5]}...{api_key[-4:]}" if len(api_key) > 10 else "[too short]"
        print(f"API Key: {masked_key}")
    else:
        print("API Key: Not found")
    
    print(f"Auth Header: {auth_header}")
    
    # Environment variables
    print("\nRelevant Environment Variables:")
    for var in ["LCC_API_KEY", "LCC_API_KEY_ENV", "LCC_API_KEY_HEADER", 
                "LCC_API_PROVIDER", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        val = os.environ.get(var)
        if val:
            # Don't show actual API keys
            if "API_KEY" in var and val:
                masked_val = f"{val[:5]}...{val[-4:]}" if len(val) > 10 else "[too short]"
                print(f"  {var}: {masked_val}")
            else:
                print(f"  {var}: {val}")
        else:
            print(f"  {var}: Not set")

if __name__ == "__main__":
    debug_config()