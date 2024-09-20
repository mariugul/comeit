import logging
from enum import IntEnum


class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def is_debug(self):
        return self == LogLevel.DEBUG

    def is_info(self):
        return self == LogLevel.INFO

    def is_warning(self):
        return self == LogLevel.WARNING

    def is_error(self):
        return self == LogLevel.ERROR

    def is_critical(self):
        return self == LogLevel.CRITICAL

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(level_str):
        try:
            return LogLevel[level_str.upper()]
        except KeyError:
            raise ValueError(f"Invalid log level: {level_str}")


def configure_logger(log_level: LogLevel):
    logging.basicConfig(level=log_level)
