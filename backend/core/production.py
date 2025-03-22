from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.sessions import SessionMiddleware
from ..middleware.rate_limit import RateLimitMiddleware
from ..middleware.error_handler import ErrorHandler
from ..config import settings

def configure_production(app: FastAPI) -> None:
    """Configure the application for production environment."""
    
    # Security middlewares
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure based on your domain
    )
    
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.JWT_SECRET_KEY,
        max_age=3600,  # 1 hour
    )
    
    # Rate limiting
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=100,  # Requests per minute
        window=60,  # Window size in seconds
    )
    
    # Error handling
    app.add_middleware(ErrorHandler)
    
    # Compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response 