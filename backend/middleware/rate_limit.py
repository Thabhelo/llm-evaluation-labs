from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from cachetools import TTLCache
from ..config import settings

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        max_requests: int = 100,
        window: int = 60,
    ):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.cache = TTLCache(maxsize=10000, ttl=window)

    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limit
        if client_ip in self.cache:
            self.cache[client_ip] += 1
            if self.cache[client_ip] > self.max_requests:
                return Response(
                    content="Rate limit exceeded",
                    status_code=429,
                )
        else:
            self.cache[client_ip] = 1
        
        # Process the request
        response = await call_next(request)
        return response 