#!/usr/bin/env bash
set -e

mkdir -p docs/cli

echo "# dworshak CLI" > docs/cli/dworshak.md
echo '```' >> docs/cli/dworshak.md
dworshak --help >> docs/cli/dworshak.md
echo '```' >> docs/cli/dworshak.md

echo "# secret commands" > docs/cli/secret.md
echo '```' >> docs/cli/secret.md
dworshak secret --help >> docs/cli/secret.md
echo '```' >> docs/cli/secret.md

echo "# secret vault commands" > docs/cli/secret_vault.md
echo '```' >> docs/cli/secret_vault.md
dworshak secret vault --help >> docs/cli/secret_vault.md
echo '```' >> docs/cli/secret_vault.md

echo "# config commands" > docs/cli/config.md
echo '```' >> docs/cli/config.md
dworshak config --help >> docs/cli/config.md
echo '```' >> docs/cli/config.md

echo "# env commands" > docs/cli/env.md
echo '```' >> docs/cli/env.md
dworshak env --help >> docs/cli/env.md
echo '```' >> docs/cli/env.md

echo "# prompt commands" > docs/cli/prompt.md
echo '```' >> docs/cli/prompt.md
dworshak prompt --help >> docs/cli/prompt.md
echo '```' >> docs/cli/prompt.md
