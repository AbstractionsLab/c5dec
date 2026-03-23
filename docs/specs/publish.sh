#!/bin/bash
# This script is used to publish specifications using Doorstop and a C5-DEC Python script for keyword replacement.
# It first runs a Python script to replace keywords in the specifications, then publishes the specifications using Doorstop, and finally runs the Python script again to undo the keyword replacement.
# Ensure the script is executable
# chmod +x ./docs/specs/publish.sh

echo Usage guide:
echo ---
echo ./c5dec.sh
echo ... to publish tech specs without the CC database
echo ./publish.sh keep-cc
echo ... to keep CC database in published tech specs
echo ---

# Run c5 keyword replacement with "replace" argument
poetry run python ./SpecEngine/c5-keyword.py ./trp replace

# Render Mermaid diagrams in spec items (one-way, idempotent)
poetry run python ./SpecEngine/c5mermaid.py .

# Parse the "keep-cc" argument
if [[ "$@" == *"keep-cc"* ]]; then
    poetry run python ./SpecEngine/c5publish.py --include-cc-db
else
    poetry run python ./SpecEngine/c5publish.py
fi

# Run c5 keyword replacement with "undo" argument
poetry run python ./SpecEngine/c5-keyword.py ./trp undo

# Undo Mermaid diagram encoding (restore readable ```mermaid blocks)
poetry run python ./SpecEngine/c5mermaid.py . undo

# Generate traceability statistics (console + HTML report)
poetry run python ./SpecEngine/c5traceability.py --config ./SpecEngine/c5traceability_config.yaml --csv ./docs/publish/traceability.csv --html

# Generate interactive specification item browser
poetry run python ./SpecEngine/c5browser.py

poetry run python ./SpecEngine/c5publish.py --linkify-only

# Generate interactive Cytoscape.js traceability graph
poetry run python ./SpecEngine/c5graph.py

# Recompute references content fingerprints for dependency impact analysis.
# Items whose referenced files have changed since the last run are flagged as
# [STALE]; their stored fingerprint is updated in-place.
poetry run python ./SpecEngine/c5fingerprint.py