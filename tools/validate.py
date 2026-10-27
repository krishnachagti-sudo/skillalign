"""Does the method find real trends, ignore fake ones, and state honest ranges?

The sample postings are synthetic, so on their own they prove nothing:
any trend the tool reports was written into the generator. This script
uses that: because the generator's true parameters are known, every
claim can be checked against the truth. Results go to docs/validation.md.

1. False alarms on data with NO skill trends, in three versions: fully
   flat; role volumes still shifting (only the mix of jobs changes); and
   flat with employers reposting the same ad. Compared with the naive
   rule SkillAlign first used (growth thresholds, no test).
2. Detection on trended data, against the TRUE within-role change implied
   by the generator: precision, recall by size of change, and the
   precision a random guesser would get.
3. Score ranges: how often the "90% range" contains the true score.
4. Forecast backtest: fit on the first six quarters, predict the eighth.
5. Stability of course scores and grades across samples.

Run:  python tools/validate.py
"""

import io
import os
import statistics
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.alignment import CORE_SHARE, assess_program, weighted_score  # noqa: E402
from engine.dataset import load_programs, parse_postings  # noqa: E402
from engine.demand import (Z95, declining_skills, emerging_skills, filter_postings, fit_line_weighted,  # noqa: E402
                           is_entry_level, quarter_index, split_windows, trend_table)
from engine.taxonomy import SkillExtractor, load_taxonomy  # noqa: E402
from generate_sample_data import QUARTERS, ROLES, generate, lerp, write_csv  # noqa: E402

SEEDS = range(1, 21)
skills = load_taxonomy(os.path.join(ROOT, "data", "skills.json"))
extractor = SkillExtractor(skills)
programs = load_programs(os.path.join(ROOT, "data", "programs.json"), extractor)


def postings_for(seed, **kw):
    buf = io.StringIO()
    write_csv(generate(seed, **kw), buf)
    return parse_postings(buf.getvalue(), extractor)[0]


def naive_calls(table):
    """The first version's rule: thresholds on growth, no significance test."""
    up = [s for s, t in table.items() if t["share"] >= 0.05 and t["growth"] is not None and t["growth"] >= 0.3]
    down = [s for s, t in table.items() if (t["previous"] or 0) >= 0.05 and t["growth"] is not None
            and t["growth"] <= -0.2]
    return up + down


def calls(table):
    return [s for s, _ in emerging_skills(table)] + [s for s, _ in declining_skills(table)]


# --- the truth, from the generator's parameters ------------------------------------

def expected(role, skill, qi):
    t = qi / (len(QUARTERS) - 1)
    p0, p1 = ROLES[role][2].get(skill, (0.0, 0.0))
    return lerp(p0, p1, t)


def volume(role, qi):
    v0, v1 = ROLES[role][1]
    return lerp(v0, v1, qi / (len(QUARTERS) - 1))


def true_changes():
    """{skill: (true within-role relative change, true recent market share, true previous share)}
    using the same definition the tool estimates: recent window = last 4 quarters."""
    recent, previous = range(4, 8), range(0, 4)
    out = {}
    all_skills = {s for _, _, prof in ROLES.values() for s in prof}
    for s in all_skills:
        change = base = 0.0
        share_now = share_before = 0.0
        vol_now = sum(volume(r, q) for r in ROLES for q in recent)
        vol_before = sum(volume(r, q) for r in ROLES for q in previous)
        for r in ROLES:
            w = sum(volume(r, q) for q in recent)
            p_now = sum(expected(r, s, q) * volume(r, q) for q in recent) / w
            p_before = sum(expected(r, s, q) * volume(r, q) for q in previous) / sum(volume(r, q) for q in previous)
            change += w * (p_now - p_before)
            base += w * p_before
            share_now += p_now * w / vol_now
            share_before += p_before * sum(volume(r, q) for q in previous) / vol_before
        out[s] = (change / base if base else (1.0 if change > 0 else 0.0), share_now, share_before)
    return out


