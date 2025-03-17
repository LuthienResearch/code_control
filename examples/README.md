# Luthien Code Control Examples

This directory contains example code and configuration for using Luthien Code Control (LCC).

## Examples

- `test_lcc.py`: Test script for sending requests through the LCC proxy using the OpenAI SDK
- `simple_test.py`: Direct test of Anthropic's API using the OpenAI SDK (without the LCC proxy)
- `.env.example`: Example environment variable configuration

## Debug Tools

The `debug_tools` directory contains additional utilities for debugging and testing:

- `create_test_lcc_client.py`: Low-level HTTP client for testing the LCC proxy
- `debug_lcc.py`: Utility to check configuration and environment variables

## Usage

1. Copy the `.env.example` file to a `.env` file in the project root:
   ```bash
   cp examples/.env.example .env
   ```

2. Add your API keys and customize settings as needed.

3. Run the example scripts with Poetry:
   ```bash
   # Start the LCC server
   poetry run python -m luthien_code_control.main
   
   # In another terminal, run the test client
   poetry run python examples/test_lcc.py
   ```

## Using the OpenAI SDK with Anthropic

Both examples show how to use the OpenAI SDK with Anthropic's API:

1. Direct approach (using Anthropic's API directly):
   ```python
   client = OpenAI(
       api_key=api_key,  # Your Anthropic API key
       base_url="https://api.anthropic.com/v1/",  # Anthropic's API
   )
   ```

2. Through the LCC proxy:
   ```python
   client = OpenAI(
       api_key=client_api_key,  # Just a client identifier
       base_url="http://localhost:8000/",  # LCC proxy
   )
   ```