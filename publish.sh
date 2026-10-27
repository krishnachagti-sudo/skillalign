#!/bin/sh
# Rebuild the site and push dist/ to the gh-pages branch (served by GitHub Pages).
set -e
cd "$(dirname "$0")"
python3 build.py
touch dist/.nojekyll   # serve files as-is, no Jekyll processing
TMP=$(mktemp -d)
cp -R dist/. "$TMP"
cd "$TMP"
git init -q -b gh-pages
git add -A
git commit -q -m "Publish site"
git push -q -f https://github.com/krishnachagti-sudo/skillalign.git gh-pages
rm -rf "$TMP"
echo "published: https://krishnachagti-sudo.github.io/skillalign/"
