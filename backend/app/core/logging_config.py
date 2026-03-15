import json
import logging
import os
import sys
import uuid
from typing import Any

class RequestFormatter(logging.Formatter):
    """Custom formatter that handles missing request_id gracefully."""
    def format(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "SYSTEM"
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """Formatter that outputs JSON for production logs."""
    def format(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "SYSTEM"
        
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "request_id": record.request_id,
            "name": record.name,
            "func": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging():
    """Configures the root logger with a professional format."""
    is_json = os.getenv("LOG_FORMAT", "text").lower() == "json"
    
    handler = logging.StreamHandler(sys.stdout)
    
    if is_json:
        handler.setFormatter(JSONFormatter())
    else:
        log_format = (
            "%(asctime)s | %(levelname)-8s | ReqID: %(request_id)s | "
            "%(name)s:%(funcName)s:%(lineno)d - %(message)s"
        )
        handler.setFormatter(RequestFormatter(log_format))
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers to avoid duplicates
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
        
    root_logger.addHandler(handler)
    
    # Clean up standard FastAPI/Uvicorn/Alembic logs to match
    for log_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi", "alembic"]:
        l = logging.getLogger(log_name)
        l.handlers = [handler]
        l.propagate = False

setup_logging()
logger = logging.getLogger("app")
