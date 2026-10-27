"""Loading job postings and training programs.

Job postings come from a CSV with at least: title, date, and a
description and/or a skills column (e.g. "Python|SQL|Excel", as many
job-board exports provide). Optional columns: sector, district (or
city), state. Commas, semicolons,
tabs and pipes all work as separators. Dates may be YYYY-MM-DD or the
Indian DD-MM-YYYY / DD/MM/YYYY.

Skills are read from the description only, never the title: a title
like "Solar PV Technician" would otherwise count as every posting
asking for solar skills.

Training programs come from JSON: each program has modules, and each
module has hours and an outline. A pasted syllabus becomes a program
with one module per line.
"""

import csv
import io
import json
import math
import re
from dataclasses import dataclass, field
from datetime import date

REQUIRED_COLUMNS = ("title", "date")
TEXT_COLUMNS = ("description", "skills")
COLUMN_ALIASES = {"city": "district", "location": "district", "joblocation_address": "district",
                  "posted": "date", "posted_on": "date", "posted_date": "date", "postdate": "date",
                  "post_date": "date", "createddate": "date", "job_title": "title", "jobtitle": "title",
                  "job_description": "description", "jobdescription": "description", "job-desc": "description",
                  "key_skills": "skills", "key skills": "skills", "tagsandskills": "skills", "job_skills": "skills",
                  "industry": "sector", "category": "sector", "region": "state", "inferred_state": "state"}
MIN_YEAR, MAX_YEAR = 1990, 2100
MAX_HOURS = 10000
csv.field_size_limit(10_000_000)


@dataclass
class Posting:
    title: str
    description: str
    date: str
    quarter: str
    sector: str = ""
    district: str = ""
    state: str = ""
    skills: set = field(default_factory=set)


@dataclass
class Module:
    title: str
    hours: float
    outline: str
    mandatory: bool = False
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
    nsqf_level: str = ""
    qp_code: str = ""

    def skills(self):
        taught = set()
        for module in self.modules:
            taught |= module.skills
        return taught

    def mandatory_skills(self):
        """Skills taught ONLY in compulsory modules: never advised to cut."""
        optional = set()
        for m in self.modules:
            if not m.mandatory:
                optional |= m.skills
        return {s for m in self.modules if m.mandatory for s in m.skills} - optional

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

    def unmatched_hours(self):
        return sum(m.hours for m in self.modules if not m.skills)


def parse_date(text):
    """Accept YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY or DD/MM/YYYY; return a date."""
    text = re.sub(r"[T ]\d{1,2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?$", "", text.strip())
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", text)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", text)
        if not m:
            raise ValueError(f"date must look like 2025-08-14 or 14/08/2025, got '{text}'")
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if not MIN_YEAR <= y <= MAX_YEAR:
        raise ValueError(f"year {y} is outside {MIN_YEAR}-{MAX_YEAR} in '{text}'")
    try:
        return date(y, mo, d)
    except ValueError:
        raise ValueError(f"'{text}' is not a real date") from None


def quarter_of(date_text):
    """'2025-08-14' -> '2025-Q3'."""
    d = parse_date(date_text)
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def _reader(csv_text):
    """The separator is whichever of , ; tab | appears most in the header line."""
    header_line = csv_text.split("\n", 1)[0]
    delimiter = max(",;\t|", key=header_line.count)
    return csv.reader(io.StringIO(csv_text), delimiter=delimiter)


