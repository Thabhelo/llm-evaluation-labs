"""
LLM API endpoints for text generation.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from models.llm_client import llm_client
from config import settings

router = APIRouter(prefix="/llm", tags=["llm"])

class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    text: str
    model: str

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using the configured LLM."""
    try:
        text = await llm_client.generate(
            prompt=request.prompt,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return GenerateResponse(
            text=text,
            model=request.model or settings.DEFAULT_MODEL,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating text: {str(e)}"
        ) 