import logging
from pathlib import Path

from rich.console import Console
from rich.table import Table

from comeit import (
    Body,
    Footer,
    Header,
    Rule,
    RuleConfig,
    RuleCreator,
    RuleLoader,
    RuleManager,
    configure_logger,
)
from comeit.parse_args import parse_args

logger = logging.getLogger("comeit")

CONVENTIONAL_TYPES = set(["feat", "fix"])
DEFAULT_TYPES = set(["build", "chore", "ci", "docs", "perf", "refactor", "revert", "style", "test"])
MAX_HEADER_LENGTH = 52  # Make this a config later
MAX_BODY_LENGTH = 70  # Make this a config later
MAX_FOOTER_LENGTH = 52  # Make this a config later


def init_rules(
    types: set[str], commit_msg: tuple[str, str, str], user_rules_yml: Path = None
) -> dict[str, Rule]:
    # Init check classes
    header = Header(types=types, max_length=MAX_HEADER_LENGTH, commit_msg=commit_msg[0])  # FINISH
    body = Body()
    footer = Footer()

    # Load rules from yaml config
    rule_loader = RuleLoader(user_rules_yml=user_rules_yml)
    loaded_rules: list[RuleConfig] = rule_loader.load_rules()

    # Create rule objects
    rule_creator = RuleCreator(rule_configs=loaded_rules, header=header, body=body, footer=footer)
    rules: dict[str, Rule] = rule_creator.create_rules()

    return rules


def create_commit_types(extra_types: list[str] = None, custom_types: list[str] = None) -> set[str]:
    """Create commit types from default types and/or custom types or extra types.

    Args:
    ----
        extra_types (list[str]): Adds extra types to the default types.
        custom_types (list[str], optional): Create your own types. This will disgard the
            default types, however it keeps "feat" and "fix" as they are required.
            Specifying this overrides the `extra_types` if it was given. Defaults to
            None.

    """
    types = CONVENTIONAL_TYPES

    if extra_types and not custom_types:
        types |= set(extra_types) | DEFAULT_TYPES
    elif custom_types:
        types |= set(custom_types)
    else:
        types |= DEFAULT_TYPES

    logger.debug("Allowed commit types: %s", "|".join(types))
    return types


# Make a commit parser file
def commit_parser():
    """Parse out header, body and footer."""


def main():
    args = parse_args()
    configure_logger(log_level=args.log_level)

    logger.info("Creating allowed commit types...")
    allowed_commit_types = create_commit_types()

    logger.info("Preparing commit message...")
    commit_msg = ("feat: this is a feature", "", "")

    logger.info("Initializing rules...")
    rules = init_rules(
        types=allowed_commit_types, commit_msg=commit_msg, user_rules_yml=args.config_file
    )

    logger.info("Listing rules...")
    for rule_id, rule in rules.items():
        logger.debug("%s", rule)

    logger.info("Applying rules to commit %s", commit_msg)
    rule_manager = RuleManager(rules)

    # Rule ID and successful/unsuccessful run returned
    results = rule_manager.apply_rules()

    # Display results
    console = Console()
    table = Table(title="Rules Summary")
    table.add_column("Rule", justify="left")
    table.add_column("Pass", justify="center")
    # table.add_column("Severity", justify="center")
    table.add_column("Description", justify="left")
    for rule_id, result in results.items():
        rule = rules[rule_id]

        if result.is_success():
            status = "✅"
        elif result.is_failed():
            status = "❌"
        elif result.is_ignored():
            status = "👻"
        else:
            raise ValueError(f"Unknown {result=}")

        # Warnings are always pass
        if rule.severity.is_warning():
            status = "🚧"

        rule_name = (
            f"{rule.component.value.title()} {rule.check.__name__.replace('_', ' ').title()}"
        )
        table.add_row(f"{rule_id} - {rule_name}", status, rule.description)

        if result.is_failed() and rule.severity.is_error():
            table.add_row(
                f"[bold red]{' ' * 7}Error[/bold red]", "", f"[bold red]  {rule.message}[/bold red]"
            )
        elif result.is_failed() and rule.severity.is_warning():
            table.add_row(
                f"[bold yellow]{' ' * 7}Warning[/bold yellow]",
                "",
                f"[bold yellow]  {rule.message}[/bold yellow]",
            )

    console.print(table)


if __name__ == "__main__":
    main()
