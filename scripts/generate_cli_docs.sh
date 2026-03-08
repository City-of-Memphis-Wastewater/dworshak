#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="docs/cli"
mkdir -p "$OUT_DIR"

strip_ansi() {
    sed 's/\x1B\[[0-9;?]*[ -/]*[@-~]//g'
}

generate_doc() {
    local cmd="$1"
    local file="${cmd// /_}.md"

    echo "Generating $OUT_DIR/$file"

    {
        echo "# $cmd"
        echo
        echo '```console'
        NO_COLOR=1 $cmd --help 2>&1 | strip_ansi
        echo '```'
    } > "$OUT_DIR/$file"
}

commands=(
"dworshak"
"dworshak config"
"dworshak env"
"dworshak env get"
"dworshak env set"
"dworshak env remove"
"dworshak env list"
"dworshak prompt"
"dworshak secret"
"dworshak secret vault"
)

rm -f "$OUT_DIR"/*.md

for cmd in "${commands[@]}"; do
    generate_doc "$cmd"
done

echo "CLI docs generated in $OUT_DIR"
