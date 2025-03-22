from typing import Dict, Any, Optional
import openai
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.exceptions import APIKeyError, RateLimitError
from app.models.models import Model
import time
import asyncio
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError))
)
async def get_completion(
    model: Model,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = False
) -> str:
    """
    Get completion from OpenAI API with retry logic and error handling.
    """
    if not settings.OPENAI_API_KEY:
        raise APIKeyError("OpenAI")
        
    try:
        # Extract model name from parameters
        model_name = model.parameters.get("model_name", "gpt-4")
        
        # Prepare the completion request
        completion = await client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        if stream:
            # Handle streaming response
            full_response = ""
            async for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
            return full_response
        else:
            # Handle regular response
            return completion.choices[0].message.content
            
    except openai.RateLimitError as e:
        raise RateLimitError("OpenAI")
    except openai.AuthenticationError:
        raise APIKeyError("OpenAI")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

async def get_embeddings(text: str) -> list[float]:
    """
    Get embeddings from OpenAI's embedding model.
    """
    if not settings.OPENAI_API_KEY:
        raise APIKeyError("OpenAI")
        
    try:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        raise Exception(f"Error getting embeddings: {str(e)}")

async def analyze_safety(text: str) -> Dict[str, float]:
    """
    Analyze text for safety concerns using OpenAI's moderation endpoint.
    """
    if not settings.OPENAI_API_KEY:
        raise APIKeyError("OpenAI")
        
    try:
        response = await client.moderations.create(input=text)
        
        # Extract scores from response
        scores = response.results[0].category_scores
        
        return {
            "hate": scores.hate,
            "hate_threatening": scores.hate_threatening,
            "self_harm": scores.self_harm,
            "sexual": scores.sexual,
            "sexual_minors": scores.sexual_minors,
            "violence": scores.violence,
            "violence_graphic": scores.violence_graphic
        }
    except Exception as e:
        raise Exception(f"Error analyzing safety: {str(e)}")

async def get_token_count(text: str, model: str = "gpt-4") -> int:
    """
    Get the token count for a text using tiktoken.
    """
    import tiktoken
    
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        raise Exception(f"Error counting tokens: {str(e)}")

async def estimate_cost(
    text: str,
    model: str = "gpt-4",
    is_completion: bool = True
) -> float:
    """
    Estimate the cost of an API call based on token count and model.
    """
    # Token costs per 1K tokens (as of March 2024)
    costs = {
        "gpt-4": {"input": 0.01, "output": 0.03},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
    }
    
    if model not in costs:
        raise ValueError(f"Unknown model: {model}")
        
    token_count = await get_token_count(text, model)
    cost_type = "output" if is_completion else "input"
    
    return (token_count / 1000) * costs[model][cost_type] 