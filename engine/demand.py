"""Measuring what the job market asks for, and how that is changing.

The basic number is a skill's share: the fraction of postings that
mention it. Shares are compared between the latest four quarters and
the four before them (growth), and a straight line fitted through the
quarterly shares gives a short forecast.
"""


def sort_quarters(quarters):
    """'2025-Q3' style labels sort correctly as text, but make it explicit."""
    return sorted(set(quarters), key=lambda q: (int(q[:4]), int(q[-1])))


def matches_role(posting, roles):
    """True if the posting title contains any of the role phrases."""
    if not roles:
        return True
    title = posting.title.lower()
    return any(role in title for role in roles)


def filter_postings(postings, roles=None, sector=None, city=None, quarters=None):
    selected = []
    for p in postings:
        if roles and not matches_role(p, roles):
            continue
        if sector and p.sector != sector:
            continue
        if city and p.city != city:
            continue
        if quarters is not None and p.quarter not in quarters:
            continue
        selected.append(p)
    return selected


def skill_counts(postings):
    counts = {}
    for p in postings:
        for skill_id in p.skills:
            counts[skill_id] = counts.get(skill_id, 0) + 1
    return counts


def skill_shares(postings):
    """{skill_id: fraction of postings mentioning it}."""
    if not postings:
        return {}
    total = len(postings)
    return {skill_id: n / total for skill_id, n in skill_counts(postings).items()}


def shares_by_quarter(postings):
    """{quarter: {skill_id: share}} for every quarter in the data."""
    grouped = {}
    for p in postings:
        grouped.setdefault(p.quarter, []).append(p)
    return {q: skill_shares(grouped[q]) for q in sort_quarters(grouped)}


def split_windows(postings, window=4):
    """Split quarters into (recent, previous) lists of up to `window` each."""
    quarters = sort_quarters(p.quarter for p in postings)
    recent = quarters[-window:]
    previous = quarters[-2 * window:-window] if len(quarters) > window else []
    return recent, previous


def fit_line(xs, ys):
    """Least-squares straight line. Returns (slope, intercept).

    slope = sum((x - mean_x)(y - mean_y)) / sum((x - mean_x)^2)
    """
    n = len(xs)
    if n == 0:
        return 0.0, 0.0
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    spread = sum((x - mean_x) ** 2 for x in xs)
    if spread == 0:
        return 0.0, mean_y
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / spread
    return slope, mean_y - slope * mean_x


def trend_table(postings, window=4, horizon=4, min_postings=1):
    """Per-skill demand summary.

    Returns {skill_id: {
        share      - share across the recent window,
        previous   - share across the previous window (None if no data),
        growth     - relative change recent vs previous (None if no data),
        slope      - change in share per quarter (fitted line),
        forecast   - projected share `horizon` quarters after the last one,
        series     - [(quarter, share), ...] for charting,
        postings   - number of recent postings mentioning it,
    }}
    """
    recent_q, previous_q = split_windows(postings, window)
    recent = [p for p in postings if p.quarter in recent_q]
    previous = [p for p in postings if p.quarter in previous_q]
    recent_share = skill_shares(recent)
    previous_share = skill_shares(previous)
    recent_count = skill_counts(recent)
    by_quarter = shares_by_quarter(postings)
    quarters = list(by_quarter)

    table = {}
    for skill_id in set(recent_share) | set(previous_share):
        if recent_count.get(skill_id, 0) < min_postings and skill_id not in previous_share:
            continue
        series = [(q, by_quarter[q].get(skill_id, 0.0)) for q in quarters]
        slope, intercept = fit_line(list(range(len(series))), [s for _, s in series])
        projected = intercept + slope * (len(series) - 1 + horizon)
        now = recent_share.get(skill_id, 0.0)
        before = previous_share.get(skill_id) if previous else None
        if before is None:
            growth = None
        elif before == 0:
            growth = None if now == 0 else 9.99  # brand-new skill: show as a large rise
        else:
            growth = min((now - before) / before, 9.99)
        table[skill_id] = {
            "share": now,
            "previous": before,
            "growth": growth,
            "slope": slope,
            "forecast": max(0.0, min(1.0, projected)),
            "series": series,
            "postings": recent_count.get(skill_id, 0),
        }
    return table


def emerging_skills(table, min_share=0.05, min_growth=0.3):
    """Skills already visible in demand and rising fast."""
    rows = [(sid, t) for sid, t in table.items()
            if t["share"] >= min_share and t["growth"] is not None and t["growth"] >= min_growth]
    return sorted(rows, key=lambda r: r[1]["growth"], reverse=True)


def declining_skills(table, min_previous=0.05, max_growth=-0.2):
    """Skills that were in demand and are clearly falling."""
    rows = [(sid, t) for sid, t in table.items()
            if t["previous"] is not None and t["previous"] >= min_previous
            and t["growth"] is not None and t["growth"] <= max_growth]
    return sorted(rows, key=lambda r: r[1]["growth"])
