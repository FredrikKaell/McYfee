"""
#Module for application-wide logging.
"""

import logging
from pathlib import Path
from datetime import datetime

from webtracker.config import PROJECT_ROOT

class AppLogger:
    def __init__(self, name: str = "mcyfee", log_level: int = logging.INFO):
        self.name = name
        self.log_level = log_level

        self.log_dir = PROJECT_ROOT / 'logs'
        self.log_file = self.log_dir / f"log_{datetime.now().strftime('%Y%m%d')}.log"

        self._ensure_log_directory()

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.log_level)

        if not self.logger.handlers:
            self._setup_handlers()

    def _ensure_log_directory(self):

        #Create log directory if it does not exist
        self.log_dir.mkdir(exist_ok=True)

    def _setup_handlers(self):
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


# TEST
#if __name__ == "__main__":
    #logger = AppLogger().get_logger()
    #logger.info("Logger is working")
    #logger.warning("This is a warning...")
    #logger.error("This is an error")
