#!/usr/bin/env bash
set -euo pipefail

PARENT_DIR="/home/stk/GitHub"
COMMIT_MSG="Auto commit and push all modified files"

cd "$PARENT_DIR"

find . -maxdepth 1 -mindepth 1 -type d -print0 | while IFS= read -r -d '' dir; do
  REPO_PATH="$(realpath "$dir")"
  cd "$REPO_PATH" || continue

  if [ ! -d .git ]; then
    echo "=== Skipping (no .git): $REPO_PATH ==="
    cd "$PARENT_DIR"
    continue
  fi

  echo "=== Processing: $REPO_PATH ==="

  # Normalize origin to SSH if it's a GitHub HTTPS remote
  if git remote get-url origin >/dev/null 2>&1; then
    REMOTE_URL="$(git remote get-url origin)"
    if [[ "$REMOTE_URL" =~ ^https://([^/]+)/([^/]+)/([^/]+?)(\.git)?$ ]] && [[ "${BASH_REMATCH[1]}" == "github.com" ]]; then
      USER="${BASH_REMATCH[2]}"
      REPO="${BASH_REMATCH[3]}"
      SSH_URL="git@github.com:${USER}/${REPO}.git"
      if [ "$REMOTE_URL" != "$SSH_URL" ]; then
        echo "  Remote: $REMOTE_URL -> $SSH_URL"
        git remote set-url origin "$SSH_URL"
      fi
    fi
  fi

  # Optional: bring branch up-to-date before committing (safe rebase)
  if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    git pull --rebase --autostash || true
  fi

  # Stage and commit if needed
  # First, normalize line endings according to .gitattributes
  git add --renormalize .
  git add -A

  if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
  fi

  # Determine current branch
  BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo 'HEAD')"
  if [ "$BRANCH" = "HEAD" ]; then
    echo "  Detached HEAD; skipping push."
    cd "$PARENT_DIR"
    continue
  fi

  # Push (set upstream if missing)
  if git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    LOCAL="$(git rev-parse @)"
    REMOTE="$(git rev-parse @{u})"
    if [ "$LOCAL" != "$REMOTE" ]; then
      echo "  Pushing ${BRANCH}..."
      git push
    else
      echo "  Nothing to push."
    fi
  else
    echo "  No upstream; pushing with -u..."
    git push -u origin "$BRANCH" || true
  fi

  cd "$PARENT_DIR"
done
# If we reach here, all repositories have been processed
echo "=== All repositories processed successfully ==="  
# Ensure the script exits with a success status
exit 0  
