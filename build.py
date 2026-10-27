"""Build the static website into dist/.

dist/ is self-contained: the page, its CSS/JS, the Python engine and
the data files. Upload the whole folder to any static host.

Run:  python build.py
Then: python -m http.server 8040 --directory dist
"""

import hashlib
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "site"), DIST)

    files = []
    for folder, pattern in (("engine", ".py"), ("data", "")):
        os.makedirs(os.path.join(DIST, "py", folder), exist_ok=True)
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            if name.startswith((".", "__")) and name != "__init__.py":
                continue
            if pattern and not name.endswith(pattern):
                continue
            if name.endswith((".pyc",)):
                continue
            shutil.copy(os.path.join(ROOT, folder, name), os.path.join(DIST, "py", folder, name))
            files.append(f"{folder}/{name}")

    # a content hash in every URL, so browsers never mix old and new files
    digest = hashlib.sha1()
    for folder in ("site", "engine", "data"):
        for name in sorted(os.listdir(os.path.join(ROOT, folder))):
            path = os.path.join(ROOT, folder, name)
            if os.path.isfile(path) and not name.endswith(".pyc"):
                digest.update(open(path, "rb").read())
    version = digest.hexdigest()[:10]
    with open(os.path.join(DIST, "py", "manifest.json"), "w") as f:
        json.dump({"version": version, "files": files}, f, indent=1)
    index = os.path.join(DIST, "index.html")
    html = open(index, encoding="utf-8").read()
    html = html.replace('href="style.css"', f'href="style.css?v={version}"').replace('src="app.js"', f'src="app.js?v={version}"')
    open(index, "w", encoding="utf-8").write(html)
    shutil.copy(os.path.join(ROOT, "data", "job_postings.csv"), os.path.join(DIST, "sample_postings.csv"))
    print(f"built {DIST} with {len(files)} engine/data files")


if __name__ == "__main__":
    main()
