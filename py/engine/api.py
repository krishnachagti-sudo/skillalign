"""The functions the web page calls.

Every function returns a JSON string, so the JavaScript side only ever
does JSON.parse(). The loaded data lives in one State object; program
reports are cached per filter until the data changes.
"""

import json
import os

from .alignment import CORE_SHARE, assess_program
from .dataset import load_postings, load_programs, parse_postings, program_from_syllabus
from .demand import (declining_skills, emerging_skills, filter_postings, role_family, sort_quarters, split_windows,
                     trend_table)
from .learner import assess_learner
from .taxonomy import SkillExtractor, load_taxonomy


DATASETS = {
    "sample": {"file": "job_postings.csv",
               "label": "Synthetic demo data (Maharashtra, 8 quarters)"},
    "real": {"file": "real_postings_india_2026.csv",
             "label": "Real postings, India, Jan-Jun 2026 (Fliar Research, CC BY-NC 4.0)"},
}


class State:
    data_dir = "data"
    skills = {}
    extractor = None
    postings = []
    loaded = {}        # dataset name -> postings, parsed once
    programs = []
    source = "sample"
    problems = []
    cache = {}


def _json(value):
    # allow_nan=False: NaN or Infinity would make JSON.parse fail in the browser
    return json.dumps(value, separators=(",", ":"), allow_nan=False)


def init(data_dir="data"):
    State.data_dir = data_dir
    State.skills = load_taxonomy(os.path.join(data_dir, "skills.json"))
    State.extractor = SkillExtractor(State.skills)
    State.programs = load_programs(os.path.join(data_dir, "programs.json"), State.extractor)
    State.loaded = {}
    return use_dataset("sample")


def use_dataset(name):
    """Switch to a built-in dataset ('sample' or 'real'), parsing it the first time."""
    if name not in DATASETS:
        raise ValueError(f"unknown dataset '{name}'")
    if name not in State.loaded:
        path = os.path.join(State.data_dir, DATASETS[name]["file"])
        if not os.path.exists(path):
            raise ValueError(f"the {name} dataset is not available")
        State.loaded[name] = load_postings(path, State.extractor)
    postings, problems = State.loaded[name]
    _use(postings, problems, name)
    return meta()


def _use(postings, problems, source):
    State.postings, State.problems, State.source = postings, problems, source
    State.cache = {}


def _meta_dict(postings, problems, source):
    quarters = sort_quarters(p.quarter for p in postings)
    families = {}
    for p in postings:
        fam = p.family or role_family(p.title)
        if len(fam) >= 3:
            families[fam] = families.get(fam, 0) + 1
    return {
        "source": source,
        "source_label": DATASETS[source]["label"] if source in DATASETS else "Your uploaded file",
        "datasets": {k: v["label"] for k, v in DATASETS.items()},
        "postings": len(postings),
        "quarters": quarters,
        "sectors": sorted({p.sector for p in postings if p.sector}),
        "districts": sorted({p.district for p in postings if p.district}),
        "states": sorted({p.state for p in postings if p.state}),
        # jobs a learner can pick: families with enough postings to say anything, largest first
        "roles": sorted(((f, n) for f, n in families.items() if n >= 5), key=lambda r: -r[1])[:400],
        "skills": [{"id": s.id, "name": s.name, "category": s.category} for s in State.skills.values()],
        "synonyms": sum(len(s.synonyms) for s in State.skills.values()),
        "programs": [{"id": p.id, "name": p.name} for p in State.programs],
        "problems": problems[:20],
        "problem_count": len(problems),
    }


def meta():
    return _json(_meta_dict(State.postings, State.problems, State.source))


def _reports(sector="", district="", state=""):
    key = (sector, district, state)
    if key not in State.cache:
        selected = filter_postings(State.postings, sector=sector or None, district=district or None, state=state or None)
        State.cache[key] = {p.id: assess_program(p, selected, State.skills) for p in State.programs}
    return State.cache[key]


def _skill_row(skill_id, t):
    s = State.skills[skill_id]
    return {"id": skill_id, "name": s.name, "category": s.category, "share": t["share"], "low": t["low"],
            "high": t["high"], "growth": t["growth"], "is_new": t["is_new"], "significant": t["significant"],
            "within_growth": t["within_growth"], "forecast": t["forecast"], "forecast_ok": t["forecast_ok"],
            "postings": t["count"], "n": t["n"], "series": t["series"]}


