#!/bin/bash

PARENT_DIR="/home/stk/GitHub" # note the capital H

cd "$PARENT_DIR" || exit 1

for dir in */; do
  REPO_PATH="$PARENT_DIR/$dir"
  cd "$REPO_PATH" || continue

  if [ -d ".git" ]; then
    echo "=== Pulling updates for $dir ==="

    # Optional: check current branch
    CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

    # Fetch and pull from origin
    git fetch origin "$CURRENT_BRANCH"
    git pull origin "$CURRENT_BRANCH"
    
    echo ""
  fi
done

echo "Script completed at: $(date)"
