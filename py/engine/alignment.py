"""Scoring how well a training program matches the jobs it trains for.

For one program we take the postings for its target roles (entry-level
jobs only, for an entry-level course), then:

- if there are fewer than MIN_POSTINGS, the course is NOT scored and gets
  no advice: a handful of postings cannot say what a trade needs;
- core skills: skills in at least CORE_SHARE of those postings;
- depth credit: a core skill counts fully only when the course gives it
  enough hours. "Enough" is absolute, not relative to the course's length:
  half of what a REF_HOURS-hour reference course would give it in
  proportion to its demand, and never less than MIN_HOURS. So a one-hour
  "Introduction to X" earns little, shrinking a course earns less, padding
  it with unrelated hours neither helps nor hurts, and adding hours to a
  core skill can only raise the score;
- alignment score = sum(share x credit) / sum(share) over core skills;
- a 90% range from resampling EMPLOYERS (a company's postings move
  together) with replacement, re-picking the core skills every time;
- recommendations (Add / Expand / Prepare / Reduce / Review). Trend-based
  ones need a significant role-adjusted change. Nothing taught in a
  compulsory module, and no core/soft skill, is ever advised to cut:
  job ads under-report basics like communication or computer use.
"""

import random

from .demand import filter_postings, is_falling, is_rising, split_windows, trend_table, wilson

CORE_SHARE = 0.15     # in at least 15% of relevant postings
LOW_SHARE = 0.05      # under 5% of relevant postings (and confidently under 15%) -> Reduce
MIN_POSTINGS = 30     # below this a course is not scored
DEPTH = 0.5           # full credit at half the hours a reference course would give
REF_HOURS = 200       # the reference course length
MIN_HOURS = 5         # no core skill is "taught" in less than this
BOOTSTRAP = 400       # resamples for the score range
NEVER_CUT = "Core & Soft Skills"


def priority(row):
    """Demand weight for ranking gaps: share, boosted by growth."""
    growth = row["growth"] if row["growth"] is not None else (1.0 if row.get("is_new") else 0.0)
    return row["share"] * (1 + max(growth, 0.0))


def grade(score):
    if score >= 75:
        return "Strong"
    if score >= 50:
        return "Partial"
    return "Weak"


def hours_needed(weights):
    """{skill: hours for full credit}, from each core skill's share of demand."""
    demand = sum(weights.values())
    if demand <= 0:
        return {}
    return {s: max(MIN_HOURS, DEPTH * REF_HOURS * w / demand) for s, w in weights.items()}


def depth_credits(weights, hours):
    needed = hours_needed(weights)
    return {s: min(1.0, hours.get(s, 0.0) / needed[s]) for s in weights}


def weighted_score(weights, hours):
    total = sum(weights.values())
    if total == 0:
        return 0.0
    credits = depth_credits(weights, hours)
    return 100 * sum(w * credits[s] for s, w in weights.items()) / total


def bootstrap_interval(postings, hours, seed=12345):
    """90% range for the score: resample employers with replacement (a posting
    with no employer is its own group) and re-pick the core skills each time."""
    groups = {}
    for i, p in enumerate(postings):
        groups.setdefault(p.employer or f"#{i}", []).append(p.skills)
    clusters = list(groups.values())
    if len(clusters) < 2:
        return None
    rng = random.Random(seed)
    scores = []
    for _ in range(BOOTSTRAP):
        counts, n = {}, 0
        for _ in range(len(clusters)):
            cluster = clusters[rng.randrange(len(clusters))]
            n += len(cluster)
            for skills in cluster:
                for s in skills:
                    counts[s] = counts.get(s, 0) + 1
        core = {s: c / n for s, c in counts.items() if c / n >= CORE_SHARE}
        scores.append(weighted_score(core, hours))
    scores.sort()
    return scores[int(0.05 * (BOOTSTRAP - 1))], scores[int(0.95 * (BOOTSTRAP - 1))]


def pct(x):
    return f"{x:.0%}"


