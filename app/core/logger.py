import logging
from logging.handlers import TimedRotatingFileHandler
from pythonjsonlogger import jsonlogger
from pathlib import Path
import sys
from datetime import datetime
from app.database.sync.session import get_db
from app.models.logs import Log
from app.core.logger_db_handler import DBHandler

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def get_log_file():
    """Return log file path based on current date."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"app_{date_str}.log"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Add module, function, and line number automatically."""
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = record.levelname
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        log_record["module"] = record.module
        log_record["funcName"] = record.funcName
        log_record["lineno"] = record.lineno
        # Include any extra dynamic fields
        if hasattr(record, "extra") and record.extra:
            log_record.update(record.extra)


def setup_logger(name: str = "app", level=logging.INFO, log_to_db: bool = False):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        log_file = get_log_file()

        # File handler with JSON
        file_handler = TimedRotatingFileHandler(log_file, when="midnight", backupCount=7, encoding="utf-8")
        file_formatter = CustomJsonFormatter("%(timestamp)s %(name)s %(level)s %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler with human-readable format
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            "%(levelname)s: %(asctime)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Optional DB handler
        if log_to_db:
            db_handler = DBHandler()
            db_handler.setFormatter(file_formatter)
            logger.addHandler(db_handler)

    return logger



# Custom log level for execution
EXECUTION = 25
logging.addLevelName(EXECUTION, "EXECUTION")

def log_execution(self, message, extra=None):
    if self.isEnabledFor(EXECUTION):
        self._log(EXECUTION, message, (), extra={"extra": extra})

logging.Logger.execution = log_execution

# Global logger instance
logger = setup_logger(log_to_db=True)
