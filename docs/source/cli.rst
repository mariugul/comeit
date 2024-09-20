Command Line Interface (CLI)
============================

This section describes the command-line arguments available for configuring and running the application.

Overview
--------

The application can be configured through several command-line arguments, allowing customization of logging levels and specifying configuration files.

.. note::
   The CLI options may change in future versions, so it's always a good idea to check the most up-to-date documentation.

Usage Example
-------------

Here's an example of how to use the CLI:

.. code-block:: bash

   comeit --config-file path/to/config.yaml --log-level INFO

Arguments
---------

.. _cli-config-file:

``--config-file``
   **Type**: :class:`pathlib.Path`
   
   Path to the configuration file. This file can override the default severity levels of the rules.

   Example:

   .. code-block:: bash

      comeit --config-file path/to/config.yaml

.. _cli-log-level:

``--log-level``
   **Type**: :class:`comeit.LogLevel`
   **Default**: ``WARNING``
   
   Set the logging level for the application. You can choose from the following log levels:

   - ``DEBUG``: Detailed information, typically used for debugging.
   - ``INFO``: General information about the application’s process.
   - ``WARNING``: Indicates potential issues but not critical.
   - ``ERROR``: An error that has occurred but does not stop the application.
   - ``CRITICAL``: Severe errors that may prevent the application from continuing.

   Example:

   .. code-block:: bash

      comeit --log-level DEBUG

Configuration Arguments
-----------------------

All arguments passed via the command line are encapsulated in the ``ConfigArgs`` dataclass, which stores:

- ``config_file``: A string representing the path to the config file.
- ``log_level``: The selected log level (``LogLevel`` enum).

Future Updates
--------------

If the CLI options change in future releases, this document will be updated accordingly. Be sure to check the latest documentation to stay informed of any new options or behavior changes.