def assess_program(program, postings, skills, window=4):
    relevant = filter_postings(postings, roles=program.target_roles, entry_only=program.entry_level)
    scored = len(relevant) >= MIN_POSTINGS
    table = trend_table(relevant, window)
    n_recent = next(iter(table.values()))["n"] if table else 0
    taught = program.skills()
    protected = program.mandatory_skills() | {s for s in taught if s in skills and skills[s].category == NEVER_CUT}
    hours = program.hours_by_skill()
    total_hours = program.total_hours()

    core = {s: t["share"] for s, t in table.items() if t["share"] >= CORE_SHARE}
    future_core = {s: t["forecast"] for s, t in table.items() if t["forecast"] >= CORE_SHARE}
    credits = depth_credits(core, hours)
    needed = hours_needed(core)
    forecast_ok = bool(table) and next(iter(table.values()))["forecast_ok"]

    score = weighted_score(core, hours) if scored else 0.0
    future_score = weighted_score(future_core, hours) if scored and forecast_ok else None
    recent_q, _ = split_windows(relevant, window)
    interval = bootstrap_interval([p for p in relevant if p.quarter in recent_q], hours) if scored else None
    hours_on_core = sum(h for s, h in hours.items() if s in core)
    unmatched = program.unmatched_hours()

    def name(s):
        return skills[s].name if s in skills else s

    def stats(s):
        """A skill's row in the table, or what 0 of n postings means."""
        if s in table:
            return table[s]
        low, high = wilson(0, n_recent)
        return {"share": 0.0, "low": low, "high": high, "growth": None, "is_new": False,
                "significant": False, "forecast": 0.0}

    def row_for(s):
        t = stats(s)
        return {
            "id": s, "name": name(s), "category": skills[s].category if s in skills else "",
            "share": t["share"], "low": t["low"], "high": t["high"],
            "growth": t["growth"], "is_new": t["is_new"], "significant": t["significant"],
            "forecast": t["forecast"],
            "taught": s in taught, "mandatory": s in protected,
            "hours": round(hours.get(s, 0.0), 1),
            "credit": round(credits[s], 2) if s in credits else None,
            "fair_hours": round(needed[s]) if s in needed else None,
        }

    def trend_words(t):
        if t["is_new"] and t["significant"]:
            return ", new this year"
        if t["growth"] is not None and t["significant"] and t["growth"] > 0:
            return f", up {pct(t['growth'])} on last year"
        return ""

    recommendations = []
    if scored:
        for s in sorted((s for s in core if s not in taught), key=lambda s: priority(table[s]), reverse=True):
            t = table[s]
            recommendations.append({"action": "Add", "skill": name(s), "id": s, "reason":
                f"asked for in {pct(t['share'])} of postings for these roles (95% range "
                f"{pct(t['low'])}-{pct(t['high'])}){trend_words(t)}"})
        for s in sorted((s for s in core if s in taught and credits[s] < 1), key=lambda s: credits[s]):
            r = row_for(s)
            recommendations.append({"action": "Expand", "skill": r["name"], "id": s, "reason":
                f"asked for in {pct(r['share'])} of postings but given {r['hours']:g} h; "
                f"{r['fair_hours']} h would earn full credit"})
        for s in sorted((s for s in future_core if s not in core and s not in taught and is_rising(table[s])),
                        key=lambda s: table[s]["forecast"], reverse=True):
            t = table[s]
            recommendations.append({"action": "Prepare", "skill": name(s), "id": s, "reason":
                f"now {pct(t['share'])} of postings and rising beyond chance; forecast about "
                f"{pct(t['forecast'])} ({pct(t['forecast_low'])}-{pct(t['forecast_high'])}) within a year"})
        for s in sorted((s for s in taught if s not in protected and hours.get(s, 0) > 0
                         and stats(s)["share"] < LOW_SHARE and stats(s)["high"] < CORE_SHARE),
                        key=lambda s: hours.get(s, 0), reverse=True):
            r = row_for(s)
            recommendations.append({"action": "Reduce", "skill": r["name"], "id": s, "reason":
                f"only {pct(r['share'])} of postings ask for it (at most {pct(r['high'])}), "
                f"yet it takes {r['hours']:g} training hours"})
        for s in sorted((s for s in taught if s in table and s not in protected and is_falling(table[s])),
                        key=lambda s: table[s]["growth"]):
            t = table[s]
            recommendations.append({"action": "Review", "skill": name(s), "id": s, "reason":
                f"still {pct(t['share'])} of postings but down {pct(-t['growth'])} on last year, "
                f"beyond chance and within the same roles"})

    warnings = []
    if not relevant:
        warnings.append("No job postings match this program's target roles, so it cannot be scored.")
    elif not scored:
        warnings.append(f"Only {len(relevant)} matching postings (at least {MIN_POSTINGS} needed), so it is not "
                        f"scored and gets no advice.")
    if total_hours and unmatched / total_hours >= 0.2:
        missed = [m.title for m in program.modules if not m.skills]
        warnings.append(f"{pct(unmatched / total_hours)} of training hours ({len(missed)} module"
                        f"{'s' if len(missed) != 1 else ''}) matched no skill SkillAlign knows, so the "
                        f"score cannot see them: {', '.join(missed[:4])}{'…' if len(missed) > 4 else ''}.")

    all_skills = (set(core) | set(future_core) | taught) if relevant else taught
    return {
        "id": program.id, "name": program.name, "provider": program.provider, "sector": program.sector,
        "duration": program.duration, "target_roles": program.target_roles,
        "nsqf_level": program.nsqf_level, "qp_code": program.qp_code,
        "postings": len(relevant),
        "scored": scored,
        "score": round(score, 1),
        "score_low": round(interval[0], 1) if interval else None,
        "score_high": round(interval[1], 1) if interval else None,
        "future_score": round(future_score, 1) if future_score is not None else None,
        "forecast_ok": forecast_ok,
        "grade": grade(score) if scored else ("Unscored" if not relevant else "Too few postings"),
        "low_data": 0 < len(relevant) < MIN_POSTINGS,
        "hours_total": total_hours,
        "hours_on_demand_pct": round(100 * hours_on_core / total_hours, 1) if total_hours else 0.0,
        "unmatched_pct": round(100 * unmatched / total_hours, 1) if total_hours else 0.0,
        "core_count": len(core),
        "covered_count": sum(1 for s in core if s in taught),
        "skills": sorted((row_for(s) for s in all_skills), key=lambda r: r["share"], reverse=True),
        "recommendations": recommendations,
        "modules": [{"title": m.title, "hours": m.hours, "mandatory": m.mandatory,
                     "skills": sorted(name(s) for s in m.skills)} for m in program.modules],
        "warnings": warnings,
        "warning": " ".join(warnings),
    }
