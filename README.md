# Luthien Code Control

Luthien Code Control (LCC) is a proof-of-concept AI Control application. It works by proxying all requests to and from an OpenAI-API-compatible endpoint, implementing strategies to determine which requests are safe to pass on, which should be modified, and which should be rejected.

## Project Structure

```
luthien_code_control/
├── luthien_code_control/
│   ├── __init__.py
│   ├── config.py       # Configuration settings
│   ├── control.py      # Security control implementation
│   ├── main.py         # FastAPI application entrypoint
│   └── proxy.py        # Request proxying logic
├── tests/
│   ├── __init__.py
│   ├── conftest.py     # Pytest fixtures
│   ├── test_control.py # Tests for control module
│   ├── test_main.py    # Tests for main module
│   └── test_proxy.py   # Tests for proxy module
├── README.md
└── pyproject.toml      # Poetry configuration
```

## Features

- Proxies requests to OpenAI-compatible API endpoints
- Analyzes and controls both requests and responses
- Configurable through environment variables
- Simple API-compatible interface

## Installation

```bash
# Clone the repository
git clone https://github.com/jaidhyani/luthien-code-control.git
cd luthien-code-control

# Install dependencies
poetry install
```

## Usage

```bash
# Start the server
poetry run python -m luthien_code_control.main
```

By default, the server starts on port 8000. You can modify the target API URL using the `LCC_TARGET_URL` environment variable.

## Configuration

The application can be configured using environment variables:

- `LCC_TARGET_URL`: The target OpenAI-compatible API URL (default: https://api.openai.com/v1)
- `LCC_LOG_LEVEL`: The log level (default: INFO)

## Development

```bash
# Install development dependencies
poetry install

# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Run type checking
poetry run mypy .

# Format code
poetry run black . && poetry run isort .
```

## License

[MIT](LICENSE)