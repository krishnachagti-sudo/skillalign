"""Scoring how well a training program matches the jobs it trains for.

For one program we take only the postings for its target roles, then:

- core skills: skills in at least CORE_SHARE of those postings
- depth credit: a core skill counts fully only if the program gives it
  at least half the hours its demand would justify. Its "fair" hours are
  total hours x its share of all core demand. So a one-hour
  "Introduction to X" earns almost nothing, and padding a course with
  unrelated hours lowers every skill's credit.
- alignment score = sum(share x credit) / sum(share) over core skills,
  with a 90% bootstrap interval from resampling the postings
- future score: the same, using forecast shares
- recommendations (Add / Expand / Prepare / Reduce / Review), where the
  trend-based ones need a statistically significant change and nothing
  taught only in a compulsory module is ever advised to cut
"""

import random

from .demand import filter_postings, is_falling, is_rising, split_windows, trend_table

CORE_SHARE = 0.15     # in at least 15% of relevant postings
LOW_SHARE = 0.05      # in under 5% of relevant postings
DEPTH = 0.5           # full credit at half the demand-proportional hours
EXPAND_BELOW = 0.75   # advise "Expand" only when a taught skill earns under 75% credit
MIN_POSTINGS = 30     # below this a score is flagged as low-data
BOOTSTRAP = 150       # resamples for the score interval


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


def depth_credits(weights, hours, total_hours):
    """{skill: credit in [0, 1]} for the skills in `weights` (skill -> share)."""
    demand = sum(weights.values())
    credits = {}
    for s, w in weights.items():
        h = hours.get(s, 0.0)
        if h <= 0:
            credits[s] = 0.0
        elif total_hours <= 0 or demand <= 0 or w <= 0:
            credits[s] = 1.0
        else:
            fair = total_hours * w / demand
            credits[s] = min(1.0, h / (DEPTH * fair))
    return credits


def weighted_score(weights, hours, total_hours):
    total = sum(weights.values())
    if total == 0:
        return 0.0
    credits = depth_credits(weights, hours, total_hours)
    return 100 * sum(w * credits[s] for s, w in weights.items()) / total


def bootstrap_interval(relevant, core, hours, total_hours, seed=12345):
    """90% interval for the score by resampling the recent-window postings
    (the same postings the score itself is computed from) with replacement."""
    if len(relevant) < 2 or not core:
        return None
    rng = random.Random(seed)
    present = [[s for s in p.skills if s in core] for p in relevant]
    n = len(present)
    scores = []
    for _ in range(BOOTSTRAP):
        counts = dict.fromkeys(core, 0)
        for _ in range(n):
            for s in present[rng.randrange(n)]:
                counts[s] += 1
        weights = {s: c / n for s, c in counts.items()}
        scores.append(weighted_score(weights, hours, total_hours))
    scores.sort()
    return scores[int(0.05 * (BOOTSTRAP - 1))], scores[int(0.95 * (BOOTSTRAP - 1))]


def pct(x):
    return f"{x:.0%}"


