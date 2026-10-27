"""Measuring what the job market asks for, and how that is changing.

The basic number is a skill's share: the fraction of postings that
mention it, with a 95% Wilson interval because a share measured from 50
postings is much less certain than one from 5,000.

Change is measured between two calendar windows: the latest four
quarters and the four before them. A change only counts as a trend when
a two-proportion z-test says it is unlikely to be chance, and when it
also holds WITHIN job roles, so a skill does not look like it is
"declining" just because the roles that use it hire less.

Because dozens of skills are tested at once, a plain 5% test would flag
a few skills by luck every time. The z threshold is therefore Bonferroni
corrected: with m skills tested, |z| must pass the 1 - 0.05/(2m) normal
quantile (about 3.3 for 60 skills instead of 1.96).

A straight line fitted through the quarterly shares (least squares)
gives a short forecast, only when there are at least six quarters.
"""

import math
import re

Z95 = 1.96
SENIORITY = re.compile(r"\b(?:junior|senior|sr|jr|trainee|fresher|apprentice|intern)\b\.?|\(.*?\)", re.IGNORECASE)


# --- quarters ---------------------------------------------------------------

def quarter_index(q):
    """'2025-Q3' -> 2025*4 + 2, so consecutive quarters differ by exactly 1."""
    year, n = q.split("-Q")
    return int(year) * 4 + int(n) - 1


def sort_quarters(quarters):
    return sorted(set(quarters), key=quarter_index)


def split_windows(postings, window=4):
    """Calendar windows: (recent quarters, previous quarters), each up to `window` long.

    Windows are counted back from the latest quarter in the data, by the
    calendar, so a gap in the data is never mistaken for a year passing.
    """
    present = sort_quarters(p.quarter for p in postings)
    if not present:
        return [], []
    latest = quarter_index(present[-1])
    recent = [q for q in present if latest - window < quarter_index(q) <= latest]
    previous = [q for q in present if latest - 2 * window < quarter_index(q) <= latest - window]
    return recent, previous


# --- roles ------------------------------------------------------------------

def role_family(title):
    """'Sr. Data Analyst (Fresher)' -> 'data analyst'."""
    cleaned = SENIORITY.sub(" ", title.lower())
    # "Team Lead - Retail Sales Associate", "Data Analyst | Pune": keep the longest part
    cleaned = max(re.split(r"\s[-|–]\s", cleaned), key=len)
    cleaned = re.sub(r"[^\w\s/&+#.]", " ", cleaned)
    return " ".join(cleaned.split()).strip(" .")


def role_patterns(roles):
    """Whole-word patterns for role phrases; phrases under 3 letters are refused."""
    patterns = []
    for role in roles or []:
        role = " ".join(role.lower().split())
        if len(role) < 3:
            raise ValueError(f"role '{role}' is too short to match job titles safely")
        patterns.append(re.compile(rf"(?<!\w){re.escape(role)}(?!\w)"))
    return patterns


def matches_role(posting, patterns):
    title = posting.title.lower()
    return any(p.search(title) for p in patterns)


def filter_postings(postings, roles=None, sector=None, district=None, quarters=None):
    patterns = role_patterns(roles) if roles else None
    selected = []
    for p in postings:
        if patterns and not matches_role(p, patterns):
            continue
        if sector and p.sector != sector:
            continue
        if district and p.district != district:
            continue
        if quarters is not None and p.quarter not in quarters:
            continue
        selected.append(p)
    return selected


# --- statistics -------------------------------------------------------------

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


