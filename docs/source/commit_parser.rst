Commit Message Parser
======================

Overview
--------
The commit message parser is designed to extract and organize commit message components into a structured format. It identifies the summary, body, and footer from commit messages that follow common conventions.

Features
--------
The commit parser offers several key features. First, it performs summary extraction by capturing the first line of the commit message and designating it as the summary.

Next, it includes body extraction, which collects all lines that follow the summary while excluding any footer lines.

In addition, the parser recognizes and collects footer lines, accommodating special tags such as “BREAKING CHANGE” as well as any user-defined footer labels.

Moreover, the parser effectively handles whitespace, preserving leading and trailing whitespace and newlines to maintain the original formatting of the commit message.

Finally, it incorporates error handling by raising a ValueError when an empty commit message is provided, thus preventing potential processing errors.