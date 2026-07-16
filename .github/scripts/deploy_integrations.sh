#!/usr/bin/env bash
set -euo pipefail

while IFS= read -r spec; do
  name=$(basename "$spec" .json)
  title=$(jq -r '.info.title' "$spec")
  version=$(jq -r '.info.version' "$spec")
  version_id="${title}:${version}"

  #size check for spec since this is not done when using ipctl to import
  size_bytes=$(stat -c%s "$spec" 2>/dev/null || stat -f%z "$spec")
  max_bytes=15728640  # 14.99 MB
  if [ "$size_bytes" -gt "$max_bytes" ]; then
    echo "⚠️  Skipping $name — spec too large ($(( size_bytes / 1048576 )) MB > 14.99 MB limit)"
    continue
  fi

  if ipctl describe integration-model "$version_id" > /dev/null 2>&1; then
    echo "🗑️  Deleting existing model: $version_id"
    ipctl delete integration-model "$version_id" || true
  fi

  echo "📥 Importing integration: $name"
  if ipctl import integration-model "$spec" --verbose; then
    echo "✅ Successfully imported: $name"
  else
    echo "⚠️  Skipping $name (import failed)"
  fi
done < <(echo "$CHANGED_SPECS" | jq -r '.[]')
