"""Loading job postings and training programs.

Job postings come from a CSV with at least: title, description, date
(YYYY-MM-DD). Optional columns: sector, city. Anyone can export their
own postings into this shape and upload them.

Training programs come from JSON: each program has modules, and each
module has hours and an outline. Skills are read out of the outline
text, so a syllabus can be pasted in as plain text.
"""

import csv
import io
import json
from dataclasses import dataclass, field

REQUIRED_COLUMNS = ("title", "description", "date")


@dataclass
class Posting:
    title: str
    description: str
    date: str
    quarter: str
    sector: str = ""
    city: str = ""
    skills: set = field(default_factory=set)


@dataclass
class Module:
    title: str
    hours: float
    outline: str
    skills: set = field(default_factory=set)


@dataclass
class Program:
    id: str
    name: str
    provider: str
    sector: str
    duration: str
    target_roles: list
    modules: list

    def skills(self):
        taught = set()
        for module in self.modules:
            taught |= module.skills
        return taught

    def total_hours(self):
        return sum(m.hours for m in self.modules)

    def hours_by_skill(self):
        """Split each module's hours evenly across the skills it teaches."""
        hours = {}
        for module in self.modules:
            if not module.skills:
                continue
            share = module.hours / len(module.skills)
            for skill_id in module.skills:
                hours[skill_id] = hours.get(skill_id, 0) + share
        return hours


def quarter_of(date_text):
    """'2025-08-14' -> '2025-Q3'."""
    parts = date_text.strip().split("-")
    if len(parts) < 2 or not parts[0].isdigit() or not parts[1].isdigit():
        raise ValueError(f"date must look like YYYY-MM-DD, got '{date_text}'")
    year, month = int(parts[0]), int(parts[1])
    if not 1 <= month <= 12:
        raise ValueError(f"month out of range in '{date_text}'")
    return f"{year}-Q{(month - 1) // 3 + 1}"


def parse_postings(csv_text, extractor):
    """Parse CSV text into Posting objects with their skills extracted.

    Returns (postings, problems) where problems lists rows that were
    skipped and why, so a bad upload explains itself instead of failing.
    """
    reader = csv.DictReader(io.StringIO(csv_text.lstrip("﻿")))
    columns = [c.strip().lower() for c in (reader.fieldnames or [])]
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        raise ValueError("CSV is missing column(s): " + ", ".join(missing))

    postings, problems = [], []
    for line_no, raw in enumerate(reader, start=2):
        row = {k.strip().lower(): (v or "").strip() for k, v in raw.items() if k}
        if not row.get("title") or not row.get("description"):
            problems.append(f"line {line_no}: empty title or description")
            continue
        try:
            quarter = quarter_of(row["date"])
        except ValueError as err:
            problems.append(f"line {line_no}: {err}")
            continue
        postings.append(Posting(
            title=row["title"],
            description=row["description"],
            date=row["date"],
            quarter=quarter,
            sector=row.get("sector", ""),
            city=row.get("city", ""),
            skills=extractor.extract(row["title"] + " " + row["description"]),
        ))
    return postings, problems


def load_postings(path, extractor):
    with open(path, encoding="utf-8") as f:
        return parse_postings(f.read(), extractor)


def build_program(raw, extractor):
    modules = []
    for m in raw["modules"]:
        modules.append(Module(
            title=m["title"],
            hours=float(m["hours"]),
            outline=m["outline"],
            skills=extractor.extract(m["title"] + " " + m["outline"]),
        ))
    return Program(
        id=raw["id"],
        name=raw["name"],
        provider=raw.get("provider", ""),
        sector=raw.get("sector", ""),
        duration=raw.get("duration", ""),
        target_roles=[r.lower() for r in raw["target_roles"]],
        modules=modules,
    )


def load_programs(path, extractor):
    with open(path, encoding="utf-8") as f:
        return [build_program(raw, extractor) for raw in json.load(f)]


def program_from_syllabus(name, target_roles, syllabus_text, extractor):
    """Turn a pasted syllabus into a Program.

    Each non-empty line is one module. A line may end with an hour count
    like "(40 hrs)" or "- 40h"; lines without one count as 10 hours.
    """
    import re
    hours_pattern = re.compile(r"[\(\-\s]*(\d+(?:\.\d+)?)\s*(?:hours|hrs|hr|h)\)?\s*$", re.IGNORECASE)
    modules = []
    for line in syllabus_text.splitlines():
        line = line.strip(" \t•*-")
        if not line:
            continue
        hours = 10.0
        match = hours_pattern.search(line)
        if match:
            hours = float(match.group(1))
            line = line[:match.start()].strip()
        modules.append({"title": line, "hours": hours, "outline": ""})
    if not modules:
        raise ValueError("the syllabus is empty")
    return build_program({
        "id": "custom",
        "name": name or "Your program",
        "provider": "Pasted syllabus",
        "target_roles": target_roles,
        "modules": modules,
    }, extractor)
