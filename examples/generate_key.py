"""
Example Script - Generate encrypted LLM configuration key
"""

import os
import sys
import argparse

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import generate_encrypted_key


def main():
    """Parse command line arguments and generate encrypted LLM configuration key"""
    parser = argparse.ArgumentParser(description='Generate encrypted LLM configuration key')
    
    parser.add_argument('--provider', required=True, choices=['openai', 'anthropic', 'google', 'openrouter', 'custom'],
                      help='LLM provider (openai, anthropic, google, openrouter, custom)')
    parser.add_argument('--base-url', required=True, help='API base URL')
    parser.add_argument('--api-key', required=True, help='API key')
    parser.add_argument('--model', required=True, help='Model name')
    parser.add_argument('--header', action='append', help='Optional HTTP header (format: key=value)')
    parser.add_argument('--extra-body', action='append', help='Optional extra request body parameter (format: key=value)')
    
    args = parser.parse_args()
    
    # Process headers
    headers = {}
    if args.header:
        for header in args.header:
            key, value = header.split('=', 1)
            headers[key] = value
    
    # Process extra request body parameters
    extra_body = {}
    if args.extra_body:
        for param in args.extra_body:
            key, value = param.split('=', 1)
            # Try to convert to appropriate type
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit():
                value = float(value)
            extra_body[key] = value
    
    # Generate encrypted configuration key
    encrypted_key = generate_encrypted_key(
        provider=args.provider,
        base_url=args.base_url,
        api_key=args.api_key,
        model=args.model,
        headers=headers,
        extra_body=extra_body
    )
    
    print(f"Encrypted configuration key: {encrypted_key}")


if __name__ == "__main__":
    main() 