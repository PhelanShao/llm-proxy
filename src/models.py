"""
Define data models for LLM configuration
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List, Union
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OPENROUTER = "openrouter"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    """LLM configuration model"""
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
            raise ValueError(f"Unsupported provider: {v}")
        return v


class Message(BaseModel):
    """Chat message model"""
    role: str
    content: Union[str, List[Dict[str, Any]]]


class ChatRequest(BaseModel):
    """Chat request model"""
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None 