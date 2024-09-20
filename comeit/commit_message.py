import logging
import re

logger = logging.getLogger(__name__)


def parse_commit_message(commit_message: str):
    """Parse a commit message into its components: summary, body, and footer.

    Args:
        commit_message (str): The commit message to parse.

    Returns:
        tuple: A tuple containing:
            - summary (str): The summary line of the commit message.
            - body (str or None): The body of the commit message, or None if not present.
            - footer (str or None): The footer of the commit message, or None if not present.

    Raises:
        ValueError: If the commit message is empty or cannot be parsed.
    """
    lines = commit_message.split("\n")  # Do not strip here to preserve all newlines

    if not lines or lines == [""]:
        raise ValueError("Failed to parse commit message. Commit message is empty.")

    summary = lines[0]

    if _is_summary_only(lines):
        return summary, None, None

    # We check for footers first and assume anything before the footer is the body
    body, footer = _extract_body_and_footer(lines[1:])  # Pass all lines after the summary

    return summary, body, footer


def _is_summary_only(lines: list[str]):
    """Check if the commit message consists of only the summary line."""
    return len(lines) == 1


def _is_footer_line(line: str):
    """Check if the given line is a footer line based on the rules."""
    footer_pattern = re.compile(r"^(BREAKING CHANGE|[A-Za-z-]+)(: | #)")
    return bool(footer_pattern.match(line.strip()))


def _extract_body_and_footer(lines: list[str]):
    """Extract body and footer by treating lines as body until a footer is found.

    After the first footer, all lines are treated as footer.
    """
    footers = []
    body_lines = []
    found_footer = False  # Track whether a footer has been found

    for line in lines:
        if found_footer:
            footers.append(line)  # Once a footer is found, everything else is part of the footer
        elif _is_footer_line(line):
            found_footer = True
            footers.append(line)  # Start collecting footer lines
        else:
            body_lines.append(line)  # Collect body lines until a footer is encountered

    # Join lines without stripping to preserve all newlines
    body = "\n".join(body_lines) if body_lines else None
    footer = "\n".join(footers) if footers else None

    return body, footer


if __name__ == "__main__":
    # Example usage
    commit_msg = """feat(core): add new feature

BREAKING CHANGE: Changes the API."""

    summary, body, footer = parse_commit_message(commit_msg)

    def print_message(header: str, msg: str):
        print(f"{header}")
        print("‾" * 50)
        print("" if msg is None else msg)
        print("‾" * 50)
        print()

    print_message("Summary", summary)
    print_message("Body", body)
    print_message("Footer", footer)
