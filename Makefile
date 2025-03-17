.PHONY: install test lint format check run clean

# Install dependencies
install:
	poetry install

# Run tests
test:
	poetry run pytest

# Run tests with coverage
test-cov:
	poetry run pytest --cov=luthien_code_control

# Lint the code
lint:
	poetry run ruff check .

# Format the code
format:
	poetry run black .
	poetry run isort .

# Type check
check:
	poetry run mypy .

# Run the server
run:
	poetry run python -m luthien_code_control.main

# Clean build artifacts
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build