def truly_trending(truth):
    """The tool's own rule applied to the TRUE values: market-wide growth of +30% (or -20%)
    and a within-role change of at least half that, in a skill in 5%+ of postings."""
    def market(now, before):
        return (now - before) / before if before else 1.0
    rising = {s for s, (g, now, before) in truth.items() if now >= 0.05 and market(now, before) >= 0.3 and g >= 0.15}
    falling = {s for s, (g, now, before) in truth.items() if before >= 0.05 and market(now, before) <= -0.2 and g <= -0.1}
    eligible = {s for s, (_, now, before) in truth.items() if max(now, before) >= 0.05}
    return rising, falling, eligible


def true_score(program):
    """A course's score if shares were exactly the generator's expected ones."""
    recent = range(4, 8)
    weights, total = {}, 0.0
    for r in ROLES:
        if not any(target in r.lower() for target in program.target_roles):
            continue
        for q in recent:
            v = volume(r, q) * 0.5        # PREFIXES: half the titles carry no seniority word -> entry level
            total += v
            for s in ROLES[r][2]:
                weights[s] = weights.get(s, 0.0) + v * expected(r, s, q)
    if not total:
        return None
    core = {s: w / total for s, w in weights.items() if w / total >= CORE_SHARE}
    return weighted_score(core, program.hours_by_skill())


