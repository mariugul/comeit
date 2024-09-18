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
    def __init__(self, user_rules_yml: Path | None = None) -> None:
        self._DEFAULT_RULES_YML = Path("default_rules.yml")
        self._user_rules_yml = user_rules_yml

    def load_rules(self) -> list[RuleConfig]:
        try:
            with importlib.resources.open_text("comeit", self._DEFAULT_RULES_YML) as f:
                rules_data = yaml.safe_load(f)
                logger.debug(f"{rules_data=}")

            if self._user_rules_yml:
                with self._user_rules_yml.open() as f:
                    user_rules_data: dict[str] = yaml.safe_load(f)
                    logger.debug(f"{user_rules_data}")

                for rule in rules_data:
                    rule_id = rule["id"]
                    if rule_id in user_rules_data:
                        rule["severity"] = user_rules_data[rule_id]

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
