"""
定义LLM配置的数据模型
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Union
from enum import Enum


class LLMProvider(str, Enum):
    """支持的LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OPENROUTER = "openrouter"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    """LLM配置模型"""
    provider: LLMProvider
    base_url: str
    api_key: str
    model: str
    headers: Optional[Dict[str, str]] = Field(default_factory=dict)
    extra_body: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        use_enum_values = True

    @validator('provider')
    def validate_provider(cls, v):
        if isinstance(v, str) and v not in [p.value for p in LLMProvider]:
            raise ValueError(f"不支持的提供商: {v}")
        return v


class Message(BaseModel):
    """聊天消息模型"""
    role: str
    content: Union[str, List[Dict[str, Any]]]


class ChatRequest(BaseModel):
    """聊天请求模型"""
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None 