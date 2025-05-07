#!/bin/bash
# This script is used to publish specifications using Doorstop and a C5-DEC Python script for keyword replacement.
# It first runs a Python script to replace keywords in the specifications, then publishes the specifications using Doorstop, and finally runs the Python script again to undo the keyword replacement.
# Ensure the script is executable
# chmod +x ./docs/specs/c5proc-doorstop-pub.sh

# Run the Python script with "replace" argument
python ./c5-keyword.py ./tra replace
python ./c5-keyword.py ./trb replace
python ./c5-keyword.py ./trs replace

# Run the doorstop publish command
# doorstop publish -H all ./publish
python ./c5publish.py

# Run the Python script with "undo" argument
python ./c5-keyword.py ./tra undo
python ./c5-keyword.py ./trb undo
python ./c5-keyword.py ./trs undo