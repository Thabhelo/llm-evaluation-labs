"""
LLM Client module for managing API-based language models.
"""

from typing import Optional, Dict, Any, List
import logging
from openai import OpenAI, AsyncOpenAI
from anthropic import Anthropic
from config import settings

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for managing API-based language models."""
    
    def __init__(self):
        """Initialize LLM clients."""
        self.openai_client = None
        self.async_openai_client = None
        self.anthropic_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize API clients if credentials are available."""
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                organization=settings.OPENAI_ORG_ID,
            )
            self.async_openai_client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                organization=settings.OPENAI_ORG_ID,
            )
            logger.info("OpenAI client initialized")
        
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(
                api_key=settings.ANTHROPIC_API_KEY,
            )
            logger.info("Anthropic client initialized")
    
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs: Any,
    ) -> str:
        """Generate text using the available LLM APIs."""
        model = model or settings.DEFAULT_MODEL
        
        try:
            if "gpt" in model.lower():
                return await self._generate_openai(prompt, model, max_tokens, temperature, **kwargs)
            elif "claude" in model.lower():
                return await self._generate_anthropic(prompt, model, max_tokens, temperature, **kwargs)
            else:
                raise ValueError(f"Unsupported model: {model}")
        except Exception as e:
            logger.error(f"Error generating text with {model}: {str(e)}")
            # Try fallback model
            if model != settings.FALLBACK_MODEL:
                logger.info(f"Attempting fallback to {settings.FALLBACK_MODEL}")
                return await self.generate(
                    prompt,
                    model=settings.FALLBACK_MODEL,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    **kwargs
                )
            raise
    
    async def _generate_openai(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        **kwargs: Any,
    ) -> str:
        """Generate text using OpenAI's API."""
        if not self.async_openai_client:
            raise ValueError("OpenAI client not initialized. Please check your API key.")
        
        response = await self.async_openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )
        return response.choices[0].message.content
    
    async def _generate_anthropic(
        self,
        prompt: str,
        model: str,
        max_tokens: int,
        temperature: float,
        **kwargs: Any,
    ) -> str:
        """Generate text using Anthropic's API."""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized. Please check your API key.")
        
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text

# Global instance
llm_client = LLMClient() 