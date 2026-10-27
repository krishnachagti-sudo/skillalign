#!/bin/sh
# Rebuild the site from the COMMITTED code and push dist/ to the gh-pages
# branch (served by GitHub Pages). Refuses to run with uncommitted changes,
# so what is live always matches a commit on main.
set -e
cd "$(dirname "$0")"
if [ -n "$(git status --porcelain)" ]; then
  echo "Uncommitted changes. Commit them first, so the live site matches a commit:" >&2
  git status --short >&2
  exit 1
fi
python3 build.py
touch dist/.nojekyll   # serve files as-is, no Jekyll processing
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
cp -R dist/. "$TMP"
cd "$TMP"
git init -q -b gh-pages
git add -A
git commit -q -m "Publish site from $(git -C "$OLDPWD" rev-parse --short HEAD)"
git push -q -f https://github.com/krishnachagti-sudo/skillalign.git gh-pages
echo "published: https://krishnachagti-sudo.github.io/skillalign/"
