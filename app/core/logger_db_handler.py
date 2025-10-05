import logging
from app.database.sync.session import get_db
from app.models.logs import Log
import json

class DBHandler(logging.Handler):
    """
    Custom logging handler to write logs into the database
    """
    def emit(self, record: logging.LogRecord):
        try:
            session = get_db()
            log_entry = Log(
                level=record.levelname,
                message=record.getMessage(),
                module=record.module,
                func_name=record.funcName,
                line_no=record.lineno,
                extra=getattr(record, "extra", None)
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            print(f"Failed to log to DB: {e}")
        finally:
            session.close()
