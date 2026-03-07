#!/usr/bin/env bash
set -e

OUT_DIR="docs/cli"
mkdir -p "$OUT_DIR"

# Strip ANSI escape codes for clean Markdown
strip_ansi() {
    sed 's/\x1B\[[0-9;]*[JKmsu]//g'
}

# Recursive function to generate CLI docs
generate_command_md() {
    local cmd_path=$1      # e.g., "dworshak secret vault"
    local out_file=$2      # output markdown file
    local title=$3         # heading in the markdown

    echo "# $title" > "$out_file"
    echo '```console' >> "$out_file"
    $cmd_path --help 2>&1 | strip_ansi >> "$out_file"
    echo '```' >> "$out_file"

    # Discover subcommands dynamically
    local subcommands
    subcommands=$($cmd_path --help 2>&1 | strip_ansi | awk '/Commands:/{flag=1;next}/Options:/{flag=0}flag {print $1}')
    
    for sub in $subcommands; do
        # Create a filename safe for Markdown
        local file_name=$(echo "$cmd_path"_"$sub" | tr ' ' '_').md
        local title_name="$cmd_path $sub"
        generate_command_md "$cmd_path $sub" "$OUT_DIR/$file_name" "$title_name"
    done
}

# Base CLI
BASE_CMD="dworshak"
generate_command_md "$BASE_CMD" "$OUT_DIR/dworshak.md" "$BASE_CMD CLI"

echo "Recursive CLI docs generated in $OUT_DIR"

