=========================
Rules Configuration
=========================

The purpose of the ``rules.yml`` file is to define commit rules for the project, ensuring consistency and adherence to established guidelines. Each rule within the file specifies certain criteria that commits must meet in order to be accepted.

The commit rules are structured in the following format:

Rule Fields
===========

Each rule contains the following fields:

- **id**: A unique identifier for the rule (string).
- **description**: A brief description of the rule's purpose (string).
- **check**: The function or method to be executed for this rule (string). 
  The value of the ``check`` field is matched to the method name of the  **component** it applies to
  (``HEADER``, ``BODY``, or ``FOOTER``). The method with the same name as the ``check`` field is
  called to run the rule.
- **component**: The component to which the rule applies. Possible values are:
  
  - ``HEADER``: Rule applies to the commit message header.
  - ``FOOTER``: Rule applies to the commit message footer.
  - ``BODY``: Rule applies to the commit message body.
  
- **severity**: The level of severity for the rule violation. Possible values are:
  
  - ``ERROR``: Indicates a serious issue that must be addressed.
  - ``WARNING``: Indicates a minor issue that should be addressed.
  - ``INFO``: Provides informational messages or suggestions.
  - ``IGNORE``: The rule is ignored and does not trigger any action.

- **dependencies**: Other rules that this rule depends on. This can be:
  
  - ``null``: No dependencies.
  - ``[]``: An empty list, indicating no dependencies.
  - ``[dependency1, dependency2]``: A list of dependent rule IDs.


Check Field
-----------



Example Rule
============

Here is an example rule defined within the ``rules.yml`` file:

.. code-block:: yaml

   - id: "01"
     description: "Check header length"
     check: length # remove
     component: HEADER # remove
     severity: WARNING
     dependencies: null

This rule checks the length of the commit message header and raises a warning if it violates the specified length constraint.

Ignoring Rules with Dependencies
================================

If a rule is marked with a severity of ``IGNORE``, any rules that depend on the ignored rule will also be ignored. This ensures strict dependency enforcement within the system, meaning that a rule cannot run if its required prerequisite (dependency) has been skipped.

For example, if **Rule 01** is ignored and **Rule 02** depends on it, then **Rule 02** will not be executed. This design ensures that rules are only run when their dependent checks are properly validated, preventing incomplete or inconsistent rule evaluations.


Defined Rules
=============

Here are the current rules defined in the ``rules.yml`` file:

1. **Rule 01**: Check header length
   - **Severity**: Warning
   - **Dependencies**: None
   
...

