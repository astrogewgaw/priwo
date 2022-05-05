import nox

vers = ["3.6", "3.7", "3.8", "3.9", "3.10"]
deps = ["pytest", "deepdiff", "pytest-cov", "pytest-clarity"]


@nox.session(python=vers, reuse_venv=True)
def tests(session):
    session.install(*deps)
    session.run("pip", "install", "-e", ".")
    session.run("pytest", "-vv", "--cov", "--cov-report", "term-missing", "tests")
