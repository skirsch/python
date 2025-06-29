#!/bin/bash

# run from WSL
# stk@stk-home:~/GitHub/python$ ./checkin_all.sh

# Parent directory containing all your Git repos
PARENT_DIR="/home/stk/GitHub" # note the capital H
COMMIT_MSG="Auto commit and push all modified files"

cd "$PARENT_DIR" || exit

for dir in */; do
  REPO_PATH="$PARENT_DIR/$dir"
  cd "$REPO_PATH" || continue

  if [ -d ".git" ]; then
    echo "=== Processing $dir ==="

    # Ensure remote uses SSH
    REMOTE_URL=$(git remote get-url origin)

    if [[ "$REMOTE_URL" =~ ^https://([^@]+@)?github\.com[:/](.*)/(.*)\.git$ ]]; then
        USER=${BASH_REMATCH[2]}
        REPO=${BASH_REMATCH[3]}
        SSH_URL="git@github.com:$USER/$REPO.git"
        echo "Fixing remote: $REMOTE_URL → $SSH_URL"
        git remote set-url origin "$SSH_URL"
    fi

    # Stage and commit changes if needed
    git add -A
    if ! git diff --cached --quiet; then
      git commit -m "$COMMIT_MSG"
    fi

    # Push if ahead of upstream
    if git rev-parse --abbrev-ref --symbolic-full-name @{u} > /dev/null 2>&1; then
      LOCAL=$(git rev-parse @)
      REMOTE=$(git rev-parse @{u})
      if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Pushing $dir..."
        git push
      else
        echo "Nothing to push in $dir"
      fi
    else
      echo "No upstream tracking set. Skipping push in $dir"
    fi
  fi
done
