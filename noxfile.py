import nox


py_versions = [
    "3.6",
    "3.7",
    "3.8",
    "3.9",
]


@nox.session
def lint(session):

    """
    Lint all files in priwo.
    """

    session.install("black")
    session.run("black", ".")


@nox.session(
    python=py_versions,
    reuse_venv=True,
)
def tests(session):

    """
    Run tests for priwo.
    """

    # Install dependencies.
    session.install(
        "pytest",
        "pytest-cov",
        "deepdiff",
    )

    # Install the package in development mode.
    session.run(
        "pip",
        "install",
        "-e",
        ".",
    )

    # Run the tests using pytest and generate a coverage report.
    session.run(
        "pytest",
        "-vv",
        "--cov",
        "--cov-report",
        "term-missing",
        "tests",
    )