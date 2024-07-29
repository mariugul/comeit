from enum import Enum
from typing import Callable

class Severity(Enum):
    """Different levels of severity for rules

    Attributes:
        ERROR (str): Indicates a critical issue that must be fixed.
        WARNING (str): Indicates a potential issue that should be reviewed.
        INFO (str): Provides informational messages or suggestions.
        IGNORE (str): Indicates issues that should be ignored or not reported.
    """
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    IGNORE = "ignore"

class Rule:
    def __init__(self, id: str, description: str, check: Callable, severity: Severity = Severity.WARNING, dependencies: list[str] | None = None):
        self.id = id
        self.description = description
        self.check = check
        self.severity = severity
        self.dependencies = dependencies if dependencies else []

    def apply(self, *args, **kwargs):
        return self.check(*args, **kwargs)
