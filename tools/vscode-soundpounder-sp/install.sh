#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ext_src="${repo_root}/tools/vscode-soundpounder-sp"

name="$(python3 - <<'PY'
import json, pathlib
p = pathlib.Path("tools/vscode-soundpounder-sp/package.json")
j = json.loads(p.read_text())
print(j["name"], j["publisher"], j["version"])
PY
)"

ext_name="$(awk '{print $1}' <<<"$name")"
publisher="$(awk '{print $2}' <<<"$name")"
version="$(awk '{print $3}' <<<"$name")"

extensions_dir="${VSCODE_EXTENSIONS_DIR:-$HOME/.vscode/extensions}"
target="${extensions_dir}/${publisher}.${ext_name}-${version}"

mkdir -p "${extensions_dir}"
rm -rf "${target}"
mkdir -p "${target}"

# Copy extension files. Keep it simple; no build step.
cp -R "${ext_src}/." "${target}/"

echo "Installed to: ${target}"
echo "Reload VS Code to apply."

