#!/bin/bash

# don't judge me for this script.

# Find the project root by looking for the .git directory
function find_project_root() {
    local current_dir="$1"
    while [[ "$current_dir" != "" && ! -d "$current_dir/.git" ]]; do
        current_dir=$(dirname "$current_dir")
    done
    echo "$current_dir"
}

# Get the directory of the running script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Find the project root
PROJECT_ROOT=$(find_project_root "$SCRIPT_DIR")

# Validate that the project root was found
if [[ -z "$PROJECT_ROOT" ]]; then
    echo "Error: Unable to find the project root."
    exit 1
fi

# Define relative paths to Doorstop repositories
PATH_TO_DB="c5dec/assets/database/SecurityControls"
PATH_TO_REQ="docs/reqs"

# Convert relative paths to absolute paths
REPO1_ABS_PATH="$PROJECT_ROOT/$PATH_TO_DB"
REPO2_ABS_PATH="$PROJECT_ROOT/$PATH_TO_REQ"

user_input="$1"

if [ "$user_input" == "db" ]; then
    cd "$REPO1_ABS_PATH"
    echo "$(pwd)"
    mkdir .git
    doorstop "${@:2}"
    rm -rf .git
elif [ "$user_input" == "req" ]; then
    cd "$REPO2_ABS_PATH"
    echo "$(pwd)"
    mkdir .git
    doorstop "${@:2}"
    rm -rf .git
fi 

