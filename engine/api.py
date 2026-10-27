"""The functions the web page calls.

Every function returns a JSON string, so the JavaScript side only ever
does JSON.parse(). The loaded data lives in one State object.
"""

import json
import os
import re

from .alignment import assess_program
from .dataset import load_postings, load_programs, parse_postings, program_from_syllabus
from .demand import declining_skills, emerging_skills, filter_postings, sort_quarters, trend_table
from .learner import assess_learner
from .taxonomy import SkillExtractor, load_taxonomy

SENIORITY = re.compile(r"\b(junior|senior|sr\.?|jr\.?|trainee|fresher|apprentice|lead)\b|\(.*?\)", re.IGNORECASE)


class State:
    skills = {}
    extractor = None
    postings = []
    sample_postings = []
    programs = []
    source = "sample"
    problems = []


def _json(value):
    return json.dumps(value, separators=(",", ":"))


def role_family(title):
    """'Junior Data Analyst (Fresher)' -> 'data analyst'."""
    cleaned = SENIORITY.sub(" ", title.lower())
    cleaned = re.split(r"\s[-|–]\s", cleaned)[0]
    return " ".join(cleaned.split())


def init(data_dir="data"):
    State.skills = load_taxonomy(os.path.join(data_dir, "skills.json"))
    State.extractor = SkillExtractor(State.skills)
    State.sample_postings, State.problems = load_postings(os.path.join(data_dir, "job_postings.csv"), State.extractor)
    State.postings = State.sample_postings
    State.programs = load_programs(os.path.join(data_dir, "programs.json"), State.extractor)
    State.source = "sample"
    return meta()


def meta():
    quarters = sort_quarters(p.quarter for p in State.postings)
    families = {}
    for p in State.postings:
        fam = role_family(p.title)
        families[fam] = families.get(fam, 0) + 1
    return _json({
        "source": State.source,
        "postings": len(State.postings),
        "quarters": quarters,
        "sectors": sorted({p.sector for p in State.postings if p.sector}),
        "cities": sorted({p.city for p in State.postings if p.city}),
        "roles": sorted(((f, n) for f, n in families.items() if n >= 3), key=lambda r: -r[1]),
        "skills": [{"id": s.id, "name": s.name, "category": s.category} for s in State.skills.values()],
        "programs": [{"id": p.id, "name": p.name} for p in State.programs],
        "problems": State.problems[:20],
        "problem_count": len(State.problems),
    })


def _skill_row(skill_id, t):
    s = State.skills[skill_id]
    return {"id": skill_id, "name": s.name, "category": s.category, "share": t["share"],
            "growth": t["growth"], "forecast": t["forecast"], "postings": t["postings"],
            "series": t["series"]}


def overview(sector="", city=""):
    selected = filter_postings(State.postings, sector=sector or None, city=city or None)
    table = trend_table(selected)
    top = sorted(table.items(), key=lambda kv: kv[1]["share"], reverse=True)
    reports = [assess_program(p, State.postings, State.skills) for p in State.programs]
    scored = [r for r in reports if r["postings"]]
    return _json({
        "postings": len(selected),
        "skills_seen": len(table),
        "top": [_skill_row(s, t) for s, t in top[:15]],
        "emerging": [_skill_row(s, t) for s, t in emerging_skills(table)[:10]],
        "declining": [_skill_row(s, t) for s, t in declining_skills(table)[:8]],
        "avg_alignment": round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None,
        "programs_weak": sum(1 for r in scored if r["grade"] == "Weak"),
        "programs_total": len(scored),
    })


def programs_summary():
    rows = []
    for p in State.programs:
        r = assess_program(p, State.postings, State.skills)
        rows.append({k: r[k] for k in ("id", "name", "provider", "sector", "duration", "postings",
                                       "score", "future_score", "grade", "hours_on_demand_pct",
                                       "core_count", "covered_count", "warning")})
    rows.sort(key=lambda r: r["score"])
    return _json(rows)


def program_report(program_id):
    for p in State.programs:
        if p.id == program_id:
            return _json(assess_program(p, State.postings, State.skills))
    raise KeyError(program_id)


def matrix(limit=18):
    """Programs x most-demanded skills: is each skill taught?"""
    table = trend_table(State.postings)
    top = [s for s, _ in sorted(table.items(), key=lambda kv: kv[1]["share"], reverse=True)[:limit]]
    rows = []
    for p in State.programs:
        relevant = filter_postings(State.postings, roles=p.target_roles)
        local = trend_table(relevant)
        taught = p.skills()
        rows.append({"id": p.id, "name": p.name, "cells": [
            {"taught": s in taught, "share": local.get(s, {"share": 0.0})["share"]} for s in top]})
    return _json({"skills": [{"id": s, "name": State.skills[s].name} for s in top], "rows": rows})


def extract(text):
    found = State.extractor.extract_with_evidence(text)
    return _json([{"id": s, "name": State.skills[s].name, "category": State.skills[s].category,
                   "matched": phrases} for s, phrases in sorted(found.items(), key=lambda kv: State.skills[kv[0]].name)])


def learner(role, skill_ids_json="[]", free_text=""):
    have = set(json.loads(skill_ids_json)) | State.extractor.extract(free_text)
    report = assess_learner(have, [role.lower()], State.postings, State.programs, State.skills)
    report["have"] = sorted(State.skills[s].name for s in have if s in State.skills)
    return _json(report)


def analyse_syllabus(name, roles_text, syllabus_text):
    roles = [r.strip().lower() for r in roles_text.split(",") if r.strip()]
    if not roles:
        raise ValueError("enter at least one target role")
    program = program_from_syllabus(name, roles, syllabus_text, State.extractor)
    return _json(assess_program(program, State.postings, State.skills))


def load_uploaded(csv_text):
    postings, problems = parse_postings(csv_text, State.extractor)
    if not postings:
        raise ValueError("no usable rows found" + (": " + problems[0] if problems else ""))
    State.postings = postings
    State.problems = problems
    State.source = "uploaded"
    return meta()


def use_sample():
    State.postings = State.sample_postings
    State.problems = []
    State.source = "sample"
    return meta()
