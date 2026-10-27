"""A learner's view: how ready am I for a role, and which program closes my gaps."""

from .alignment import CORE_SHARE, NEVER_CUT, priority
from .demand import filter_postings, role_patterns, trend_table

STRONG_GAP = 0.25   # a course not built for the job is suggested only if it covers a gap this common


def assess_learner(have, roles, postings, programs, skills, top_programs=3, family=None):
    """Readiness for a job. `family` (an exact job family from the site's list) is
    matched exactly; otherwise `roles` are matched as whole words in titles."""
    roles = [r for r in roles if r.strip()]
    if not roles and family is None:
        raise ValueError("choose a job first")
    relevant = filter_postings(postings, family=family) if family is not None else \
        filter_postings(postings, roles=roles)
    table = trend_table(relevant)
    required = {s: t for s, t in table.items() if t["share"] >= CORE_SHARE}

    total = sum(t["share"] for t in required.values())
    matched = sum(t["share"] for s, t in required.items() if s in have)
    readiness = 100 * matched / total if total else 0.0

    missing = sorted((s for s in required if s not in have),
                     key=lambda s: priority(required[s]), reverse=True)

    def describe(skill_id):
        t = required[skill_id]
        return {"id": skill_id, "name": skills[skill_id].name, "share": t["share"],
                "growth": t["growth"], "is_new": t["is_new"], "significant": t["significant"],
                "have": skill_id in have}

    job_words = roles or [family]
    patterns = role_patterns([w for w in job_words if len(w) >= 3])
    ranked = []
    for program in programs:
        covers = [s for s in missing if s in program.skills()]
        if not covers:
            continue
        for_this_job = any(p.search(target) for target in program.target_roles for p in patterns) or \
            any(w in target or target in w for target in program.target_roles for w in job_words)
        # an unrelated course must cover a specific, common gap - not just "problem solving"
        strong = [s for s in covers if required[s]["share"] >= STRONG_GAP and skills[s].category != NEVER_CUT]
        if not for_this_job and not strong:
            continue
        ranked.append({
            "id": program.id,
            "name": program.name,
            "duration": program.duration,
            "hours": program.total_hours(),
            "covers": [skills[s].name for s in covers],
            "value": sum(priority(required[s]) for s in covers),
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
