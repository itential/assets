#!/usr/bin/env bash
set -euo pipefail

BASE_SHA=$(git log --pretty=format:'%P' -n 1 HEAD | awk '{print $1}')
ASSET_DIRS="Studio Projects|Agent Projects|Automations|LCM Resource Models|Golden Configs"
INTEGRATION_MODELS_DIR="OpenAPIs"

echo "Diffing against merge base $BASE_SHA"

# ── Asset diff ────────────────────────────────────────────────────────────────
# core.quotePath=false prevents git from quoting paths that contain spaces
CHANGED_FILES=$(git -c core.quotePath=false diff --name-only --diff-filter=AM "$BASE_SHA" HEAD \
  | { grep -E "(${ASSET_DIRS})/.*\.json$" || true; } | jq -R . | jq -sc .)
echo "changed_files: $CHANGED_FILES"
{
  echo "changed_files<<EOF"
  echo "$CHANGED_FILES"
  echo "EOF"
} >> "$GITHUB_OUTPUT"
count=$(echo "$CHANGED_FILES" | jq 'length')
if [ "$count" -gt 0 ]; then
  echo "Asset changes detected"
  echo "has_asset_changes=true" >> "$GITHUB_OUTPUT"
else
  echo "No asset changes detected — skipping asset deploy"
  echo "has_asset_changes=false" >> "$GITHUB_OUTPUT"
fi

# ── Integration spec diff ─────────────────────────────────────────────────────
CHANGED_SPECS=$(git -c core.quotePath=false diff --name-only --diff-filter=AM "$BASE_SHA" HEAD \
  | { grep "${INTEGRATION_MODELS_DIR}/.*-latest\.json$" || true; } | jq -R . | jq -sc .)
echo "changed_specs: $CHANGED_SPECS"

# Use heredoc format — GitHub Actions rejects bare JSON arrays as output values
{
  echo "changed_specs<<EOF"
  echo "$CHANGED_SPECS"
  echo "EOF"
} >> "$GITHUB_OUTPUT"
count=$(echo "$CHANGED_SPECS" | jq 'length')
if [ "$count" -gt 0 ]; then
  echo "Found $count changed spec(s)"
  echo "has_spec_changes=true" >> "$GITHUB_OUTPUT"
else
  echo "No integration spec changes detected — skipping integration deploy"
  echo "has_spec_changes=false" >> "$GITHUB_OUTPUT"
fi
