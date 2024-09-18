import logging
from collections import deque
from enum import Enum, auto

from .rule import Rule, Severity

logger = logging.getLogger(__name__)


class RuleResult(Enum):
    """Enumeration for the result of applying a rule.

    Attributes:
        IGNORED: The rule was ignored.
        SUCCESS: The rule was applied successfully.
        FAILED: The rule application failed.
    """

    IGNORED = auto()
    SUCCESS = auto()
    FAILED = auto()

    def is_ignored(self) -> bool:
        return self == RuleResult.IGNORED

    def is_success(self) -> bool:
        return self == RuleResult.SUCCESS

    def is_failed(self) -> bool:
        return self == RuleResult.FAILED


class RuleManager:
    """Manages and applies a set of rules."""

    def __init__(self, rules: dict[str, Rule]):
        """Initialize the RuleManager with a dictionary of rules.

        Args:
            rules (dict[str, Rule]): A dictionary mapping rule IDs to Rule objects.
        """
        self._rules = rules

    def apply_rules(self) -> dict[str, RuleResult]:
        """Applies all the rules in dependency order.

        Returns:
            dict[str, RuleResult]: A dictionary mapping rule IDs to their corresponding RuleResult.
        """
        # Validate dependencies and build graph
        graph, in_degree = self._validate_and_build_graph()

        # Perform topological sort
        sorted_rules = self._topological_sort(graph, in_degree)
        logger.debug(f"{sorted_rules=}")

        # Apply rules in sorted order
        results: dict[str, bool | None] = {}
        for rule_id in sorted_rules:
            rule = self._rules[rule_id]

            if rule.severity == Severity.IGNORE:
                results[rule_id] = RuleResult.IGNORED
                continue

            result, rule.message = rule.apply()
            results[rule_id] = RuleResult.SUCCESS if result else RuleResult.FAILED

        return results

    def _validate_and_build_graph(self) -> tuple[dict[str, list[str]], dict[str, int]]:
        """Builds the dependency graph and validates the rules.

        Returns:
            tuple[dict[str, list[str]], dict[str, int]]: A graph and in-degree dictionary.
        """
        graph = {rule_id: [] for rule_id in self._rules}
        in_degree = {rule_id: 0 for rule_id in self._rules}

        for rule_id, rule in self._rules.items():
            if rule.dependencies:
                if len(rule.dependencies) > 1:
                    raise ValueError(f"Rule {rule_id} has more than one dependency.")
                dependency = rule.dependencies[0]

                if dependency not in self._rules:
                    raise ValueError(f"Rule {rule_id} depends on a non-existent rule {dependency}.")

                graph[dependency].append(rule_id)
                in_degree[rule_id] += 1

        return graph, in_degree

    def _topological_sort(
        self, graph: dict[str, list[str]], in_degree: dict[str, int]
    ) -> list[str]:
        """Performs a topological sort on the rule graph.

        Args:
            graph (dict[str, list[str]]): The dependency graph.
            in_degree (dict[str, int]): The in-degree (number of dependencies) of each rule.

        Returns:
            list[str]: The sorted order of rule IDs.
        """
        queue = deque([rule_id for rule_id in self._rules if in_degree[rule_id] == 0])
        sorted_rules = []

        while queue:
            rule_id = queue.popleft()
            sorted_rules.append(rule_id)

            for dependent in graph[rule_id]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_rules) != len(self._rules):
            raise ValueError("Circular dependency detected among rules.")

        return sorted_rules
