# LLM Proxy Platform

A secure LLM proxy platform that allows users to encrypt and use API configurations from different LLM service providers.

## Features

- Encrypt API configurations (base URL, model, API key, etc.) from various LLM providers into a single string
- Automatically set environment variables for LLM service access using the encrypted configuration string
- Gradio-based testing dialogue platform for configuration validation and LLM interaction testing
- Gradio-based key generation interface for easy creation of encrypted configuration keys

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install as a package (development mode)
pip install -e .
```

## Usage

### Generate Encrypted Configuration with GUI

```bash
# Launch the key generation interface
python generate_key.py
```

Or run directly:

```bash
python -m src.key_generator_app
```

### Generate Encrypted Configuration through Code

```python
from src.key_generator import generate_encrypted_key

# Generate encrypted configuration key
encrypted_key = generate_encrypted_key(
    provider="openai",
    base_url="https://api.openai.com/v1",
    api_key="your-api-key",
    model="gpt-3.5-turbo"
)
print(f"Encrypted configuration key: {encrypted_key}")
```

### Access LLM with Encrypted Configuration

```python
from src.llm_proxy import LLMProxy

# Initialize proxy
proxy = LLMProxy(encrypted_key="your-encrypted-key")

# Send message
response = proxy.send_message("Hello, world!")
print(response)
```

### Launch Dialogue Testing Interface

```bash
# Launch dialogue testing interface
python chat_app.py
```

Or run directly:

```bash
python -m src.app
```

## Development

### Run Tests

```bash
python -m unittest discover tests
```

### Generate Keys with Command Line Tool

```bash
python examples/generate_key.py --provider openai --base-url https://api.openai.com/v1 --api-key your-api-key --model gpt-3.5-turbo
```

## License

MIT 