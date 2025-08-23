SRC="$HOME/.gitattributes"
find -H "$HOME/GitHub" -name .git -print0 |
while IFS= read -r -d '' gitpath; do
  repo="$(dirname "$gitpath")"
  if git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    if ! cmp -s "$SRC" "$repo/.gitattributes" 2>/dev/null; then
      install -m 0644 "$SRC" "$repo/.gitattributes"
      echo "Updated: $repo/.gitattributes"
    fi
  fi
done
