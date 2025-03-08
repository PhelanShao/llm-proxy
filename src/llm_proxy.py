"""
LLM代理 - 负责处理与各种LLM供应商的通信
"""

import os
from typing import Dict, List, Any, Optional, Union
import openai
from openai import OpenAI
from dotenv import load_dotenv

from .key_generator import KeyGenerator
from .models import LLMConfig, LLMProvider, Message, ChatRequest

load_dotenv()


class LLMProxy:
    """LLM代理类，处理与LLM服务提供商的通信"""
    
    def __init__(self, encrypted_key: str):
        """
        初始化LLM代理
        
        Args:
            encrypted_key: 加密的LLM配置密钥
        """
        self.config = KeyGenerator.decrypt_config(encrypted_key)
        self._setup_client()
    
    def _setup_client(self):
        """根据配置设置适当的客户端"""
        if self.config.provider == LLMProvider.OPENAI.value:
            self.client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
            )
        elif self.config.provider == LLMProvider.ANTHROPIC.value:
            # 这里需要导入Anthropic客户端
            # 为简化示例，我们暂时只实现OpenAI接口
            raise NotImplementedError("Anthropic客户端尚未实现")
        elif self.config.provider == LLMProvider.GOOGLE.value:
            # 这里需要导入Google客户端
            # 为简化示例，我们暂时只实现OpenAI接口
            raise NotImplementedError("Google客户端尚未实现")
        elif self.config.provider == LLMProvider.OPENROUTER.value:
            # OpenRouter实际上使用OpenAI兼容接口
            self.client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
            )
        else:
            raise ValueError(f"不支持的提供商: {self.config.provider}")
    
    def send_message(self, message: str, model: Optional[str] = None) -> str:
        """
        发送单条消息到LLM并获取响应
        
        Args:
            message: 用户消息
            model: 可选的模型名称，如果不提供则使用配置中的默认模型
            
        Returns:
            LLM的响应文本
        """
        return self.chat([{"role": "user", "content": message}], model)
    
    def chat(self, 
             messages: List[Dict[str, Any]], 
             model: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> str:
        """
        发送聊天消息到LLM并获取响应
        
        Args:
            messages: 消息列表
            model: 可选的模型名称
            temperature: 温度参数
            max_tokens: 最大生成token数
            
        Returns:
            LLM的响应文本
        """
        model = model or self.config.model
        
        if self.config.provider in [LLMProvider.OPENAI.value, LLMProvider.OPENROUTER.value]:
            # 构建请求参数
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            # 添加max_tokens如果有提供
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
                
            # 添加额外的请求体参数
            if self.config.extra_body:
                kwargs.update(self.config.extra_body)
                
            # 添加额外的头信息
            extra_headers = {}
            if self.config.headers:
                extra_headers = self.config.headers
                
            # 发送请求
            completion = self.client.chat.completions.create(
                **kwargs,
                extra_headers=extra_headers
            )
            
            # 返回响应文本
            return completion.choices[0].message.content
        else:
            raise NotImplementedError(f"尚未实现{self.config.provider}的聊天功能") 