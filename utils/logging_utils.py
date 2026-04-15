import logging
import json
from typing import Optional

class JsonFormatter(logging.Formatter):
    """
    Custom formatter to output logs in JSON format.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        try:
            return json.dumps(log_record)
        except TypeError:
            log_record["message"] = str(log_record.get("message", ""))
            return json.dumps(log_record)

def setup_logging(name: str = "SmartCitySimulator", json_format: bool = False, level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance.
    """
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    
    if json_format:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

    # Clean existing handlers to avoid duplicates
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(level)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger
