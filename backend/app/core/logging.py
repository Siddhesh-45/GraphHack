import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict
from app.core.config import settings

class JSONFormatter(logging.Formatter):
    """
    Format logs as structured JSON records for production telemetry.
    Ensures no sensitive credentials or keys are leaked in output.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "environment": settings.APP_ENV,
        }
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id"):
            log_entry["request_id"] = getattr(record, "request_id")
        return json.dumps(log_entry)

def setup_logging():
    level_name = settings.LOG_LEVEL.upper()
    level = getattr(logging, level_name, logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    if settings.APP_ENV.lower() in ("production", "staging"):
        handler.setFormatter(JSONFormatter())
    else:
        # Development readable format
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
