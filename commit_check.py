import logging

logger = logging.getLogger(__name__)

CONVENTIONAL_TYPES = set(["feat", "fix"])
DEFAULT_TYPES = set([
  'build',
  'chore',
  'ci',
  'docs',
  'perf',
  'refactor',
  'revert',
  'style',
  'test'
  ])


def check_commit(extra_types: list[str] = None, custom_types: list[str] = None):
    """Check a commit

    Args:
        extra_types (list[str]): Adds extra types to the default types.
        custom_types (list[str], optional): Create your own types. This will disgard the default
            types, however it keeps "feat" and "fix" as they are required. Specifying this overrides
            the `extra_types` if it was given. Defaults to None.
    """
    types = CONVENTIONAL_TYPES

    if extra_types and not custom_types:
        types |= set(extra_types) | DEFAULT_TYPES
    elif custom_types:
        types |= set(custom_types)
    else:
        types |= DEFAULT_TYPES
    
    print(types)


if __name__ == "__main__":
    check_commit()
