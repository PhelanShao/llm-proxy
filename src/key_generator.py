"""
Key Generator - Responsible for encrypting and decrypting LLM configuration information
"""

import base64
import json
import os
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Dict, Any, Optional, Union

from .models import LLMConfig, LLMProvider


class KeyGenerator:
    """LLM configuration key generator"""
    
    # Master key used to derive encryption key, should be stored in a secure environment variable in production
    MASTER_KEY = os.environ.get("LLM_PROXY_MASTER_KEY", "this_is_a_default_master_key_please_change_in_production")
    
    @classmethod
    def _derive_key(cls, salt: bytes) -> bytes:
        """Derive encryption key from master key"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(cls.MASTER_KEY.encode()))
    
    @classmethod
    def encrypt_config(cls, config: Union[LLMConfig, Dict[str, Any]]) -> str:
        """Encrypt LLM configuration information"""
        if isinstance(config, LLMConfig):
            config_dict = config.dict()
        else:
            config_dict = config
            
        # Generate random salt
        salt = secrets.token_bytes(16)
        
        # Derive encryption key
        key = cls._derive_key(salt)
        
        # Encrypt configuration
        f = Fernet(key)
        config_bytes = json.dumps(config_dict).encode()
        encrypted_config = f.encrypt(config_bytes)
        
        # Combine salt and encrypted configuration
        result = base64.urlsafe_b64encode(salt + encrypted_config).decode()
        return result
    
    @classmethod
    def decrypt_config(cls, encrypted_key: str) -> LLMConfig:
        """Decrypt LLM configuration information"""
        # Decode encrypted key
        raw_data = base64.urlsafe_b64decode(encrypted_key.encode())
        
        # Extract salt and encrypted configuration
        salt, encrypted_config = raw_data[:16], raw_data[16:]
        
        # Derive encryption key
        key = cls._derive_key(salt)
        
        # Decrypt configuration
        f = Fernet(key)
        decrypted_config = f.decrypt(encrypted_config)
        config_dict = json.loads(decrypted_config)
        
        return LLMConfig(**config_dict)


def generate_encrypted_key(
    provider: str,
    base_url: str,
    api_key: str,
    model: str,
    headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, Any]] = None
) -> str:
    """
    Generate encrypted LLM configuration key
    
    Args:
        provider: LLM provider (openai, anthropic, google, etc.)
        base_url: API base URL
        api_key: API key
        model: Model name
        headers: Optional HTTP headers
        extra_body: Optional extra request body parameters
        
    Returns:
        Encrypted configuration key
    """
    config = LLMConfig(
        provider=provider,
        base_url=base_url,
        api_key=api_key,
        model=model,
        headers=headers or {},
        extra_body=extra_body or {}
    )
    
    return KeyGenerator.encrypt_config(config) 