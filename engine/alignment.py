"""Scoring how well a training program matches the jobs it trains for.

For one program we take only the postings for its target roles, then:

- core skills: skills in at least CORE_SHARE of those postings
- alignment score: the share-weighted part of core demand the program
  teaches (teaching a skill half the postings want counts for more than
  one a fifth want)
- future score: the same, using forecast shares instead of today's
- hours on demand: how much of the training time goes to core skills
- gaps, rising gaps, low-demand and declining skills, turned into plain
  add / expand / reduce recommendations
"""

from .demand import filter_postings, trend_table

CORE_SHARE = 0.15    # in at least 15% of relevant postings
LOW_SHARE = 0.05     # in under 5% of relevant postings
FALLING = -0.2       # share down 20% or more year on year
THIN_DEMAND = 0.4    # a skill in 40%+ of postings...
THIN_HOURS = 0.05    # ...that gets under 5% of the training hours


def priority(row):
    """Demand weight for ranking gaps: share, boosted by growth."""
    growth = row["growth"] if row["growth"] is not None else 0.0
    return row["share"] * (1 + max(growth, 0.0))


def grade(score):
    if score >= 75:
        return "Strong"
    if score >= 50:
        return "Partial"
    return "Weak"


def weighted_coverage(weights, taught):
    total = sum(weights.values())
    if total == 0:
        return 0.0
    return 100 * sum(w for s, w in weights.items() if s in taught) / total


def assess_program(program, postings, skills, window=4):
    relevant = filter_postings(postings, roles=program.target_roles)
    table = trend_table(relevant, window)
    taught = program.skills()
    hours = program.hours_by_skill()
    total_hours = program.total_hours()

    core = {s: t["share"] for s, t in table.items() if t["share"] >= CORE_SHARE}
    future_core = {s: t["forecast"] for s, t in table.items() if t["forecast"] >= CORE_SHARE}

    score = weighted_coverage(core, taught)
    future_score = weighted_coverage(future_core, taught)
    hours_on_core = sum(h for s, h in hours.items() if s in core)
    hours_pct = 100 * hours_on_core / total_hours if total_hours else 0.0

    def row_for(skill_id):
        t = table.get(skill_id)
        return {
            "id": skill_id,
            "name": skills[skill_id].name if skill_id in skills else skill_id,
            "category": skills[skill_id].category if skill_id in skills else "",
            "share": t["share"] if t else 0.0,
            "growth": t["growth"] if t else None,
            "forecast": t["forecast"] if t else 0.0,
            "taught": skill_id in taught,
            "hours": round(hours.get(skill_id, 0.0), 1),
        }

    gaps = sorted((s for s in core if s not in taught), key=lambda s: priority(table[s]), reverse=True)
    rising = sorted((s for s in future_core if s not in core and s not in taught),
                    key=lambda s: table[s]["forecast"], reverse=True)
    low_value = sorted((s for s in taught if table.get(s, {"share": 0})["share"] < LOW_SHARE),
                       key=lambda s: hours.get(s, 0), reverse=True)
    declining = sorted((s for s in taught if s in table and table[s]["growth"] is not None
                        and table[s]["growth"] <= FALLING and s not in low_value),
                       key=lambda s: table[s]["growth"])
    # taught, but only touched on: a big-demand skill given a sliver of the hours
    thin = sorted((s for s in taught if s in core and core[s] >= THIN_DEMAND and total_hours
                   and hours.get(s, 0) / total_hours < THIN_HOURS and s not in declining),
                  key=lambda s: core[s], reverse=True)

    recommendations = []
    for s in gaps:
        r = row_for(s)
        recommendations.append({
            "action": "Add", "skill": r["name"], "id": s,
            "reason": f"asked for in {r['share']:.0%} of postings for these roles"
                      + (f", up {r['growth']:.0%} on last year" if r["growth"] and r["growth"] > 0 else ""),
        })
    for s in thin:
        r = row_for(s)
        recommendations.append({
            "action": "Expand", "skill": r["name"], "id": s,
            "reason": f"asked for in {r['share']:.0%} of postings but given only {r['hours']:g} of "
                      f"{total_hours:g} hours ({r['hours'] / total_hours:.0%})",
        })
    for s in rising:
        r = row_for(s)
        recommendations.append({
            "action": "Prepare", "skill": r["name"], "id": s,
            "reason": f"now {r['share']:.0%} of postings, on track for about {r['forecast']:.0%} within a year",
        })
    for s in low_value:
        r = row_for(s)
        recommendations.append({
            "action": "Reduce", "skill": r["name"], "id": s,
            "reason": f"only {r['share']:.0%} of postings ask for it, yet it takes {r['hours']:g} training hours",
        })
    for s in declining:
        r = row_for(s)
        recommendations.append({
            "action": "Review", "skill": r["name"], "id": s,
            "reason": f"still {r['share']:.0%} of postings but down {-r['growth']:.0%} on last year",
        })

    all_skills = set(core) | set(future_core) | taught
    table_rows = sorted((row_for(s) for s in all_skills), key=lambda r: r["share"], reverse=True)

    warning = ""
    if not relevant:
        warning = "No job postings match this program's target roles, so it cannot be scored."
    elif len(relevant) < 30:
        warning = f"Only {len(relevant)} matching postings; treat the score as a rough signal."

    return {
        "id": program.id,
        "name": program.name,
        "provider": program.provider,
        "sector": program.sector,
        "duration": program.duration,
        "target_roles": program.target_roles,
        "postings": len(relevant),
        "score": round(score, 1),
        "future_score": round(future_score, 1),
        "grade": grade(score),
        "hours_total": total_hours,
        "hours_on_demand_pct": round(hours_pct, 1),
        "core_count": len(core),
        "covered_count": sum(1 for s in core if s in taught),
        "skills": table_rows,
        "recommendations": recommendations,
        "modules": [{"title": m.title, "hours": m.hours,
                     "skills": sorted(skills[s].name for s in m.skills if s in skills)}
                    for m in program.modules],
        "warning": warning,
    }
