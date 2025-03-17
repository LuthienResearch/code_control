# LCC Debug Tools

This directory contains utilities for debugging and testing the Luthien Code Control server.

## Tools

- `create_test_lcc_client.py`: A low-level HTTP client that sends requests directly to the LCC server without using the OpenAI SDK. Useful for debugging raw HTTP interactions.

- `debug_lcc.py`: A utility that checks the LCC configuration and environment variables to verify the setup.

## Usage

Run these tools from the project root:

```bash
# Run the debug configuration utility
poetry run python examples/debug_tools/debug_lcc.py

# Run the test client
poetry run python examples/debug_tools/create_test_lcc_client.py
```

These tools are primarily for development and troubleshooting, not for regular use.