"""
#Module for application-wide logging.
"""

import logging
from pathlib import Path
class AppLogger:
    def __init__(self, name: str = "mcyfee", log_level: int = logging.INFO):
        self.name = name
        self.log_level = log_level

        self.log_dir = Path("logs")
        self.log_file = self.log_dir / "app.log"

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
https://github.com/FredrikKaell/McYfee/pull/6/conflict?name=src%252Fwebtracker%252Flogger.py&ancestor_oid=e69de29bb2d1d6434b8b29ae775ad8c2e48c5391&base_oid=8fd752c8386487a4e2e1f641ae7c9d6b86e67e30&head_oid=f73cd4e8490ecbf12f9fe6cf922ffb09bca0750d
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
