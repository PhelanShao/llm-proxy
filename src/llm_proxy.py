"""
LLM Proxy - Responsible for handling communication with various LLM providers
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
    """LLM proxy class, handles communication with LLM service providers"""
    
    def __init__(self, encrypted_key: str):
        """
        Initialize LLM proxy
        
        Args:
            encrypted_key: Encrypted LLM configuration key
        """
        self.config = KeyGenerator.decrypt_config(encrypted_key)
        self._setup_client()
    
    def _setup_client(self):
        """Set up appropriate client based on configuration"""
        if self.config.provider == LLMProvider.OPENAI.value:
            self.client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
            )
        elif self.config.provider == LLMProvider.ANTHROPIC.value:
            # Need to import Anthropic client here
            # For simplicity, we only implement OpenAI interface for now
            raise NotImplementedError("Anthropic client not yet implemented")
        elif self.config.provider == LLMProvider.GOOGLE.value:
            # Need to import Google client here
            # For simplicity, we only implement OpenAI interface for now
            raise NotImplementedError("Google client not yet implemented")
        elif self.config.provider == LLMProvider.OPENROUTER.value:
            # OpenRouter actually uses OpenAI-compatible interface
            self.client = OpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
            )
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")
    
    def send_message(self, message: str, model: Optional[str] = None) -> str:
        """
        Send a single message to the LLM and get a response
        
        Args:
            message: User message
            model: Optional model name, if not provided uses default model from configuration
            
        Returns:
            LLM response text
        """
        return self.chat([{"role": "user", "content": message}], model)
    
    def chat(self, 
             messages: List[Dict[str, Any]], 
             model: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> str:
        """
        Send chat messages to LLM and get a response
        
        Args:
            messages: List of messages
            model: Optional model name
            temperature: Temperature parameter
            max_tokens: Maximum tokens to generate
            
        Returns:
            LLM response text
        """
        model = model or self.config.model
        
        if self.config.provider in [LLMProvider.OPENAI.value, LLMProvider.OPENROUTER.value]:
            # Build request parameters
            kwargs = {
                "model": model,
                "messages": messages,
                "temperature": temperature
            }
            
            # Add max_tokens if provided
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens
                
            # Add extra request body parameters
            if self.config.extra_body:
                kwargs.update(self.config.extra_body)
                
            # Add extra headers
            extra_headers = {}
            if self.config.headers:
                extra_headers = self.config.headers
                
            # Send request
            completion = self.client.chat.completions.create(
                **kwargs,
                extra_headers=extra_headers
            )
            
            # Return response text
            return completion.choices[0].message.content
        else:
            raise NotImplementedError(f"Chat functionality not yet implemented for {self.config.provider}") 