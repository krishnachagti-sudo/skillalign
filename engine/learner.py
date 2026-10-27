"""A learner's view: how ready am I for a role, and which program closes my gaps."""

from .alignment import priority
from .demand import filter_postings, trend_table

REQUIRED_SHARE = 0.2  # a skill in a fifth of postings counts as "required"


def assess_learner(have, roles, postings, programs, skills, top_programs=3):
    relevant = filter_postings(postings, roles=roles)
    table = trend_table(relevant)
    required = {s: t for s, t in table.items() if t["share"] >= REQUIRED_SHARE}

    total = sum(t["share"] for t in required.values())
    matched = sum(t["share"] for s, t in required.items() if s in have)
    readiness = 100 * matched / total if total else 0.0

    missing = sorted((s for s in required if s not in have),
                     key=lambda s: priority(required[s]), reverse=True)

    def describe(skill_id):
        t = required[skill_id]
        return {"id": skill_id, "name": skills[skill_id].name, "share": t["share"],
                "growth": t["growth"], "have": skill_id in have}

    ranked = []
    for program in programs:
        covers = [s for s in missing if s in program.skills()]
        if not covers:
            continue
        value = sum(priority(required[s]) for s in covers)
        # a program built for this job comes before one that merely overlaps
        for_this_job = any(r in role or role in r for r in program.target_roles for role in roles)
        ranked.append({
            "id": program.id,
            "name": program.name,
            "duration": program.duration,
            "hours": program.total_hours(),
            "covers": [skills[s].name for s in covers],
            "value": value,
            "for_this_job": for_this_job,
        })
    ranked.sort(key=lambda r: (r["for_this_job"], r["value"], -r["hours"]), reverse=True)

    return {
        "postings": len(relevant),
        "readiness": round(readiness, 1),
        "required": sorted((describe(s) for s in required), key=lambda r: r["share"], reverse=True),
        "missing": [describe(s) for s in missing],
        "next_skill": describe(missing[0]) if missing else None,
        "programs": ranked[:top_programs],
        "extra": sorted(skills[s].name for s in have if s not in required and s in skills),
    }
