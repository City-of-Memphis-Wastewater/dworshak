#!/usr/bin/env bash
set -e

# --- CONFIG ---
INDEX_FILE="docs/index.md"
SVG_DIR="assets"
BASE_SVG_NAME="dworshak_v"
CLI_CMD="dworshak"

# --- Get current CLI version ---
VERSION=$($CLI_CMD --version | awk '{print $NF}')
echo "Detected Dworshak CLI version: $VERSION"

# --- Build new SVG filename ---
NEW_SVG="${SVG_DIR}/${BASE_SVG_NAME}${VERSION}_helptree.svg"
echo "New helptree SVG: $NEW_SVG"

# --- Replace old SVG reference in index.md ---
# Match any old dworshak_v<version>_helptree.svg
sed -i -E "s|${BASE_SVG_NAME}[0-9]+\.[0-9]+\.[0-9]+_helptree\.svg|${BASE_SVG_NAME}${VERSION}_helptree.svg|g" "$INDEX_FILE"

echo "Updated $INDEX_FILE to use version $VERSION"
