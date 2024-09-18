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
        self._OVERRIDE_RULES_YML = Path("comeit_config.yml")
        self._user_rules_yml = user_rules_yml

    def load_rules(self) -> list[RuleConfig]:
        try:
            with importlib.resources.open_text("comeit", self._DEFAULT_RULES_YML) as f:
                rules_data = yaml.safe_load(f)

            logger.debug(f"{rules_data=}")

            # Determine which file to use for overrides
            override_file = None
            if self._user_rules_yml is not None:  # If the user provides a file
                if self._user_rules_yml.exists():
                    override_file = self._user_rules_yml
                else:
                    logger.warning(
                        f"User-specified rules file '{self._user_rules_yml}' not found. Skipping."
                    )
            elif self._OVERRIDE_RULES_YML.exists():  # Fall back to system-wide override if provided
                override_file = self._OVERRIDE_RULES_YML
                logger.debug(f"Using system-wide override: {self._OVERRIDE_RULES_YML}")

            # If an override file exists, load it and apply the overrides
            if override_file:
                with override_file.open() as f:
                    user_rules_data: dict[str] = yaml.safe_load(f)
                logger.debug(f"User or system rules loaded: {user_rules_data}")

                # Apply user overrides to default rules
                for rule in rules_data:
                    rule_id = rule["id"]
                    if rule_id in user_rules_data:
                        rule["severity"] = user_rules_data[rule_id]
                        logger.debug(
                            f"Overriding severity for rule {rule_id} to {user_rules_data[rule_id]}"
                        )

        except Exception as e:
            logger.error(e)
            raise

        config = [RuleConfig(**d) for d in rules_data]
        return config
