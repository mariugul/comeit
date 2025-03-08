from invoke import task


@task
def format(c):
    """Run ruff formatter and check."""
    c.run("ruff format")
    c.run("ruff check --fix")


@task
def test(c):
    """Run unit tests."""
    c.run("pytest comeit/tests")


@task
def all(c):
    """Run format and test tasks."""
    format(c)
    test(c)
