import pytest
from comeit import parse_commit_message


def test_only_summary_line():
    """Test parsing a commit message that contains only a summary line.

    This test verifies that when a commit message consists of a single line,
    it is correctly identified as the summary, with no body or footer.
    """
    commit_msg = "feat(core): add new feature"
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg
    assert body is None
    assert footer is None


def test_empty_commit_message():
    """Test parsing an empty commit message.

    This test ensures that a ValueError is raised when an empty string is
    provided as the commit message, indicating that the message cannot be parsed.
    """
    with pytest.raises(
        ValueError, match="Failed to parse commit message. Commit message is empty."
    ):
        parse_commit_message("")


def test_summary_and_newline_only():
    """Test parsing a commit message with a summary line followed by a newline.

    This test checks that a commit message containing a summary followed
    by a single newline is correctly parsed, resulting in an empty body
    and no footer.
    """

    commit_msg = "feat(core): add new feature\n"
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == ""
    assert footer is None


def test_summary_and_body_without_footer():
    """Test parsing a commit message with a summary and body without a footer.

    This test ensures that when a commit message contains a summary and
    a body but no footer, both the summary and body are correctly extracted.
    """
    commit_msg = """feat(core): add new feature
This feature allows users to do amazing things."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == commit_msg.partition("\n")[2]
    assert footer is None


def test_summary_with_newline_and_body_without_footer():
    """Test parsing a commit message with a summary line and a body with newlines.

    This test checks that a commit message containing a summary,
    followed by newlines and then a body, is parsed correctly, with
    the body including preserved newlines.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.
It supports multiple languages."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == commit_msg.partition("\n")[2]
    assert footer is None


def test_summary_body_and_footer():
    """Test parsing a commit message with a summary, body, and footer.

    This test verifies that a commit message containing a summary,
    body, and footer is correctly parsed, with each component
    accurately identified.
    """

    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.

BREAKING CHANGE: This will change the API."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\nThis feature allows users to do amazing things.\n"
    assert footer == "BREAKING CHANGE: This will change the API."


def test_multiple_footers():
    """Test parsing a commit message with multiple footers.

    This test ensures that when a commit message contains multiple footer lines,
    they are all correctly recognized and separated from the body and summary.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.

BREAKING CHANGE: This will change the API.
Signed-off-by: John Doe
Reviewed-by: Jane Doe"""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\nThis feature allows users to do amazing things.\n"
    assert (
        footer
        == """BREAKING CHANGE: This will change the API.
Signed-off-by: John Doe
Reviewed-by: Jane Doe"""
    )


def test_commit_with_multiple_newlines_at_end():
    """Test parsing a commit message with multiple newlines at the end.

    This test checks that a commit message containing newlines at the end
    is parsed correctly, with the body and footer preserving their
    respective newlines.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.

BREAKING CHANGE: This will change the API.



"""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\nThis feature allows users to do amazing things.\n"
    assert footer == "BREAKING CHANGE: This will change the API.\n\n\n\n"


def test_body_with_no_footers():
    """Test parsing a commit message with a summary and body without footers.

    This test verifies that a commit message with a summary and body,
    but no footers, is parsed correctly with both components recognized.
    """
    commit_msg = """fix(bug): fix issue with feature

Corrected the error with the feature causing failures."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == commit_msg.partition("\n")[2]
    assert footer is None


def test_footer_without_body():
    """Test parsing a commit message with a summary and an empty body."""
    commit_msg = """feat(core): add new feature




BREAKING CHANGE: Changes the API."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\n\n\n"
    assert footer == "BREAKING CHANGE: Changes the API."


def test_footer_inside_body():
    """Test parsing a commit message with a footer line inside the body.

    This test checks that a footer line within the body of a commit message
    is correctly included in the body instead of being recognized as a footer.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.
BREAKING CHANGE: This looks like a footer but should be part of the body.

This is a continuation of the body.
Signed-off-by: John Doe"""

    summary, body, footer = parse_commit_message(commit_msg)

    assert summary == commit_msg.partition("\n")[0]
    assert body == "\nThis feature allows users to do amazing things."
    assert (
        footer
        == """BREAKING CHANGE: This looks like a footer but should be part of the body.

This is a continuation of the body.
Signed-off-by: John Doe"""
    )


def test_footer_with_leading_blank_lines():
    """Test parsing a commit message with leading blank lines before a footer.

    This test verifies that a commit message with leading blank lines before
    a footer is parsed correctly, preserving all blank lines in the body
    while recognizing the footer.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.


BREAKING CHANGE: This will change the API."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == "feat(core): add new feature"
    assert body == "\nThis feature allows users to do amazing things.\n\n"
    assert footer == "BREAKING CHANGE: This will change the API."


def test_empty_footer():
    """Test parsing a commit message with an empty footer line.

    This test ensures that when a footer tag such as 'BREAKING CHANGE:' is present
    but does not contain any content after the colon, it is treated as part of the
    body instead of being recognized as a footer. The commit message contains a
    summary, body, and an empty 'BREAKING CHANGE:' line, which should result in no
    footer being identified.
    TODO: Look into whether this should change to recognized as footer
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do amazing things.

BREAKING CHANGE:"""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == commit_msg.partition("\n")[2]
    assert footer is None


def test_commit_with_random_whitespace():
    """Test parsing a commit message with random whitespace.

    This test verifies that a commit message containing multiple blank lines
    and random whitespace is correctly parsed, with the body preserving all 
    whitespace and newlines, while the footer is accurately extracted.
    """
    commit_msg = """feat(core): add new feature





This is the body.
    


 
Signed-off-by: John Doe"""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\n\n\n\n\nThis is the body.\n    \n\n\n "
    assert footer == "Signed-off-by: John Doe"


def test_commit_without_summary():
    """Test parsing a commit message that lacks a summary.

    This test checks that when a commit message does not include a summary 
    line, the first line is treated as part of the body, and the footer, if 
    present, is correctly identified.
    """
    commit_msg = """
This feature allows users to do amazing things.

BREAKING CHANGE: This will change the API."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "This feature allows users to do amazing things.\n"
    assert footer == "BREAKING CHANGE: This will change the API."


def test_footer_and_body_same_line():
    """Test parsing a commit message with a footer line on the same line as the body.

    This test ensures that when a commit message contains a footer immediately 
    following the body on the same line, the footer is not misidentified and 
    the entire line is treated as part of the body.
    """
    commit_msg = """feat(core): add new feature

This feature allows users to do things.BREAKING CHANGE: Changes the API."""
    summary, body, footer = parse_commit_message(commit_msg)
    assert summary == commit_msg.partition("\n")[0]
    assert body == "\nThis feature allows users to do things.BREAKING CHANGE: Changes the API."
    assert footer is None
