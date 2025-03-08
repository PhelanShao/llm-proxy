"""
测试密钥生成器功能
"""

import unittest
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.key_generator import KeyGenerator, generate_encrypted_key
from src.models import LLMConfig, LLMProvider


class TestKeyGenerator(unittest.TestCase):
    """测试密钥生成器功能"""
    
    def setUp(self):
        """设置测试环境"""
        self.test_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            base_url="https://api.openai.com/v1",
            api_key="test-api-key",
            model="gpt-3.5-turbo",
            headers={"User-Agent": "TestApp/1.0"},
            extra_body={"max_tokens": 100}
        )
    
    def test_encrypt_decrypt(self):
        """测试加密和解密过程"""
        # 加密配置
        encrypted_key = KeyGenerator.encrypt_config(self.test_config)
        self.assertIsInstance(encrypted_key, str)
        
        # 解密配置
        decrypted_config = KeyGenerator.decrypt_config(encrypted_key)
        self.assertIsInstance(decrypted_config, LLMConfig)
        
        # 验证解密后的配置是否与原始配置一致
        self.assertEqual(decrypted_config.provider, self.test_config.provider)
        self.assertEqual(decrypted_config.base_url, self.test_config.base_url)
        self.assertEqual(decrypted_config.api_key, self.test_config.api_key)
        self.assertEqual(decrypted_config.model, self.test_config.model)
        self.assertEqual(decrypted_config.headers, self.test_config.headers)
        self.assertEqual(decrypted_config.extra_body, self.test_config.extra_body)
    
    def test_generate_encrypted_key(self):
        """测试生成加密密钥函数"""
        # 使用辅助函数生成加密密钥
        encrypted_key = generate_encrypted_key(
            provider="openai",
            base_url="https://api.openai.com/v1",
            api_key="test-api-key",
            model="gpt-3.5-turbo",
            headers={"User-Agent": "TestApp/1.0"},
            extra_body={"max_tokens": 100}
        )
        
        self.assertIsInstance(encrypted_key, str)
        
        # 验证解密后的内容
        decrypted_config = KeyGenerator.decrypt_config(encrypted_key)
        self.assertEqual(decrypted_config.provider, "openai")
        self.assertEqual(decrypted_config.base_url, "https://api.openai.com/v1")
        self.assertEqual(decrypted_config.api_key, "test-api-key")
        self.assertEqual(decrypted_config.model, "gpt-3.5-turbo")
        self.assertEqual(decrypted_config.headers, {"User-Agent": "TestApp/1.0"})
        self.assertEqual(decrypted_config.extra_body, {"max_tokens": 100})


if __name__ == "__main__":
    unittest.main() 