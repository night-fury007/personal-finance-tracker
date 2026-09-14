import logging
import sys


class WealthEngineLogger:
    """Configures and provides a standardized logger for the Wealth Engine application."""

    def __init__(self, name: str = "wealth_engine", level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Prevent adding duplicate handlers if initialized multiple times
        if not self.logger.handlers:
            self._configure_handlers()

    def _configure_handlers(self):
        # Console handler for standard output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Standardized formatter with timestamps, module name, log level, and message
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    @property
    def get_logger(self) -> logging.Logger:
        return self.logger


# Global application logger instance
logger = WealthEngineLogger().get_logger
