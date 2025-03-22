import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

class ErrorHandler(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        try:
            response = await call_next(request)
            return response
            
        except Exception as e:
            # Log the error
            logger.exception(f"Error processing request: {str(e)}")
            
            # Return error response
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "message": str(e)
                }
            )

    async def handle_error(
        self,
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        error_id = None
        
        # Log the error
        logger.error(
            f"Error processing request: {request.url.path}",
            exc_info=exc,
            extra={
                "error_id": error_id,
                "method": request.method,
                "path": request.url.path,
                "client_host": request.client.host,
            }
        )

        # Determine status code and error message
        if hasattr(exc, "status_code"):
            status_code = exc.status_code
        else:
            status_code = 500

        error_msg = str(exc)
        if status_code == 500:
            error_msg = "Internal server error"

        response = {
            "error": {
                "code": status_code,
                "message": error_msg,
                "id": error_id
            }
        }

        return JSONResponse(
            status_code=status_code,
            content=response
        ) 