def assess_program(program, postings, skills, window=4):
    relevant = filter_postings(postings, roles=program.target_roles)
    table = trend_table(relevant, window)
    taught = program.skills()
    protected = program.mandatory_skills()
    hours = program.hours_by_skill()
    total_hours = program.total_hours()

    core = {s: t["share"] for s, t in table.items() if t["share"] >= CORE_SHARE}
    future_core = {s: t["forecast"] for s, t in table.items() if t["forecast"] >= CORE_SHARE}
    credits = depth_credits(core, hours, total_hours)
    demand = sum(core.values())

    score = weighted_score(core, hours, total_hours)
    future_score = weighted_score(future_core, hours, total_hours)
    recent_q, _ = split_windows(relevant, window)
    interval = bootstrap_interval([p for p in relevant if p.quarter in recent_q], set(core), hours, total_hours)
    hours_on_core = sum(h for s, h in hours.items() if s in core)
    hours_pct = 100 * hours_on_core / total_hours if total_hours else 0.0
    unmatched = program.unmatched_hours()

    def name(s):
        return skills[s].name if s in skills else s

    def row_for(s):
        t = table.get(s)
        fair = total_hours * core[s] / demand if s in core and demand else 0.0
        return {
            "id": s, "name": name(s), "category": skills[s].category if s in skills else "",
            "share": t["share"] if t else 0.0, "low": t["low"] if t else 0.0, "high": t["high"] if t else 0.0,
            "growth": t["growth"] if t else None, "is_new": t["is_new"] if t else False,
            "significant": t["significant"] if t else False,
            "forecast": t["forecast"] if t else 0.0,
            "taught": s in taught, "mandatory": s in protected,
            "hours": round(hours.get(s, 0.0), 1),
            "credit": round(credits[s], 2) if s in credits else None,
            "fair_hours": round(DEPTH * fair) if fair else None,
        }

    def trend_words(t):
        if t["is_new"]:
            return ", new this year"
        if t["growth"] is not None and t["significant"] and t["growth"] > 0:
            return f", up {pct(t['growth'])} on last year"
        return ""

    recommendations = []
    if relevant:
        for s in sorted((s for s in core if s not in taught), key=lambda s: priority(table[s]), reverse=True):
            t = table[s]
            recommendations.append({"action": "Add", "skill": name(s), "id": s, "reason":
                f"asked for in {pct(t['share'])} of postings for these roles (95% range "
                f"{pct(t['low'])}-{pct(t['high'])}){trend_words(t)}"})
        for s in sorted((s for s in core if s in taught and credits[s] < EXPAND_BELOW), key=lambda s: credits[s]):
            r = row_for(s)
            recommendations.append({"action": "Expand", "skill": r["name"], "id": s, "reason":
                f"asked for in {pct(r['share'])} of postings but given {r['hours']:g} h; about "
                f"{round(r['fair_hours'])} h would earn full credit"})
        for s in sorted((s for s in future_core if s not in core and s not in taught and is_rising(table[s])),
                        key=lambda s: table[s]["forecast"], reverse=True):
            t = table[s]
            recommendations.append({"action": "Prepare", "skill": name(s), "id": s, "reason":
                f"now {pct(t['share'])} of postings and rising beyond chance; forecast about "
                f"{pct(t['forecast'])} within a year"})
        for s in sorted((s for s in taught if s not in protected and hours.get(s, 0) > 0
                         and table.get(s, {"high": 0})["high"] < CORE_SHARE
                         and table.get(s, {"share": 0})["share"] < LOW_SHARE),
                        key=lambda s: hours.get(s, 0), reverse=True):
            r = row_for(s)
            recommendations.append({"action": "Reduce", "skill": r["name"], "id": s, "reason":
                f"only {pct(r['share'])} of postings ask for it, yet it takes {r['hours']:g} training hours"})
        for s in sorted((s for s in taught if s in table and s not in protected and is_falling(table[s])),
                        key=lambda s: table[s]["growth"]):
            t = table[s]
            recommendations.append({"action": "Review", "skill": name(s), "id": s, "reason":
                f"still {pct(t['share'])} of postings but down {pct(-t['growth'])} on last year, "
                f"beyond chance and within the same roles"})

    warnings = []
    if not relevant:
        warnings.append("No job postings match this program's target roles, so it cannot be scored.")
    elif len(relevant) < MIN_POSTINGS:
        warnings.append(f"Only {len(relevant)} matching postings: treat the score as a rough signal.")
    if total_hours and unmatched / total_hours >= 0.2:
        missed = [m.title for m in program.modules if not m.skills]
        warnings.append(f"{pct(unmatched / total_hours)} of training hours ({len(missed)} module"
                        f"{'s' if len(missed) != 1 else ''}) matched no skill SkillAlign knows, so the "
                        f"score cannot see them: {', '.join(missed[:4])}{'…' if len(missed) > 4 else ''}.")
    forecast_ok = bool(table) and next(iter(table.values()))["forecast_ok"]

    all_skills = set(core) | set(future_core) | taught
    return {
        "id": program.id, "name": program.name, "provider": program.provider, "sector": program.sector,
        "duration": program.duration, "target_roles": program.target_roles,
        "nsqf_level": program.nsqf_level, "qp_code": program.qp_code,
        "postings": len(relevant),
        "scored": bool(relevant),
        "score": round(score, 1),
        "score_low": round(interval[0], 1) if interval else None,
        "score_high": round(interval[1], 1) if interval else None,
        "future_score": round(future_score, 1) if forecast_ok else None,
        "forecast_ok": forecast_ok,
        "grade": grade(score) if relevant else "Unscored",
        "low_data": 0 < len(relevant) < MIN_POSTINGS,
        "hours_total": total_hours,
        "hours_on_demand_pct": round(hours_pct, 1),
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
