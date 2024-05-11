#!/usr/bin/env bash
set -eu
# Function to print the help message
__print_help() {
    cat <<<"""
Usage: $0 [-h|--help] [-u|--update-version] [-i|--install [--dev]] [-t|--test] [-b|--build] [-p|--upload]

-h, --help:         Display this help message and exit.
-uv, --update-version:  Update the package version in pyproject.toml.
-i, --install:       Install dependencies from requirements.txt.
--install-dev:      Install development dependencies from requirements-dev.txt.
-t, --test:         Run tests for the current package.
-b, --build:        Build the new package.
-p, --upload, --publish:       Upload the project build to pypi.org.
"""
}

# Global variable for VERSION
VERSION=$(cat "VERSION")

# Updated function to handle different install options
__install_dependencies() {
    if [[ $1 == "--install-dev" ]] || [[ $2 == "--install-dev" ]]; then
        requirements_file="requirements-dev.txt"
        echo "Installing development dependencies..."
    else
        requirements_file="requirements.txt"
    fi

    if python3 -m pip install -r "$requirements_file" 2>&1 ; then
        echo "Successfully installed requirements"
    else
        echo "Failed to install requirements"
        exit 1
    fi
}

# Function to update the version
__update_version() {
    sed -E "s/version[[:space:]]*=[[:space:]]*\"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"${VERSION}\"/g" pyproject.toml | tee pyproject-temp.toml
    if mv pyproject-temp.toml pyproject.toml ; then
        echo "Successfully updated version in pyproject.toml"
        rm -rf pyproject-temp.toml
    else
        echo "Failed to update version in pyproject.toml"
        exit 1
    fi
}

# Function to run tests
__run_tests() {
    if python3 -m pytest tests/ 2>&1 ; then
        echo "Tests completed Successfully."
    else
        echo "Tests failed to complete successfully."
        exit 1
    fi
}

# Function to build the package
__build_package() {
    if python3 -m build 2>&1 ; then
        echo "Build ran Successfully."
    else
        echo "Build failed to complete successfully."
        exit 1
    fi
}

# Function to upload the package to pypi
__upload_package() {
  printf """\n
[pypi]
repository: https://upload.pypi.org/legacy/
username = $TWINE_USERNAME
password = $TWINE_PASSWORD
  """ > ~/.pypirc
  python3 -m twine upload \
  --verbose --skip-existing --non-interactive \
  --config-file ~/.pypirc \
  dist/*
  echo "Published to PyPI Successfully."
  return 0
}

# Main function to orchestrate the execution based on command-line arguments
main() {
    case "$1" in
        -h|--help)
            __print_help
            exit 0
            ;;
        -uv|--update-version)
            __update_version
            shift
            ;;
        -i|--install|--install-dev)
            __install_dependencies "$1" "$2"  # Use $2 to check for --install-dev option
            shift  # Shift twice to remove -i and --install-dev arguments, but once if only -i or --install-dev is provided
            [[ $# -gt 1 ]] && shift
            ;;
        -t|--test)
            __run_tests
            shift
            ;;
        -b|--build)
            __update_version
            __build_package
            shift
            ;;
        -p|--upload|--publish)
            __upload_package
            shift
            ;;
        *)
            printf "\e[31mUnrecognized option: $1\e[0m\n"
            __print_help
            exit 1
            ;;
    esac
    # Recursively call main with shifted arguments
    [[ "$1" ]] && main "$@"
}

# Cleanup build and dist artifacts
rm -rf dist/** && rm -rf build/**

# Call the main function with the command-line arguments
main "$@"
