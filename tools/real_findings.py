"""The real-data figures quoted in the report, computed in one place.

Every number SkillAlign states about the real postings comes from here,
with its definition in code and the matching titles printed so they can
be checked by hand. Writes docs/real_findings.md.

    python tools/real_findings.py [path/to/job_postings_2026_sample.csv]

With the raw Fliar file, it also measures how much of a skills list the
taxonomy recognises on HELD-OUT postings: the United States rows, which
were never looked at while the taxonomy was built (it was grown from the
India rows, so India coverage flatters it).
"""

import collections
import csv
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)

from engine.dataset import load_postings  # noqa: E402
from engine.taxonomy import SkillExtractor, load_taxonomy  # noqa: E402

# A hands-on trade posting is one whose TITLE names a trade job. Engineers, managers,
# designers and sales staff in trade industries are deliberately not counted.
TRADE_TITLE = re.compile(
    r"\b(electrician|wireman|lineman|welder|fitter|plumber|carpenter|mason|cnc operator|vmc operator|"
    r"machine operator|machinist|turner|tailor|sewing machine operator|beautician|hair stylist|ac technician|"
    r"hvac technician|refrigeration technician|solar technician|solar installer|ev technician|mechanic|"
    r"maintenance technician|electrical technician|production technician)\b", re.I)
NOT_TRADE = re.compile(r"\b(engineer|manager|lead|head|executive|analyst|developer|consultant|"
                       r"software|computer|laptop|aircraft|data|faculty|instructor|trainer)\b", re.I)
CARE_TITLE = re.compile(r"\b(nurse|ward attendant|ward boy|general duty assistant|gda|patient care assistant|"
                        r"caregiver|care giver|home health aide|patient attendant)\b", re.I)
NOT_CARE = re.compile(r"\b(faculty|instructor|entrance|medical coding|manager)\b", re.I)


def coverage(rows, extractor):
    items = [i.strip() for r in rows for i in r["skills"].split("|") if i.strip() and i.strip().lower() != "null"]
    hit = sum(1 for i in items if extractor.extract(i, as_list=True))
    postings = sum(1 for r in rows if extractor.extract(r["skills"], as_list=True))
    return len(rows), len(items), hit, postings


def main(raw=None):
    skills = load_taxonomy(os.path.join(ROOT, "data", "skills.json"))
    extractor = SkillExtractor(skills)
    postings, _ = load_postings(os.path.join(ROOT, "data", "real_postings_india_2026.csv"), extractor)
    n = len(postings)
    trade = [p for p in postings if TRADE_TITLE.search(p.title) and not NOT_TRADE.search(p.title)]
    care = [p for p in postings if CARE_TITLE.search(p.title) and not NOT_CARE.search(p.title)]
    trade_titles = collections.Counter(p.title for p in trade)
    care_titles = collections.Counter(p.title for p in care)

    lines = ["# Real-data findings", "",
             f"Computed by tools/real_findings.py from data/real_postings_india_2026.csv ({n:,} postings).", "",
             "## Hands-on trade and care jobs", "",
             f"- Hands-on trade postings (title names a trade job; engineers, managers and IT roles excluded): "
             f"{len(trade)} ({100 * len(trade) / n:.1f}%).",
             f"- Bedside care postings (nurse, ward attendant, general duty assistant, caregiver; teaching and "
             f"management roles excluded): "
             f"{len(care)} ({100 * len(care) / n:.1f}%).", "",
             "Trade titles counted, for checking by hand:", "",
             "; ".join(f"{t} ({c})" for t, c in trade_titles.most_common()), "",
             "Care titles counted:", "",
             "; ".join(f"{t} ({c})" for t, c in care_titles.most_common()), ""]

    if raw:
        with open(raw, encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["skills"].strip() and r["skills"].strip().lower() != "null"]
        lines += ["## How much of a skills list the taxonomy recognises", "",
                  "| Postings | Rows | Skill items | Items recognised | Postings with a recognised skill |",
                  "|---|---|---|---|---|"]
        for label, country in (("India (the taxonomy was grown from these)", "IN"),
                               ("United States (held out, never used to build it)", "US")):
            total, items, hit, with_skill = coverage([r for r in rows if r["country"] == country], extractor)
            lines.append(f"| {label} | {total:,} | {items:,} | {hit:,} ({100 * hit / items:.0f}%) | "
                         f"{with_skill:,} ({100 * with_skill / total:.0f}%) |")
        lines.append("")
    out = os.path.join(ROOT, "docs", "real_findings.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines)[:6000])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
