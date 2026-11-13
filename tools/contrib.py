"""Readers for the plain-text files teammates fill in on GitHub.

They are plain text on purpose: one line per item, nothing to escape,
so editing them in the browser cannot break the site.
"""


def read_pairs(path):
    """Translation file: `English text = translation` per line.

    Lines starting with # are notes. An empty right side means "not
    translated yet". Returns {english: translation} in file order."""
    pairs = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            left, sep, right = line.partition(" =")
            if not sep:
                raise ValueError(f'{path}: this line has no " = ": {line!r}')
            pairs[left.strip()] = right.strip()
    return pairs


def write_pairs(path, pairs, note):
    with open(path, "w", encoding="utf-8") as f:
        f.write(note.rstrip() + "\n\n")
        for k, v in pairs.items():
            f.write(f"{k} = {v}".rstrip() + "\n")


def read_faq(path):
    """FAQ file: a `Q:` line, then an `A:` line (which may run onto more lines).
    Returns [{"q", "a"}] including unanswered questions (a == "")."""
    items, current = [], None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.lstrip().startswith("#"):
                continue
            if line.startswith("Q:"):
                current = {"q": line[2:].strip(), "a": ""}
                items.append(current)
            elif line.startswith("A:") and current is not None:
                current["a"] = line[2:].strip()
            elif line.strip() and current is not None and current["a"]:
                current["a"] += " " + line.strip()
    return items


def read_ads(path):
    """Trade job ads: blocks of `Title:` `Date:` `Place:` `Link:` `Ad:` lines,
    separated by a `---` line. Blocks whose title says EXAMPLE are skipped.
    Returns CSV text that SkillAlign's upload reader takes."""
    import csv
    import io
    blocks, current = [], {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            if line == "---":
                if current:
                    blocks.append(current)
                current = {}
                continue
            key, colon, value = line.partition(":")
            if colon and key.strip().lower() in ("title", "date", "place", "link", "ad"):
                current[key.strip().lower()] = value.strip()
    if current:
        blocks.append(current)
    blocks = [b for b in blocks if "EXAMPLE" not in b.get("title", "")]
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["title", "date", "description", "district", "state", "source"])
    for b in blocks:
        district, _, state = b.get("place", "").partition(",")
        w.writerow([b.get("title", ""), b.get("date", ""), b.get("ad", ""), district.strip(), state.strip(), b.get("link", "")])
    return out.getvalue(), len(blocks)