def parse_postings(csv_text, extractor):
    """Parse CSV text into Posting objects with their skills extracted.

    Returns (postings, problems): problems lists rows that were skipped
    and why, so a bad upload explains itself instead of failing.
    """
    csv_text = csv_text.lstrip("﻿")
    try:
        rows = iter(_reader(csv_text))
        header = next(rows, None)
    except csv.Error as err:
        raise ValueError(f"could not read the CSV: {err}") from None
    if not header:
        raise ValueError("the file is empty")
    columns = [COLUMN_ALIASES.get(c.strip().lower(), c.strip().lower()) for c in header]
    dupes = sorted({c for c in columns if c and columns.count(c) > 1})
    if dupes:
        raise ValueError("CSV has the same column twice: " + ", ".join(dupes))
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if not any(c in columns for c in TEXT_COLUMNS):
        missing.append("description (or skills)")
    if missing:
        raise ValueError("CSV is missing column(s): " + ", ".join(missing)
                         + f". Found: {', '.join(columns) or 'none'}")

    postings, problems = [], []
    try:
        for line_no, raw in enumerate(rows, start=2):
            row = {columns[i]: (v or "").strip() for i, v in enumerate(raw) if i < len(columns)}
            if not any(row.values()):
                continue
            text = " ; ".join(row.get(c, "") for c in TEXT_COLUMNS if row.get(c))
            if not row.get("title") or not text:
                problems.append(f"line {line_no}: empty title, or no description/skills")
                continue
            try:
                quarter = quarter_of(row.get("date", ""))
            except ValueError as err:
                problems.append(f"line {line_no}: {err}")
                continue
            postings.append(Posting(
                title=row["title"], description=text, date=row["date"], quarter=quarter,
                sector=row.get("sector", ""), district=row.get("district", ""), state=row.get("state", ""),
                skills=extractor.extract(row.get("description", "")) | extractor.extract(row.get("skills", ""), as_list=True),
            ))
    except csv.Error as err:
        raise ValueError(f"could not read the CSV: {err}") from None
    return postings, problems


def load_postings(path, extractor):
    with open(path, encoding="utf-8") as f:
        return parse_postings(f.read(), extractor)


def check_hours(value):
    hours = float(value)
    if not math.isfinite(hours) or hours < 0 or hours > MAX_HOURS:
        shown = str(value) if len(str(value)) <= 12 else str(value)[:12] + "…"
        raise ValueError(f"module hours must be between 0 and {MAX_HOURS}, got {shown}")
    return hours


def build_program(raw, extractor):
    modules = []
    for m in raw["modules"]:
        modules.append(Module(
            title=m["title"], hours=check_hours(m["hours"]), outline=m.get("outline", ""),
            mandatory=bool(m.get("mandatory", False)),
            skills=extractor.extract(m["title"] + " " + m.get("outline", "")),
        ))
    return Program(
        id=raw["id"], name=raw["name"], provider=raw.get("provider", ""), sector=raw.get("sector", ""),
        duration=raw.get("duration", ""), target_roles=[r.lower() for r in raw["target_roles"]],
        modules=modules, nsqf_level=str(raw.get("nsqf_level", "")), qp_code=raw.get("qp_code", ""),
    )


def load_programs(path, extractor):
    with open(path, encoding="utf-8") as f:
        return [build_program(raw, extractor) for raw in json.load(f)]


# "(40 hrs)", "- 40h", "40 Hrs.", "(1,000 hours)", "(.5 hr)" at the end of a line
HOURS_AT_END = re.compile(
    r"[\s(\-–:]*(?<![\d.,])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?|\.\d+)\s*(?:hours?|hrs?|h)\.?\s*\)?\s*\.?\s*$",
    re.IGNORECASE)
MANDATORY_MARK = re.compile(r"\s*[\[(](?:mandatory|compulsory|required)[\])]\s*", re.IGNORECASE)


def parse_syllabus_line(line):
    """'Excel basics (40 hrs) [mandatory]' -> ('Excel basics', 40.0, True)."""
    mandatory = bool(MANDATORY_MARK.search(line))
    line = MANDATORY_MARK.sub(" ", line).strip(" \t•*-")
    hours = 10.0
    match = HOURS_AT_END.search(line)
    if match:
        hours = check_hours(match.group(1).replace(",", ""))
        line = line[:match.start()].strip()
    return line, hours, mandatory


def program_from_syllabus(name, target_roles, syllabus_text, extractor, nsqf_level="", qp_code=""):
    """Turn a pasted syllabus into a Program.

    Each non-empty line is one module. A line may end with an hour count
    like "(40 hrs)"; lines without one count as 10 hours. Add "[mandatory]"
    to a line that the curriculum requires (it will never be advised to cut).
    """
    modules = []
    for line in syllabus_text.splitlines():
        if not line.strip(" \t•*-"):
            continue
        title, hours, mandatory = parse_syllabus_line(line)
        modules.append({"title": title or line.strip(), "hours": hours, "mandatory": mandatory})
    if not modules:
        raise ValueError("the syllabus is empty")
    return build_program({
        "id": "custom", "name": name or "Your program", "provider": "Pasted syllabus",
        "target_roles": target_roles, "modules": modules, "nsqf_level": nsqf_level, "qp_code": qp_code,
    }, extractor)
