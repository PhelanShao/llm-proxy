"""
密钥生成器 - 负责加密和解密LLM配置信息
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
    """LLM配置密钥生成器"""
    
    # 用于派生加密密钥的主密钥，实际部署时应该存储在安全的环境变量中
    MASTER_KEY = os.environ.get("LLM_PROXY_MASTER_KEY", "this_is_a_default_master_key_please_change_in_production")
    
    @classmethod
    def _derive_key(cls, salt: bytes) -> bytes:
        """从主密钥派生加密密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(cls.MASTER_KEY.encode()))
    
    @classmethod
    def encrypt_config(cls, config: Union[LLMConfig, Dict[str, Any]]) -> str:
        """加密LLM配置信息"""
        if isinstance(config, LLMConfig):
            config_dict = config.dict()
        else:
            config_dict = config
            
        # 生成随机盐值
        salt = secrets.token_bytes(16)
        
        # 派生加密密钥
        key = cls._derive_key(salt)
        
        # 加密配置
        f = Fernet(key)
        config_bytes = json.dumps(config_dict).encode()
        encrypted_config = f.encrypt(config_bytes)
        
        # 将盐值和加密后的配置组合在一起
        result = base64.urlsafe_b64encode(salt + encrypted_config).decode()
        return result
    
    @classmethod
    def decrypt_config(cls, encrypted_key: str) -> LLMConfig:
        """解密LLM配置信息"""
        # 解码加密的密钥
        raw_data = base64.urlsafe_b64decode(encrypted_key.encode())
        
        # 提取盐值和加密的配置
        salt, encrypted_config = raw_data[:16], raw_data[16:]
        
        # 派生加密密钥
        key = cls._derive_key(salt)
        
        # 解密配置
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
    生成加密的LLM配置密钥
    
    Args:
        provider: LLM提供商 (openai, anthropic, google 等)
        base_url: API基础URL
        api_key: API密钥
        model: 模型名称
        headers: 可选的HTTP头信息
        extra_body: 可选的额外请求体参数
        
    Returns:
        加密的配置密钥
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