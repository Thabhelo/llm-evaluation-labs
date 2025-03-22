import logging
import sys
from typing import Any, Dict
import json
from datetime import datetime
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from ..config import settings

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if record.stack_info:
            log_data["stack_info"] = self.formatStack(record.stack_info)

        # Add any extra attributes
        for key, value in record.__dict__.items():
            if key not in ["timestamp", "level", "message", "module", "function", 
                         "line", "request_id", "exc_info", "stack_info", "created", 
                         "msecs", "relativeCreated", "levelno", "levelname", "msg", 
                         "args", "exc_text", "name", "pathname", "filename", 
                         "lineno", "funcName", "asctime"]:
                log_data[key] = value

        return json.dumps(log_data)

def setup_logging() -> None:
    # Configure Sentry if DSN is provided
    if settings.SENTRY_DSN:
        sentry_logging = LoggingIntegration(
            level=logging.INFO,
            event_level=logging.ERROR
        )
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[sentry_logging],
            environment=settings.ENVIRONMENT,
            traces_sample_rate=1.0,
        )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # Set levels for third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING) 