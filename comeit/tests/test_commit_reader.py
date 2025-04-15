import pytest
import subprocess
from pathlib import Path
from comeit import get_commit_hashes, get_commit_message, get_default_branch

DEFAULT_BRANCH = "main"


@pytest.fixture
def init_git_repo(tmp_path: Path):
    """Fixture to initialize a temporary Git repository."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()

    # Set user config
    subprocess.run(["git", "-C", str(repo_path), "config", "user.name", "Test User"], check=True)
    subprocess.run(
        ["git", "-C", str(repo_path), "config", "user.email", "test@example.com"], check=True
    )

    # Initialize a new git repository
    subprocess.run(
        ["git", "-C", str(repo_path), "init", f"--initial-branch={DEFAULT_BRANCH}"], check=True
    )
    subprocess.run(["git", "-C", str(repo_path), "branch", "-M", "main"], check=True)
    subprocess.run(
        ["git", "-C", str(repo_path), "commit", "--allow-empty", "-m", "chore: initial commit"],
        check=True,
    )

    yield repo_path


def run_git(repo_path: Path, *args):
    """Helper to run git commands in the repo."""
    subprocess.run(["git", "-C", str(repo_path), *args], check=True)


def git_commit(repo_path: Path, message: str):
    run_git(repo_path, "commit", "--allow-empty", "-m", message)


def git_create_branch(repo_path: Path, branch: str):
    run_git(repo_path, "branch", branch)


def git_switch_branch(repo_path: Path, branch: str):
    run_git(repo_path, "checkout", branch)


def git_log(repo_path: Path):
    run_git(repo_path, "log")


@pytest.mark.parametrize("from_ref, to_ref", [(DEFAULT_BRANCH, "HEAD"), (DEFAULT_BRANCH, None)])
def test_commits_on_current_branch(init_git_repo: Path, from_ref: str, to_ref: str | None):
    """Test that commit ranges between SHAs are properly retrieved.
    
    Verifies from default branch `main..HEAD` which means the current checked out branch.
    """
    repo_path = init_git_repo

    test_branch = "test-branch"
    git_create_branch(repo_path, test_branch)
    git_switch_branch(repo_path, test_branch)

    first_commit = "feat: first commit"
    second_commit = "feat: second commit\n\nThis is a crazy body that is a bit long"
    git_commit(repo_path, first_commit)
    git_commit(repo_path, second_commit)

    # Get the commit hashes in the range
    commit_hashes = get_commit_hashes(from_ref=from_ref, to_ref=to_ref, repo_path=repo_path)

    assert len(commit_hashes) == 2, f"Expected 2 commits, but got {len(commit_hashes)}"

    # Retrieve and assert the commit messages
    expected_messages = [second_commit, first_commit]
    commit_messages = [get_commit_message(sha=sha, repo_path=repo_path) for sha in commit_hashes]

    for commit, expected_message in zip(commit_messages, expected_messages):
        assert (
            commit.message == expected_message
        ), f"{expected_message=}, but got '{commit.message=}'"

@pytest.mark.parametrize("sha_start, sha_end, expected_count", [
    ("HEAD~3", "HEAD", 3),
    ("HEAD~1", "HEAD", 1),
    ("HEAD^", "HEAD", 1),
    (DEFAULT_BRANCH, "test-branch", 3),
    (DEFAULT_BRANCH, None, 3),
    ("1.0.0", "HEAD", 3),
    ],
    ids=[
        "HEAD~3..HEAD",
        "HEAD~1..HEAD",
        "HEAD^..HEAD",
        "main..test-branch",
        "main..HEAD",
        "1.0.0..HEAD"
    ]
)
def test_commit_ranges_with_sha(init_git_repo: Path, sha_start: str, sha_end: str, expected_count: int):
    """Test that commit ranges using SHAs are properly retrieved."""
    repo_path = init_git_repo

    # Create a tag for the first commit
    run_git(repo_path, "tag", "1.0.0", "HEAD")  # Tag the second commit

    test_branch = "test-branch"
    git_create_branch(repo_path, test_branch)
    git_switch_branch(repo_path, test_branch)

    # Create multiple commits
    git_commit(repo_path, "feat: first commit")
    git_commit(repo_path, "feat: second commit")
    git_commit(repo_path, "feat: third commit")


    # Get the commit hashes in the range
    commit_hashes = get_commit_hashes(from_ref=sha_start, to_ref=sha_end, repo_path=repo_path)

    assert len(commit_hashes) == expected_count, (
        f"Expected {expected_count} commits from {sha_start} to {sha_end}, but got {len(commit_hashes)}"
    )

    # Retrieve and assert the commit messages if there are expected commits
    if expected_count > 0:
        commit_messages = [get_commit_message(sha=sha, repo_path=repo_path) for sha in commit_hashes]
        for commit in commit_messages:
            assert commit.message.startswith("feat:"), "Commit message should start with 'feat:'"

@pytest.mark.parametrize("sha_start, sha_end, expected_count", [
    ("HEAD~3", "HEAD", 3),
    ("HEAD~1", "HEAD", 1),
    ("HEAD^", "HEAD", 1),
    (DEFAULT_BRANCH, "test-branch", 0),
    ("1.0.0", "HEAD", 3),
    (None, None, 4) # Don't pass in any sha's
],
    ids=[
        "HEAD~3..HEAD",
        "HEAD~1..HEAD",
        "HEAD^..HEAD",
        "main..test-branch",
        "1.0.0..HEAD",
        "HEAD"
    ]
)
def test_commit_ranges_on_main_branch(init_git_repo: Path, sha_start: str, sha_end: str, expected_count: int):
    """Test that commit ranges using SHAs and tags are properly retrieved from the main branch."""
    repo_path = init_git_repo

    # Create a tag for the initial commit
    run_git(repo_path, "tag", "1.0.0", "HEAD")  # Tag the initial commit

    git_commit(repo_path, "feat: first commit")
    git_commit(repo_path, "feat: second commit")
    git_commit(repo_path, "feat: third commit")

    # Get the commit hashes in the range
    if sha_start is None and sha_end is None:
        commit_hashes = get_commit_hashes(repo_path=repo_path)
    else:
        commit_hashes = get_commit_hashes(from_ref=sha_start, to_ref=sha_end, repo_path=repo_path)

    assert len(commit_hashes) == expected_count, (
        f"Expected {expected_count} commits from {sha_start} to {sha_end}, but got {len(commit_hashes)}"
    )