def overview(sector="", district="", state=""):
    selected = filter_postings(State.postings, sector=sector or None, district=district or None, state=state or None)
    table = trend_table(selected)
    top = sorted(table.items(), key=lambda kv: kv[1]["share"], reverse=True)
    scored = [r for r in _reports(sector, district, state).values() if r["scored"]]
    recent_n = next(iter(table.values()))["n"] if table else 0
    recent_q, previous_q = split_windows(selected)
    return _json({
        "has_previous": bool(previous_q),
        "quarters_present": len(recent_q) + len(previous_q),
        "postings": len(selected),
        "recent_postings": recent_n,
        "skills_seen": len(table),
        "top": [_skill_row(s, t) for s, t in top[:15]],
        "emerging": [_skill_row(s, t) for s, t in emerging_skills(table)[:10]],
        "declining": [_skill_row(s, t) for s, t in declining_skills(table)[:8]],
        "avg_alignment": round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None,
        "programs_strong": sum(1 for r in scored if r["grade"] == "Strong"),
        "programs_total": len(scored),
    })


SUMMARY_KEYS = ("id", "name", "provider", "sector", "duration", "postings", "scored", "score", "score_low",
                "score_high", "future_score", "forecast_ok", "grade", "low_data", "hours_on_demand_pct", "unmatched_pct",
                "core_count", "covered_count", "warning")


def programs_summary(sector="", district="", state=""):
    rows = [{k: r[k] for k in SUMMARY_KEYS} for r in _reports(sector, district, state).values()]
    rows.sort(key=lambda r: (not r["scored"], r["score"]))  # weakest first, unscored last
    return _json(rows)


def program_report(program_id, sector="", district="", state=""):
    reports = _reports(sector, district, state)
    if program_id not in reports:
        raise KeyError(f"no program with id '{program_id}'")
    return _json(reports[program_id])


def matrix(sector="", district="", state="", per_program=3, limit=24):
    """Programs x skills that matter to them: each program contributes its
    own most-demanded core skills, so a healthcare course is judged on
    healthcare skills, not on whatever IT jobs ask for most."""
    reports = _reports(sector, district, state)
    columns = []
    for r in reports.values():
        for s in [x for x in r["skills"] if x["share"] >= CORE_SHARE][:per_program]:
            if s["id"] not in columns:
                columns.append(s["id"])
    columns = columns[:limit]
    rows = []
    for p in State.programs:
        shares = {x["id"]: x["share"] for x in reports[p.id]["skills"]}
        taught = p.skills()
        rows.append({"id": p.id, "name": p.name, "scored": reports[p.id]["scored"], "cells": [
            {"taught": s in taught, "share": shares.get(s, 0.0)} for s in columns]})
    return _json({"skills": [{"id": s, "name": State.skills[s].name} for s in columns], "rows": rows})


def extract(text):
    found = State.extractor.extract_with_evidence(text)
    return _json({
        "skills": [{"id": s, "name": State.skills[s].name, "category": State.skills[s].category, "matched": phrases}
                   for s, phrases in sorted(found.items(), key=lambda kv: State.skills[kv[0]].name)],
        "unrecognised": State.extractor.unrecognised(text)[:30],
    })


def learner(role, skill_ids_json="[]", free_text=""):
    try:
        ids = json.loads(skill_ids_json or "[]")
    except json.JSONDecodeError:
        ids = []
    have = {s for s in ids if s in State.skills} | State.extractor.extract(free_text)
    role = " ".join(role.lower().split())
    known = any(p.family == role for p in State.postings)
    report = assess_learner(have, [] if known else [role], State.postings, State.programs, State.skills,
                            family=role if known else None)
    report["have"] = sorted(State.skills[s].name for s in have)
    report["unrecognised"] = State.extractor.unrecognised(free_text)[:30]
    return _json(report)


def analyse_syllabus(name, roles_text, syllabus_text, nsqf_level="", qp_code=""):
    roles = [r.strip().lower() for r in roles_text.split(",") if r.strip()]
    if not roles:
        raise ValueError("enter at least one target role")
    program = program_from_syllabus(name, roles, syllabus_text, State.extractor, nsqf_level, qp_code)
    return _json(assess_program(program, State.postings, State.skills))


def load_uploaded(csv_text):
    postings, problems = parse_postings(csv_text, State.extractor)
    if not postings:
        raise ValueError("no usable rows found" + (": " + problems[0] if problems else ""))
    result = _meta_dict(postings, problems, "uploaded")  # build first: a failure leaves the old data in place
    _use(postings, problems, "uploaded")
    return _json(result)


def use_sample():
    return use_dataset("sample")
