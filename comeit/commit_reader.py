import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class CommitMessage:
    """Represents a commit message with its associated SHA.

    Attributes:
        sha (str): The SHA identifier of the commit.
        message (str): The commit message associated with the SHA.
    """

    sha: str
    message: str

    def __str__(self):
        """Returns a clear string representation of the CommitMessage."""
        return (
            f"{'-' * 52}\n"
            f"Commit SHA: {self.sha}\n"
            f"{'-' * 52}\n"
            f"{self.message}\n"
            f"{'-' * 52}\n"
        )


def run_git_command(
    git_args: list[str], repo_path: Path | None = None
) -> subprocess.CompletedProcess:
    """Run a git command in a specified repository path.

    Args:
        git_args (list[str]): A list of git arguments to run.
        repo_path (Path | None): The path to the Git repository. If None, the command
            is executed in the current directory.

    Returns:
        subprocess.CompletedProcess: The result of the `subprocess.run` call.

    Raises:
        subprocess.CalledProcessError: If the git command fails.
    """
    cmd = ["git"]
    if repo_path:
        cmd.extend(["-C", str(repo_path)])

    cmd.extend(git_args)
    logger.debug(f"Running git command: `{' '.join(cmd)}`")

    try:
        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e.stderr}")
        raise


def get_default_branch(repo_path: Path | None = None) -> str | None:
    """Retrieve the default branch name of a Git repository.

    This method tries to find origin/HEAD. This might not work unless the upstream is tracked.
    Most often it works, however a fallback option if this method doesn't find the default branch
    can be read from a config file or resolve to `main` or `master`.

    Args:
        repo_path (Path | None): The path to the Git repository. If None, the command
            is executed in the current directory.

    Returns:
        str | None: The default branch name, or None if it could not be determined.
    """
    try:
        result = run_git_command(["rev-parse", "--abbrev-ref", "origin/HEAD"], repo_path)
        return result.stdout.strip().replace("origin/", "")
    except subprocess.CalledProcessError:
        logger.error("Git failed to find the default branch from origin/HEAD.")
        return None


def get_git_log(from_ref: str = None, to_ref: str = None, repo_path: Path | None = None) -> str:
    """Retrieve the git log between two references.

    Args:
        from_ref (str | None): The starting reference (commit SHA, tag, or branch).
        to_ref (str | None): The ending reference (commit SHA, tag, or branch).
        repo_path (Path | None): The path to the Git repository. If None, the command
            is executed in the current directory.

    Returns:
        str: The git log output as a string.
    """
    log_format = "--format=%B%"

    git_args = ["log", log_format]

    if from_ref and to_ref:
        git_args.append(f"{from_ref}..{to_ref}")
    elif from_ref:
        git_args.append(f"{from_ref}..HEAD")

    result = run_git_command(git_args, repo_path)
    return result.stdout


def get_commit_message(sha: str, repo_path: Path | None = None) -> CommitMessage:
    """Retrieve the commit message for a given commit SHA.

    Args:
        sha (str): The commit SHA for which to retrieve the message.
        repo_path (Path | None): The path to the Git repository. If None, the command
            is executed in the current directory.

    Raises:
        ValueError: If the provided SHA is invalid.
        RuntimeError: If the command to retrieve the commit message fails.

    Returns:
        CommitMessage: An instance of CommitMessage containing the SHA and message.
    """
    cmd = ["show", "-s", "--format=%B", sha]

    try:
        result = run_git_command(cmd, repo_path)
        return CommitMessage(sha=sha, message=result.stdout.rstrip())
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to retrieve commit message for SHA {sha}: {e.stderr}")
        raise RuntimeError(f"Error retrieving commit message for SHA '{sha}'") from e
    except ValueError as e:
        logger.error(f"Failed to create {CommitMessage.__name__} object: {e}")
        raise ValueError(f"Invalid commit SHA: {sha}") from e


def get_commit_hashes(
    from_ref: str | None = None, to_ref: str | None = None, repo_path: Path | None = None
) -> list[str]:
    """Retrieve a list of commit SHAs from `from_ref` to `to_ref` using git rev-list.

    The commit on `from_ref` will not be included. To include it add `^` at the end: `from_ref^`.

    The method determines the range of commits based on the provided references:
    - If `from_ref` and `to_ref` are provided, it retrieves commits in the range `from_ref..to_ref`.
    - If only `from_ref` is provided, it retrieves commits from `from_ref..HEAD`.
    - If neither reference is provided, it retrieves `HEAD` - all commits in the repository.

    Args:
        from_ref (str | None): The starting commit SHA, tag, or branch (e.g., `7db61cb^`).
        to_ref (str | None): The ending commit SHA, tag, or branch (e.g., `HEAD`).
        repo_path (Path | None): The path to the Git repository. If None, the command
            is executed in the current directory.

    Returns:
        list[str]: A list of commit SHAs from `from_ref` to `to_ref`.
    """
    git_args = ["rev-list"]

    if from_ref and to_ref:
        git_args.append(f"{from_ref}..{to_ref}")
    elif from_ref:
        git_args.append(f"{from_ref}..HEAD")
    else:
        git_args.append("HEAD")

    try:
        result: str = run_git_command(git_args, repo_path)
        # Split the output into a list of commit hashes
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError:
        return []
