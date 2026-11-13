"""Build the static website into dist/.

dist/ is self-contained: the page, its CSS/JS, the Python engine, the
data files, a self-hosted copy of Pyodide, and a service worker that
caches all of it so the site works offline after the first visit.

Only the files listed below are shipped, so a stray file in site/ or
data/ is never published by accident.

Run:  python build.py
Then: python -m http.server 3025 --directory dist
"""

import hashlib
import json
import os
import shutil

from engine.dataset import parse_example_syllabus
from tools.contrib import read_faq, read_pairs

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

SITE_FILES = ["index.html", "app.js", "style.css"]
ENGINE_FILES = ["__init__.py", "taxonomy.py", "dataset.py", "demand.py", "alignment.py", "learner.py", "api.py"]
DATA_FILES = ["skills.json", "programs.json", "job_postings.csv"]
LAZY_DATA = {"real": "real_postings_india_2026.csv"}   # fetched only when the user picks that dataset
PYODIDE_FILES = ["pyodide.js", "pyodide.asm.js", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json", "NOTICE.md"]


def LANGS():
    return sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, "site", "i18n")) if f.endswith(".txt"))


def example_files():
    """Contributed example syllabi; a name starting with _ is a template, not an example."""
    folder = os.path.join(ROOT, "data", "example_syllabi")
    return sorted(f for f in os.listdir(folder) if f.endswith(".txt") and not f.startswith("_"))


def load_examples():
    out = []
    for f in example_files():
        with open(os.path.join(ROOT, "data", "example_syllabi", f), encoding="utf-8") as fh:
            ex = parse_example_syllabus(fh.read())
        out.append({"id": f[:-4], **ex})
    return out


def copy(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(src, dst)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)

    extra = [os.path.join(ROOT, "site", "i18n", f) for f in sorted(os.listdir(os.path.join(ROOT, "site", "i18n")))] + \
            [os.path.join(ROOT, "site", "faq.txt")] + \
            [os.path.join(ROOT, "data", "example_syllabi", f) for f in example_files()]
    sources = extra + [os.path.join(ROOT, "site", f) for f in SITE_FILES] + \
              [os.path.join(ROOT, "engine", f) for f in ENGINE_FILES] + \
              [os.path.join(ROOT, "data", f) for f in DATA_FILES + list(LAZY_DATA.values())]
    digest = hashlib.sha1()
    for path in sources:
        with open(path, "rb") as f:
            digest.update(f.read())
    version = digest.hexdigest()[:10]

    for f in SITE_FILES:
        copy(os.path.join(ROOT, "site", f), os.path.join(DIST, f))
    py_files = [f"engine/{f}" for f in ENGINE_FILES] + [f"data/{f}" for f in DATA_FILES]
    lazy = {name: f"data/{f}" for name, f in LAZY_DATA.items()}
    for rel in py_files + list(lazy.values()):
        copy(os.path.join(ROOT, rel), os.path.join(DIST, "py", rel))
    for f in PYODIDE_FILES:
        copy(os.path.join(ROOT, "vendor", "pyodide", f), os.path.join(DIST, "vendor", "pyodide", f))
    copy(os.path.join(ROOT, "data", "job_postings.csv"), os.path.join(DIST, "sample_postings.csv"))
    # translations (site/i18n/<lang>.json) and contributed example syllabi (data/example_syllabi/*.txt)
    os.makedirs(os.path.join(DIST, "i18n"), exist_ok=True)
    for lang in LANGS():
        with open(os.path.join(DIST, "i18n", f"{lang}.json"), "w", encoding="utf-8") as f:
            json.dump(read_pairs(os.path.join(ROOT, "site", "i18n", f"{lang}.txt")), f, ensure_ascii=False)
    with open(os.path.join(DIST, "faq.json"), "w", encoding="utf-8") as f:
        json.dump([x for x in read_faq(os.path.join(ROOT, "site", "faq.txt")) if x["a"]], f, ensure_ascii=False)
    with open(os.path.join(DIST, "examples.json"), "w", encoding="utf-8") as f:
        json.dump(load_examples(), f, ensure_ascii=False, indent=1)
    # the licence and the list of changes travel with the real data file
    copy(os.path.join(ROOT, "docs", "DATA-SOURCES.md"), os.path.join(DIST, "py", "data", "DATA-SOURCES.md"))

    with open(os.path.join(DIST, "py", "manifest.json"), "w") as f:
        json.dump({"version": version, "files": py_files, "lazy": lazy}, f, indent=1)

    # a content hash in every URL, so browsers never mix old and new files
    index = os.path.join(DIST, "index.html")
    with open(index, encoding="utf-8") as f:
        html = f.read()
    html = html.replace('href="style.css"', f'href="style.css?v={version}"')
    html = html.replace('<script src="app.js" defer></script>',
                        f'<script>window.SKILLALIGN_VERSION = "{version}";</script>\n'
                        f'<script src="app.js?v={version}" defer></script>')
    with open(index, "w", encoding="utf-8") as f:
        f.write(html)

    precache = ["./", f"style.css?v={version}", f"app.js?v={version}", f"py/manifest.json?v={version}",
                f"examples.json?v={version}"] + \
               [f"i18n/{lang}.json?v={version}" for lang in LANGS()] + [f"faq.json?v={version}"] + \
               [f"py/{rel}?v={version}" for rel in py_files] + \
               [f"vendor/pyodide/{f}" for f in PYODIDE_FILES if f != "NOTICE.md"]
    with open(os.path.join(DIST, "sw.js"), "w") as f:
        f.write(SERVICE_WORKER.replace("__VERSION__", version).replace("__PRECACHE__", json.dumps(precache, indent=1)))
    print(f"built {DIST} (version {version}, {len(py_files)} engine/data files)")


SERVICE_WORKER = """// Generated by build.py. Caches the whole site so it works offline after
// the first visit (useful when venue Wi-Fi fails during a demo).
const CACHE = "skillalign-__VERSION__";
const PRECACHE = __PRECACHE__;

self.addEventListener("install", (event) => {
  // cache: "reload" skips the browser's HTTP cache, so a fresh publish is never mixed with old files
  event.waitUntil(caches.open(CACHE)
    .then((c) => c.addAll(PRECACHE.map((u) => new Request(u, { cache: "reload" }))))
    .then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(caches.keys()
    .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== location.origin) return;
  const scope = new URL(self.registration.scope);
  if (event.request.mode === "navigate") {
    // the page itself: network first so a new version is picked up, cache when offline.
    // Only a successful load of the app's own page is cached, never an error page.
    const isApp = url.pathname === scope.pathname || url.pathname === scope.pathname + "index.html";
    event.respondWith(fetch(event.request)
      .then((res) => {
        if (res.ok && isApp) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put("./", copy)); }
        return res;
      })
      .catch(() => caches.match("./")));
    return;
  }
  // everything else: cache first; large optional files (the real dataset) are cached the first time they are used
  event.respondWith(caches.match(event.request).then((hit) => hit || fetch(event.request).then((res) => {
    if (res.ok && url.pathname.includes("/py/data/")) { const copy = res.clone(); caches.open(CACHE).then((c) => c.put(event.request, copy)); }
    return res;
  })));
});
"""


if __name__ == "__main__":
    main()