def wilson(k, n, z=Z95):
    """95% Wilson score interval for a share k/n. Returns (low, high)."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def z_two_proportions(k1, n1, k2, n2):
    """z statistic for 'share k1/n1 differs from k2/n2'. 0 when undefined."""
    if n1 == 0 or n2 == 0:
        return 0.0
    pooled = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    return 0.0 if se == 0 else (k1 / n1 - k2 / n2) / se


def normal_quantile(p):
    """z such that P(Z <= z) = p for a standard normal, by bisection on erf."""
    lo, hi = -10.0, 10.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if 0.5 * (1 + math.erf(mid / math.sqrt(2))) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def bonferroni_z(tests, alpha=0.05):
    """Two-sided z threshold when `tests` comparisons are made at once."""
    return normal_quantile(1 - alpha / (2 * max(1, tests)))


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


def within_role_growth(recent, previous):
    """Change in each skill's share inside each job role, weighted by the
    role's recent hiring - so a shift in WHICH roles are hiring is not read
    as a change in the skill. {skill_id: relative change} (None if no role
    appears in both windows)."""
    def by_role(postings):
        groups = {}
        for p in postings:
            groups.setdefault(role_family(p.title), []).append(p)
        return groups

    now, before = by_role(recent), by_role(previous)
    common = [r for r in now if r in before]
    if not common:
        return {}
    shares_now = {r: skill_shares(now[r]) for r in common}
    shares_before = {r: skill_shares(before[r]) for r in common}
    skills = set().union(*shares_now.values(), *shares_before.values())
    result = {}
    for s in skills:
        change = base = 0.0
        for r in common:
            w = len(now[r])
            change += w * (shares_now[r].get(s, 0.0) - shares_before[r].get(s, 0.0))
            base += w * shares_before[r].get(s, 0.0)
        result[s] = None if base == 0 else change / base
    return result


# --- the trend table ----------------------------------------------------------

def trend_table(postings, window=4, horizon=4):
    """Per-skill demand summary.

    {skill_id: {
        share, low, high - share in the recent window and its 95% interval
        count, n         - postings mentioning it / postings, recent window
        previous         - share in the previous window (None if no previous data)
        growth           - relative change recent vs previous (None if undefined)
        is_new           - absent in the previous window, present now
        z, significant   - two-proportion z-test; significant = |z| passes the
                           Bonferroni threshold for all skills tested
        within_growth    - the same change measured inside job roles (or None)
        slope, forecast  - fitted change per quarter; share `horizon` quarters ahead
        forecast_ok      - False when fewer than 6 quarters (forecast = share)
        series           - [(quarter, share), ...] for charting
    }}
    """
    recent_q, previous_q = split_windows(postings, window)
    recent = [p for p in postings if p.quarter in recent_q]
    previous = [p for p in postings if p.quarter in previous_q]
    n_now, n_before = len(recent), len(previous)
    count_now, count_before = skill_counts(recent), skill_counts(previous)
    within = within_role_growth(recent, previous) if previous else {}

    grouped = {}
    for p in postings:
        grouped.setdefault(p.quarter, []).append(p)
    quarters = sort_quarters(grouped)
    by_quarter = {q: skill_shares(grouped[q]) for q in quarters}
    xs = [quarter_index(q) for q in quarters]
    forecast_ok = len(quarters) >= 6

    tested = set(count_now) | set(count_before)
    z_crit = bonferroni_z(len(tested))
    table = {}
    for skill_id in tested:
        k1, k0 = count_now.get(skill_id, 0), count_before.get(skill_id, 0)
        now = k1 / n_now if n_now else 0.0
        before = (k0 / n_before) if n_before else None
        if before is None:
            growth, is_new = None, False
        elif before == 0:
            growth, is_new = None, now > 0
        else:
            growth, is_new = (now - before) / before, False
        z = z_two_proportions(k1, n_now, k0, n_before) if n_before else 0.0
        series = [(q, by_quarter[q].get(skill_id, 0.0)) for q in quarters]
        slope, intercept = fit_line(xs, [s for _, s in series])
        forecast = intercept + slope * (xs[-1] + horizon) if forecast_ok and xs else now
        low, high = wilson(k1, n_now)
        table[skill_id] = {
            "share": now, "low": low, "high": high, "count": k1, "n": n_now,
            "previous": before, "growth": growth, "is_new": is_new,
            "z": z, "z_crit": z_crit, "significant": abs(z) >= z_crit,
            "within_growth": within.get(skill_id),
            "slope": slope if forecast_ok else 0.0,
            "forecast": max(0.0, min(1.0, forecast)), "forecast_ok": forecast_ok,
            "series": series,
        }
    return table


def is_rising(t, min_growth=0.3):
    if not t["significant"] or t["z"] <= 0:
        return False
    if not (t["is_new"] or (t["growth"] is not None and t["growth"] >= min_growth)):
        return False
    return t["within_growth"] is None or t["within_growth"] >= min_growth / 2


def is_falling(t, max_growth=-0.2):
    if not t["significant"] or t["z"] >= 0 or t["growth"] is None or t["growth"] > max_growth:
        return False
    return t["within_growth"] is None or t["within_growth"] <= max_growth / 2


def emerging_skills(table, min_share=0.05, min_postings=5):
    """Skills already visible in demand and rising beyond chance."""
    rows = [(sid, t) for sid, t in table.items()
            if t["share"] >= min_share and t["count"] >= min_postings and is_rising(t)]
    return sorted(rows, key=lambda r: (r[1]["is_new"], r[1]["growth"] or 0), reverse=True)


def declining_skills(table, min_previous=0.05):
    """Skills that were in demand and are falling beyond chance."""
    rows = [(sid, t) for sid, t in table.items()
            if t["previous"] is not None and t["previous"] >= min_previous and is_falling(t)]
    return sorted(rows, key=lambda r: r[1]["growth"])
