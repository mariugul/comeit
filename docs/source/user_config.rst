===================================================
Using a Configuration File for Rule Overrides
===================================================

The `comeit` package allows users to customize the severity levels of specific commit rules by using
a configuration file. This file overrides the default rules provided by the package, enabling you to
enforce or relax certain rules according to your needs.

By default, the package defines a set of commit rules, each with a specific severity level (e.g., 
`ERROR`, `WARNING`, or `IGNORE`). The configuration file lets you change the severity level of these
rules, while all other aspects of the rule (such as the rule description and function) remain the same.

There are two ways to apply a custom configuration:

1. **Create a Configuration File with Any Name and Location**
   ---------------------------------------------------------
   You can create a configuration file with any name and place it anywhere in your project directory.
   To use this file, specify the path to it using the `--config-file` parameter when running the package.

   **How to Apply:**

   Specify the path to your configuration file using the `--config-file` parameter:

   .. code-block::

       comeit --config-file /path/to/your_config.yml

2. **Create `comeit_config.yml` in the Repository Root**
   ------------------------------------------------------
   Alternatively, place a file named `comeit_config.yml` in the root of your project directory. The package 
   will automatically detect this file and apply the overrides.

   **How to Apply:**

   The package will load the `comeit_config.yml` file automatically if it exists in the project root.

Example Configuration File
--------------------------

Here's an example configuration file:

.. code-block:: yaml

    # This file overrides the severity levels for the commit rules. 
    # All other fields are inherited from the default rules defined in the package.

    # Available severity levels:
    # - IGNORE: The rule is ignored and not enforced. Dependent rules are also ignored.
    # - WARNING: The rule is applied, but violations will only report warnings.
    # - ERROR: The rule is enforced, and violations must be fixed.

    # Rule 01: Check header length
    "01": IGNORE

    # Rule 02: Tries to find a colon ':' in the header preceded by exactly one word
    "02": ERROR

    # Rule 03: Cannot have a ':' with no [a-z] char preceding it
    "03": ERROR

Available Severity Levels
-------------------------

The following severity levels can be specified for any rule:

- **IGNORE**: The rule is ignored and not enforced. Dependent rules are also ignored if this rule is set to `IGNORE`.
- **WARNING**: The rule is enforced, but violations will only result in warnings.
- **ERROR**: The rule is enforced, and violations will result in errors that must be fixed.

.. note::
   Only the `severity` field can be overridden in the configuration file. All other fields,
   such as `id`, `description`, and `check` function, will remain as defined in the default rules.

Troubleshooting
---------------

- Ensure that the configuration file is properly formatted as YAML.
- If a rule ID is not specified in the file, the package will use the default severity for that rule.
- If the configuration file is malformed or missing, the package will log a warning and fall
  back to using default rules.
