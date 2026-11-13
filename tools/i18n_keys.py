"""Keep the translation files in step with the page.

Every element in site/index.html marked data-i18n is translated by its own
first piece of text, and that English text is the key. This script lists
those keys and adds any missing ones (with an empty value) to each
site/i18n/<lang>.txt, keeping translations and the note at the top. An empty value
means "not translated yet": the page shows English for it.

Run:  python3 tools/i18n_keys.py
"""

import os
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.contrib import read_pairs, write_pairs  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, "site", "index.html")
LANGS = ["hi", "mr"]
VOID = {"input", "br", "img", "meta", "link", "use", "source", "hr"}


class _Keys(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []      # per open element: [is_marked, key_found]
        self.keys = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append([any(k == "data-i18n" for k, _ in attrs), False])

    def handle_endtag(self, tag):
        if tag not in VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        text = " ".join(data.split())
        if text and self.stack and self.stack[-1][0] and not self.stack[-1][1]:
            self.stack[-1][1] = True
            if text not in self.keys:
                self.keys.append(text)


def page_keys():
    parser = _Keys()
    with open(PAGE, encoding="utf-8") as f:
        parser.feed(f.read())
    return parser.keys


def sync():
    keys = page_keys()
    for lang in LANGS:
        path = os.path.join(ROOT, "site", "i18n", f"{lang}.txt")
        old = read_pairs(path) if os.path.exists(path) else {}
        with open(path, encoding="utf-8") as f:
            note = "".join(line for line in f if line.startswith("#"))
        new = {k: old.get(k, "") for k in keys}
        write_pairs(path, new, note)
        done = sum(1 for v in new.values() if v)
        print(f"{lang}: {done} of {len(keys)} translated")


if __name__ == "__main__":
    sync()
