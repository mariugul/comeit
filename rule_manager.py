class RuleManager:
    def __init__(self):
        self.rules = []

    def register_rule(self, rule: Rule):
        self.rules.append(rule)

    def apply_rules(self, header: Header, body: Body, footer: Footer):
        context = {
            "header": header,
            "body": body,
            "footer": footer
        }
        for rule in self.rules:
            if rule.severity != Severity.IGNORE:
                if self.check_dependencies(rule, context):
                    result = rule.apply(header, body, footer)
                    if result is not True:  # Only print if there is an issue
                        print(f"{rule.severity.value.upper()}: {rule.description} - {result}")

    def check_dependencies(self, rule: Rule, context: dict):
        for dep_id in rule.dependencies:
            dep_rule = next((r for r in self.rules if r.id == dep_id), None)
            if dep_rule and dep_rule.apply(**context) is not True:
                return False
        return True
