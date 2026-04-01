"""
MEGA-STACK v2.5 Installation Wizard — Modüler Logger
/logs/install.log dosyasına ve konsola JSON formatında log yazar.
Format: {"timestamp", "level", "message", "step_id"}
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "install.log")


class JsonFormatter(logging.Formatter):
    """Her log kaydını JSON formatında serialize eder."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "step_id": getattr(record, "step_id", None),
        }
        return json.dumps(log_entry, ensure_ascii=False)


class WizardLogger:
    """
    Hem /logs/install.log dosyasına hem de konsola
    JSON formatında (timestamp, level, message, step_id) log yazar.
    """

    def __init__(self, name: str = "wizard"):
        os.makedirs(LOG_DIR, exist_ok=True)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False

        # Mevcut handler'ları kaldır (tekrar çağrılırsa duplikasyonu önler)
        if self._logger.handlers:
            self._logger.handlers.clear()

        formatter = JsonFormatter()

        # Dosya handler — install.log
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        # Konsol handler — stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def _log(self, level: int, message: str, step_id: str | None = None) -> None:
        self._logger.log(level, message, extra={"step_id": step_id})

    def debug(self, message: str, step_id: str | None = None) -> None:
        self._log(logging.DEBUG, message, step_id)

    def info(self, message: str, step_id: str | None = None) -> None:
        self._log(logging.INFO, message, step_id)

    def warning(self, message: str, step_id: str | None = None) -> None:
        self._log(logging.WARNING, message, step_id)

    def error(self, message: str, step_id: str | None = None) -> None:
        self._log(logging.ERROR, message, step_id)

    def critical(self, message: str, step_id: str | None = None) -> None:
        self._log(logging.CRITICAL, message, step_id)


# Singleton — tüm modüller aynı logger instance'ını kullanır
wizard_logger = WizardLogger()
