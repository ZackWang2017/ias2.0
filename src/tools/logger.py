import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """
    A utility class for handling logging in the IAS 2.0 application.
    Supports both file and console logging with different log levels.
    """
    
    _instance = None
    
    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not hasattr(self, 'logger'):
            self.logger = logging.getLogger('IAS2.0')
            self.logger.setLevel(logging.DEBUG)
            
            # Create logs directory if it doesn't exist
            self.log_dir = os.path.join(os.path.dirname(
                os.path.dirname(__file__)), 'logs')
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Set up file handler
            log_file = os.path.join(
                self.log_dir, 
                f'ias_{datetime.now().strftime("%Y%m%d")}.log'
            )
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Set up console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Create formatters and add them to the handlers
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_formatter = logging.Formatter(
                '%(levelname)s: %(message)s'
            )
            
            file_handler.setFormatter(file_formatter)
            console_handler.setFormatter(console_formatter)
            
            # Add handlers to the logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Log debug level message."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Log info level message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning level message."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Log error level message."""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Log critical level message."""
        self.logger.critical(message, *args, **kwargs)
    
    def set_level(self, level: str) -> None:
        """Set the logging level."""
        self.logger.setLevel(getattr(logging, level.upper()))
    
    def get_log_file_path(self) -> str:
        """Get the current log file path."""
        return os.path.join(
            self.log_dir,
            f'ias_{datetime.now().strftime("%Y%m%d")}.log'
        )