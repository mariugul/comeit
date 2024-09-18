import importlib.resources
import logging
from dataclasses import dataclass
from pathlib import Path

import yaml

from .rule import Component, Severity

logger = logging.getLogger(__name__)


@dataclass
class RuleConfig:
    id: str
    description: str
    check: str
    component: Component
    severity: Severity
    dependencies: list[str] | None

    def __post_init__(self):
        # Convert the string to the corresponding Severity enum
        try:
            self.severity = Severity(self.severity)
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Severity field in rules.yml has invalid value. {e}. "
                "Choose from {Severity.get_members()}"
            )

        try:
            self.component = Component(self.component)
        except (KeyError, ValueError) as e:
            raise ValueError(
                f"Component field in rules.yml has invalid value. {e}. "
                "Choose from {Component.get_members()}"
            )


class RuleLoader:
    def __init__(self, rules_yml: Path = Path("default_rules.yml")) -> None:
        self._rules_yml = rules_yml

    def load_rules(self) -> list[RuleConfig]:
        try:
            with importlib.resources.open_text("comeit", self._rules_yml) as f:
                rules_data = yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(e)
            raise
        except yaml.YAMLError as e:
            logger.error(e)
            raise
        except OSError as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.error(e)
            raise

        config = [RuleConfig(**d) for d in rules_data]
        return config
