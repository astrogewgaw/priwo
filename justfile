pkg  := "priwo"

alias d := docs
alias t := test
alias c := clean
alias i := install
alias u := uninstall

# List available commands.
default:
  @just --choose

# Clean up.
@clean:
    echo "Cleaning..."
    rm -rf tmp
    rm -rf dist
    rm -rf .eggs
    rm -rf .coverage
    rm -rf .mypy_cache
    rm -rf docs/build/*
    rm -rf .pytest_cache
    fd -I -e pyc -x rm -rf
    fd -I __pycache__ -x rm -rf

# Install.
@install: && clean
    echo "Installing..."
    pip install -e . --no-build-isolation -Ceditable.rebuild=true -Cbuild-dir=build -v

# Uninstall.
@uninstall: && clean
    echo "Uninstalling {{pkg}}..."
    pip uninstall {{pkg}}
    rm -rf build/
    rm -rf src/{{pkg}}.egg-info
    rm -rf src/{{pkg}}/_version.py

# Run tests.
@test: && clean
  pytest -vv tests

# Build docs.
@docs:
    echo "Building docs for {{pkg}}..."
    sphinx-autobuild docs/source docs/build
