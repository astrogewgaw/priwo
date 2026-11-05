pkg  := "priwo"

alias d := docs
alias c := clean
alias b := build
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
    rm -rf .cache
    rm -rf .coverage
    rm -rf .mypy_cache
    rm -rf docs/build/*
    rm -rf .pytest_cache
    fd -I -e pyc -x rm -rf
    fd -I __pycache__ -x rm -rf

# Build
@build:
  echo "Building..."
  rm -rf build
  mkdir -p build
  cd build && cmake .. && make -j`nproc`
  cd ..

# Install.
@install: && clean
    echo "Installing..."
    pip install --no-build-isolation -Ceditable.rebuild=true -ve .

# Uninstall.
@uninstall: && clean
    echo "Uninstalling {{pkg}}..."
    pip uninstall {{pkg}}
    rm -rf build
    rm -rf python/{{pkg}}.egg-info
    rm -rf python/{{pkg}}/_version.py

# Build docs.
@docs:
    echo "Building docs for {{pkg}}..."
    sphinx-reload docs
