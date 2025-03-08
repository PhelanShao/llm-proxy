"""
Test key generator functionality
"""

import unittest
import os
import sys

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import KeyGenerator, generate_encrypted_key
from src.models import LLMConfig, LLMProvider


class TestKeyGenerator(unittest.TestCase):
    """Test key generator functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            base_url="https://api.openai.com/v1",
            api_key="test-api-key",
            model="gpt-3.5-turbo",
            headers={"User-Agent": "TestApp/1.0"},
            extra_body={"max_tokens": 100}
        )
    
    def test_encrypt_decrypt(self):
        """Test encryption and decryption process"""
        # Encrypt configuration
        encrypted_key = KeyGenerator.encrypt_config(self.test_config)
        self.assertIsInstance(encrypted_key, str)
        
        # Decrypt configuration
        decrypted_config = KeyGenerator.decrypt_config(encrypted_key)
        self.assertIsInstance(decrypted_config, LLMConfig)
        
        # Verify decrypted configuration matches original configuration
        self.assertEqual(decrypted_config.provider, self.test_config.provider)
        self.assertEqual(decrypted_config.base_url, self.test_config.base_url)
        self.assertEqual(decrypted_config.api_key, self.test_config.api_key)
        self.assertEqual(decrypted_config.model, self.test_config.model)
        self.assertEqual(decrypted_config.headers, self.test_config.headers)
        self.assertEqual(decrypted_config.extra_body, self.test_config.extra_body)
    
    def test_generate_encrypted_key(self):
        """Test generate_encrypted_key helper function"""
        # Use helper function to generate encrypted key
        encrypted_key = generate_encrypted_key(
            provider="openai",
            base_url="https://api.openai.com/v1",
            api_key="test-api-key",
            model="gpt-3.5-turbo",
            headers={"User-Agent": "TestApp/1.0"},
            extra_body={"max_tokens": 100}
        )
        
        self.assertIsInstance(encrypted_key, str)
        
        # Verify decrypted content
        decrypted_config = KeyGenerator.decrypt_config(encrypted_key)
        self.assertEqual(decrypted_config.provider, "openai")
        self.assertEqual(decrypted_config.base_url, "https://api.openai.com/v1")
        self.assertEqual(decrypted_config.api_key, "test-api-key")
        self.assertEqual(decrypted_config.model, "gpt-3.5-turbo")
        self.assertEqual(decrypted_config.headers, {"User-Agent": "TestApp/1.0"})
        self.assertEqual(decrypted_config.extra_body, {"max_tokens": 100})


if __name__ == "__main__":
    unittest.main() 