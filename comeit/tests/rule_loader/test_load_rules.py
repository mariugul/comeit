from pathlib import Path

from comeit import RuleConfig, RuleLoader, Severity

def test_load_rules_from_yml_file():
    """Verifies that rules can be loaded from the rules yaml file."""
    rules_yml = Path(__file__).parent / "rules.yml"
    rule_loader = RuleLoader(user_rules_yml=rules_yml)
    rule_loader._DEFAULT_RULES_YML = rules_yml
    rules = rule_loader.load_rules()

    expected_list = [
        RuleConfig(
            id="01",
            description="Check header length",
            check="check_header",
            component="HEADER",
            severity=Severity.ERROR,
            dependencies=None,
        ),
        RuleConfig(
            id="02",
            description="Check header chars",
            check="scope_chars",
            component="HEADER",
            severity=Severity.WARNING,
            dependencies=["01"],
        ),
    ]

    assert rules == expected_list
