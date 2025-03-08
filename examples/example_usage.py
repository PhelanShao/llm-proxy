"""
Example Script - Demonstrate LLM proxy usage
"""

import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import generate_encrypted_key
from src.llm_proxy import LLMProxy


def main():
    """Demonstrate LLM proxy usage flow"""
    print("1. Generate encrypted configuration key")
    # Note: In actual usage, you should use a real API key
    encrypted_key = generate_encrypted_key(
        provider="openai",
        base_url="https://api.openai.com/v1",
        api_key="sk-your-openai-api-key",
        model="gpt-3.5-turbo"
    )
    print(f"Encrypted configuration key: {encrypted_key}")
    
    # In actual applications, the encrypted key would be transmitted through secure channels to application developers
    # Developers don't need to know the original API key
    
    print("\n2. Initialize LLM proxy with encrypted key")
    try:
        # In actual usage, you should use the key generated above
        # But since we are using an example API key, this will fail
        proxy = LLMProxy(encrypted_key)
        print("LLM proxy initialized successfully")
        
        print("\n3. Send message to LLM")
        response = proxy.send_message("Hello, world!")
        print(f"LLM response: {response}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Note: Since we used an example API key, this error is expected. In actual applications with valid API keys, this issue would not occur.")
    
    print("\nExample explanation:")
    print("1. In actual applications, configuration key generation is typically done by service administrators")
    print("2. The generated encrypted key can be safely shared with application developers")
    print("3. Application developers use the encrypted key without needing to know the original API configuration")
    print("4. This approach protects API keys and other sensitive configuration information")


if __name__ == "__main__":
    main() 