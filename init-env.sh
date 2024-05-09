#!/usr/bin/env bash

# Function to create a virtual environment
create_venv() {
    local venv_dir="$1"

    # Check if virtual environment already exists
    if [[ -d "$venv_dir" ]]; then
        echo "Virtual environment '$venv_dir' already exists."
        exit 1
    fi

    echo "Creating virtual environment...'$venv_dir'"
    # Create the virtual environment
    python3 -m venv "$venv_dir"
}

# Function to activate the virtual environment
activate_venv() {
    source "$1/bin/activate"
}

# Function to install the required packages
install_packages() {
    local venv_dir="$1"

    # Activate the virtual environment
    activate_venv "$venv_dir"

    # Upgrade pip first
    pip install --upgrade pip

    # Install development requirements
    pip install -r requirements-dev.txt

    # Deactivate virtual environment (important to do this in a subshell)
    deactivate
}

# Function to display help message
print_help() {
    cat << EOF
Usage: $0 [-h|--help] [-v|--venv VENV_DIR]

Creates a Python virtual environment and installs development packages.

Options:
-h, --help     Show this help message and exit.
-v, --venv     Specify the name and location of the virtual environment.
                Default is a new directory named .venv in the current folder.

Example:
  $0 -v my_env
This will create a virtual environment named 'my_env' in the current folder.
EOF
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case "$key" in
        -h|--help)
            print_help
            exit 0
            ;;
        -v|--venv)
            venv_dir="$2"
            shift  # Move to the next argument (the value)
            shift  # Move to the argument after the value
            ;;
        *)
            echo "Unknown option: $key"
            print_help
            exit 1
            ;;
    esac
done

# Set the default virtual environment name if not provided
venv_dir=${venv_dir:-.venv}

# Call the functions
create_venv "$venv_dir"
install_packages "$venv_dir"
source "$venv_dir/bin/activate"