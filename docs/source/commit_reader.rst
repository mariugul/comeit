.. _git_utilities:

Commit Message Reader
===========================

This document provides an overview of the Git utilities implemented in the codebase. These utilities
facilitate interactions with Git repositories, including retrieving commit messages, logs, and
hashes.

Overview
--------
The utilities are designed to streamline the process of working with Git repositories, allowing
users to efficiently retrieve information about commits and branches.

Use Cases
---------
Here are some examples of how to use these utilities in practice.

1. **Get the Default Branch:**

   You can retrieve the default branch of a Git repository with:

   .. code-block:: python

      default_branch = get_default_branch()
      print(f"The default branch is: {default_branch}")

   .. note:: This function only works if the ``origin/HEAD`` upstream is tracked. It often works,
      but not always. If it fails to determine the default branch, it will return None. In such
      cases, you may need to determine the default branch through alternative methods, such as
      checking a configuration file, accepting an input from the command line, or falling back to a
      default branch name like ``main`` or ``master``.


2. **Retrieve Commit Messages between SHA's:**

   To get the commit messages between two SHAs:

   .. code-block:: python

      commit_hashes = get_commit_hashes(from_ref="438dd4a", to_ref="3516923")
      for hash in commit_hashes:
          print(get_commit_message(sha=hash))
   
   .. note:: This will not include the commit ``438dd4a``. To include it add a caret ``438dd4a^``.

3. **Retrieve Commit Messages from TAG:**

   To get the commit messages between from TAG to SHA:

   .. code-block:: python

      commit_hashes = get_commit_hashes(from_ref="0.5.0", to_ref="HEAD")
      for hash in commit_hashes:
          print(get_commit_message(sha=hash))

   .. note:: Leaving out ``to_ref`` produces the same result as ``to_ref="HEAD"``.
   
4. **Retrieve Commit Messages on Default Branch:**

   To get the commit messages on main the from-sha to-sha method works also. To get the full main
   commit history, leave out all sha references, this uses just ``HEAD``:

   .. code-block:: python

      commit_hashes = get_commit_hashes()
      for hash in commit_hashes:
          print(get_commit_message(sha=hash))


5. **Handle Errors Gracefully:**

   If an invalid SHA is provided, an error will be raised:

   .. code-block:: python

      try:
          message = get_commit_message(sha="invalid_sha")
      except RuntimeError as e:
          print(f"Error: {e}")

Conclusion
----------
These utilities provide essential functionalities for working with Git repositories
programmatically. By encapsulating common Git commands, they simplify the process of retrieving and
managing commit information.

