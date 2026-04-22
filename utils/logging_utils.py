import logging
import json
import os
from logging.handlers import RotatingFileHandler
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

def setup_logging(
    name: str = "SmartCitySimulator", 
    json_format: bool = False, 
    level: int = logging.INFO,
    log_file: Optional[str] = "simulator.log"
) -> logging.Logger:
    """
    Configures and returns a logger instance with console and optional file rotation.
    """
    logger = logging.getLogger(name)
    logger.handlers = []  # Clear existing handlers
    
    # Console Handler
    console_handler = logging.StreamHandler()
    
    # File Handler (with rotation)
    file_handler = None
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5
        )

    # Formatters
    if json_format:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if file_handler:
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.setLevel(level)
    logger.propagate = False
    
    return logger

# Optimized imports

# Simulation summary hook