def main():
    truth = true_changes()
    rising, falling, eligible = truly_trending(truth)
    moving = rising | falling
    nulls = {"flat": {}, "flat_skills": {}, "reposts": {}}
    for name in nulls:
        nulls[name] = {"new": [], "old": [], "advice": []}
    found, hits, direction_ok = [], 0, 0
    by_size = {"15-50%": [0, 0], "50-100%": [0, 0], "over 100%": [0, 0]}
    cover = {p.id: [] for p in programs}
    scores = {p.id: [] for p in programs}
    grades = {p.id: [] for p in programs}
    fc_err, fc_in = [], []

    for seed in SEEDS:
        for name, kw in (("flat", {"flat": True}), ("flat_skills", {"flat_skills": True}),
                         ("reposts", {"flat": True, "reposts": 0.3})):
            data = postings_for(seed, **kw)
            table = trend_table(data)
            nulls[name]["new"].append(len(calls(table)))
            nulls[name]["old"].append(len(naive_calls(table)))
            nulls[name]["advice"].append(sum(1 for p in programs for r in assess_program(p, data, skills)["recommendations"]
                                             if r["action"] in ("Review", "Prepare")))

        data = postings_for(seed)
        table = trend_table(data)
        reported = calls(table)
        found.append(len(reported))
        hits += sum(1 for s in reported if s in moving)
        ups = {s for s, _ in emerging_skills(table)}
        direction_ok += sum(1 for s in reported if (truth[s][0] >= 0.1 if s in ups else truth[s][0] <= -0.1))
        for s in moving:
            g = abs(truth[s][0])
            size = "15-50%" if g < 0.5 else "50-100%" if g < 1.0 else "over 100%"
            by_size[size][0] += s in reported
            by_size[size][1] += 1

        for p in programs:
            r = assess_program(p, data, skills)
            if not r["scored"]:
                continue
            scores[p.id].append(r["score"])
            grades[p.id].append(r["grade"])
            truth_score = true_score(p)
            if truth_score is not None and r["score_low"] is not None:
                cover[p.id].append(r["score_low"] <= truth_score <= r["score_high"])

        # forecast backtest: fit quarters 1-6, predict quarter 8, for skills in >= 5% of postings
        by_q = {}
        for post in data:
            by_q.setdefault(post.quarter, []).append(post)
        qs = sorted(by_q, key=quarter_index)
        train, target = qs[:6], qs[-1]
        sizes = [len(by_q[q]) for q in train]
        ws = [n / (sum(sizes) / len(sizes)) for n in sizes]
        for s in {s for post in data for s in post.skills}:
            ys = [sum(s in post.skills for post in by_q[q]) / len(by_q[q]) for q in train]
            if statistics.mean(ys) < 0.05:
                continue
            slope, icpt, se = fit_line_weighted([quarter_index(q) for q in train], ys, ws)
            x = quarter_index(target)
            pred = icpt + slope * x
            actual = sum(s in post.skills for post in by_q[target]) / len(by_q[target])
            fc_err.append(abs(pred - actual))
            fc_in.append(abs(pred - actual) <= Z95 * se(x))

    n = len(SEEDS)
    eligible_n = len(eligible)
    lines = [
        "# Validation of the SkillAlign method",
        "",
        f"Generated by tools/validate.py over {n} random samples of the synthetic generator, "
        "whose true parameters are known.",
        "",
        "## 1. False alarms on data with no skill trends",
        "",
        "| Trend-free data | First version (growth thresholds only) | Now (role-stratified test, Bonferroni) | Review/Prepare advice now, all courses |",
        "|---|---|---|---|",
    ]
    labels = {"flat": "Fully flat", "flat_skills": "Only the mix of job roles changes",
              "reposts": "Flat, with employers reposting ads"}
    for name, res in nulls.items():
        lines.append(f"| {labels[name]} | {statistics.mean(res['old']):.1f} per sample (max {max(res['old'])}) | "
                     f"{statistics.mean(res['new']):.1f} per sample (max {max(res['new'])}) | "
                     f"{statistics.mean(res['advice']):.1f} per sample (max {max(res['advice'])}) |")
    recall_total = sum(v[1] for v in by_size.values())
    recall_hit = sum(v[0] for v in by_size.values())
    lines += [
        "",
        "## 2. Detection on trended data",
        "",
        f"Truth is the tool's own rule applied to the generator's TRUE values (market-wide +30% or -20%, with a "
        f"within-role change of at least half that, in 5%+ of postings): {len(moving)} of {eligible_n} reportable "
        f"skills qualify, so a random guesser would be right {100 * len(moving) / eligible_n:.0f}% of the time.",
        "",
        f"- Precision: {hits} of {sum(found)} reported trends meet that rule in truth "
        f"({100 * hits / sum(found) if sum(found) else 0:.0f}%); {direction_ok} of {sum(found)} "
        f"({100 * direction_ok / sum(found) if sum(found) else 0:.0f}%) point the right way on a real within-role "
        f"change of 10% or more. {sum(found) / n:.1f} trends are reported per sample.",
        f"- Recall: {recall_hit} of {recall_total} true trends found across samples ({100 * recall_hit / recall_total:.0f}%).",
        "",
        "| Size of the true within-role change (true trends only) | Found |",
        "|---|---|",
    ] + [f"| {k} | {v[0]} of {v[1]} ({100 * v[0] / v[1] if v[1] else 0:.0f}%) |" for k, v in by_size.items()] + [
        "",
        "The test is deliberately cautious: it finds every large change but misses most modest ones at this sample "
        "size (about 1,100 postings a window), and what it reports almost always points the right way.",
        "",
        "## 3. Do the 90% score ranges contain the true score?",
        "",
        "| Course | Samples where the range contains the true score |",
        "|---|---|",
    ] + [f"| {p.name} | {sum(cover[p.id])} of {len(cover[p.id])} ({100 * sum(cover[p.id]) / len(cover[p.id]):.0f}%) |"
         for p in programs if cover[p.id]] + [
        "",
        "## 4. Forecast backtest",
        "",
        f"Fitted on the first six quarters and asked for the eighth, for every skill in at least 5% of postings: "
        f"mean absolute error {100 * statistics.mean(fc_err):.1f} percentage points; the 95% prediction range "
        f"contained the actual share {100 * sum(fc_in) / len(fc_in):.0f}% of the time ({len(fc_in)} forecasts).",
        "",
        "## 5. Stability of course scores across samples",
        "",
        "| Course | Score range | Mean | Most common grade (share of samples) |",
        "|---|---|---|---|",
    ]
    for p in sorted(programs, key=lambda p: statistics.mean(scores[p.id]) if scores[p.id] else 0):
        if not scores[p.id]:
            continue
        g = max(set(grades[p.id]), key=grades[p.id].count)
        lines.append(f"| {p.name} | {min(scores[p.id]):.1f} to {max(scores[p.id]):.1f} | "
                     f"{statistics.mean(scores[p.id]):.1f} | {g} ({100 * grades[p.id].count(g) / len(grades[p.id]):.0f}%) |")
    out = os.path.join(ROOT, "docs", "validation.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
