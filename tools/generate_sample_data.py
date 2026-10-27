"""Generate the SAMPLE job-postings dataset (data/job_postings.csv).

THESE POSTINGS ARE SYNTHETIC. They exist to show how the method works.
Any trend the tool reports on them was written into ROLES below, which
is exactly why tools/validate.py also runs the method on trend-free
("flat") versions of this data: a method that still reports trends
there is reporting noise.

The postings are synthetic. Each role has a skill profile: the chance a
posting mentions a skill at the start of the period and at the end, with
straight-line change in between. That lets the demo show real-looking
shifts (GenAI spreading into analyst and marketing roles, EV skills
entering automotive service, data-entry volume shrinking) without
claiming to be scraped data. Uploading a real CSV replaces it.

Run:  python tools/generate_sample_data.py            (writes data/job_postings.csv)
      python tools/generate_sample_data.py --flat     (no trends, to stdout check)
"""

import argparse
import csv
import json
import os
import random
import sys

SEED = 42
QUARTERS = ["2024-Q4", "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3"]
# Maharashtra districts (the SIH26134 sponsor's state), weighted roughly by size of job market
DISTRICTS = {"Pune": 18, "Mumbai": 18, "Thane": 12, "Nagpur": 9, "Nashik": 7,
             "Chhatrapati Sambhajinagar": 6, "Kolhapur": 4, "Solapur": 4, "Raigad": 4,
             "Satara": 3, "Jalgaon": 3, "Amravati": 3}

# role: sector, (postings per quarter at start, at end), {skill: (p_start, p_end)}
ROLES = {
    "Software Developer": ("IT & Software", (30, 30), {
        "python": (.45, .60), "java": (.50, .36), "javascript": (.55, .55), "sql": (.50, .50),
        "react": (.30, .45), "git": (.50, .60), "rest_api": (.35, .50), "cloud": (.25, .45),
        "genai": (.03, .35), "html_css": (.40, .28), "testing": (.25, .25), "devops": (.15, .25),
        "cpp": (.20, .18), "dsa": (.25, .25), "linux": (.20, .22), "nodejs": (.15, .25), "nosql": (.10, .18),
        "csharp": (.12, .10), "c_lang": (.08, .06), "os": (.06, .06),
        "problem_solving": (.40, .40), "communication": (.35, .35), "teamwork": (.30, .30)}),
    "Data Analyst": ("IT & Software", (18, 26), {
        "data_analysis": (.80, .80), "excel": (.70, .60), "sql": (.70, .75), "python": (.50, .65),
        "data_viz": (.55, .65), "statistics": (.40, .45), "ml": (.15, .30), "genai": (.02, .32),
        "prompt_eng": (.01, .22), "communication": (.45, .45)}),
    "Cloud DevOps Engineer": ("IT & Software", (10, 16), {
        "cloud": (.85, .90), "devops": (.75, .80), "python": (.35, .45), "git": (.50, .55),
        "cloud_security": (.15, .40), "cybersecurity": (.20, .25), "problem_solving": (.30, .30)}),
    "Cybersecurity Analyst": ("IT & Software", (8, 13), {
        "cybersecurity": (.90, .90), "cloud_security": (.20, .50), "python": (.25, .35),
        "cloud": (.25, .40), "communication": (.30, .30), "problem_solving": (.40, .40)}),
    "Accounts Assistant": ("Office & BFSI", (16, 15), {
        "tally": (.75, .70), "gst": (.45, .65), "excel": (.60, .70), "ms_office": (.35, .22),
        "data_entry": (.30, .15), "communication": (.30, .30), "english": (.25, .25),
        "data_analysis": (.03, .15)}),
    "Data Entry Operator": ("Office & BFSI", (20, 9), {
        "data_entry": (.85, .70), "typing": (.70, .42), "ms_office": (.55, .32), "excel": (.45, .70),
        "english": (.35, .30), "digital_literacy": (.25, .35), "data_analysis": (.02, .14),
        "genai": (.00, .12)}),
    "Digital Marketing Executive": ("Media & Marketing", (12, 15), {
        "digital_marketing": (.85, .85), "seo": (.60, .52), "social_media": (.70, .70),
        "genai": (.05, .45), "prompt_eng": (.02, .32), "data_analysis": (.20, .40),
        "excel": (.30, .35), "ecommerce": (.15, .25), "communication": (.50, .50)}),
    "Electrician": ("Manufacturing", (18, 17), {
        "wiring": (.90, .85), "motors": (.35, .30), "safety": (.60, .65), "solar_pv": (.10, .35), "plc": (.15, .25),
        "iot": (.03, .15), "first_aid": (.20, .25), "problem_solving": (.20, .20), "ev_maint": (.02, .10)}),
    "CNC Operator": ("Manufacturing", (12, 12), {
        "cnc": (.90, .90), "autocad": (.30, .40), "quality_control": (.50, .55), "safety": (.55, .60),
        "iot": (.02, .15), "teamwork": (.20, .20)}),
    "Maintenance Technician": ("Manufacturing", (10, 13), {
        "plc": (.50, .65), "wiring": (.50, .45), "motors": (.40, .40), "iot": (.10, .40), "safety": (.60, .60),
        "quality_control": (.20, .20), "problem_solving": (.40, .45), "welding": (.25, .20)}),
    "Welder": ("Manufacturing", (8, 7), {
        "welding": (.95, .95), "safety": (.70, .70), "quality_control": (.30, .30), "autocad": (.10, .15)}),
    "Solar PV Technician": ("Green Energy & EV", (6, 14), {
        "solar_pv": (.95, .95), "wiring": (.70, .70), "safety": (.60, .65), "energy_audit": (.20, .30),
        "iot": (.05, .20), "bms": (.10, .30)}),
    "EV Service Technician": ("Green Energy & EV", (4, 13), {
        "ev_maint": (.95, .95), "bms": (.50, .70), "wiring": (.40, .40), "safety": (.60, .65),
        "ic_engine": (.15, .05), "customer_service": (.20, .20)}),
    "Automotive Service Technician": ("Automotive", (16, 12), {
        "ic_engine": (.85, .60), "auto_chassis": (.50, .45), "ev_maint": (.05, .35), "bms": (.00, .15), "customer_service": (.30, .30),
        "safety": (.40, .40), "problem_solving": (.25, .25)}),
    "General Duty Assistant": ("Healthcare", (14, 15), {
        "patient_care": (.90, .90), "vitals": (.65, .70), "infection_control": (.60, .65),
        "first_aid": (.50, .55), "ehr": (.08, .35), "telehealth": (.02, .15),
        "digital_literacy": (.10, .30), "communication": (.50, .50)}),
    "Retail Sales Associate": ("Retail & Logistics", (18, 16), {
        "customer_service": (.85, .85), "pos": (.50, .55), "communication": (.60, .60),
        "english": (.35, .35), "inventory": (.30, .45), "ecommerce": (.10, .35), "digital_literacy": (.20, .40)}),
    "Plumber": ("Construction & Trades", (8, 9), {
        "plumbing": (.95, .95), "safety": (.40, .45), "customer_service": (.20, .20),
        "solar_pv": (.03, .08), "problem_solving": (.20, .20)}),
    "Sewing Machine Operator": ("Apparel", (12, 11), {
        "tailoring": (.95, .95), "quality_control": (.40, .45), "teamwork": (.20, .20),
        "safety": (.20, .25)}),
    "AC Technician": ("Construction & Trades", (7, 10), {
        "hvac": (.95, .95), "wiring": (.35, .35), "safety": (.40, .45), "customer_service": (.30, .30),
        "iot": (.02, .10)}),
    "Warehouse Associate": ("Retail & Logistics", (14, 18), {
        "inventory": (.70, .75), "wms": (.20, .50), "safety": (.40, .45), "data_entry": (.20, .15),
        "teamwork": (.30, .30), "digital_literacy": (.15, .35), "excel": (.10, .20)}),
}

EMPLOYERS = ["A mid-size company", "A growing startup", "A leading manufacturer", "A national retail chain",
             "A multi-speciality hospital", "An MSME", "A logistics firm", "A services company"]
PREFIXES = ["", "", "", "Junior ", "Senior ", "Trainee "]
SUFFIXES = ["", "", "", " (Fresher)"]
EXPERIENCE = ["Freshers welcome.", "0-2 years experience.", "1-3 years experience.", "2-5 years experience."]


def lerp(a, b, t):
    return a + (b - a) * t


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def generate(seed=SEED, flat=False):
    """Return the posting rows. flat=True holds every probability and every
    role's volume at its average, so the data contains no trend at all."""
    rng = random.Random(seed)
    with open(os.path.join(DATA_DIR, "skills.json"), encoding="utf-8") as f:
        # case-sensitive synonyms are written with a leading "=" in the taxonomy
        synonyms = {row["id"]: [s.lstrip("=") for s in row["synonyms"]] for row in json.load(f)}
    names, weights = list(DISTRICTS), list(DISTRICTS.values())

    rows = []
    for qi, quarter in enumerate(QUARTERS):
        t = qi / (len(QUARTERS) - 1)
        year, q = int(quarter[:4]), int(quarter[-1])
        for role, (sector, volume, profile) in ROLES.items():
            tt = 0.5 if flat else t
            count = round(lerp(volume[0], volume[1], tt) * rng.uniform(0.85, 1.15))
            for _ in range(count):
                skills = [s for s, (p0, p1) in profile.items() if rng.random() < lerp(p0, p1, tt)]
                if not skills:
                    skills = [max(profile, key=lambda s: profile[s][1])]
                rng.shuffle(skills)
                cut = max(1, round(len(skills) * 0.7))
                must = [rng.choice(synonyms[s]) for s in skills[:cut]]
                nice = [rng.choice(synonyms[s]) for s in skills[cut:]]
                district = rng.choices(names, weights)[0]
                text = f"{rng.choice(EMPLOYERS)} is hiring in {district}. Must have: {', '.join(must)}."
                if nice:
                    text += f" Good to have: {', '.join(nice)}."
                text += " " + rng.choice(EXPERIENCE)
                month = (q - 1) * 3 + rng.randint(1, 3)
                rows.append({
                    "title": rng.choice(PREFIXES) + role + rng.choice(SUFFIXES),
                    "description": text,
                    "date": f"{year}-{month:02d}-{rng.randint(1, 28):02d}",
                    "sector": sector,
                    "district": district,
                    "state": "Maharashtra",
                })
    rows.sort(key=lambda r: r["date"])
    return rows


def write_csv(rows, out):
    writer = csv.DictWriter(out, fieldnames=["title", "description", "date", "sector", "district", "state"])
    writer.writeheader()
    writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--flat", action="store_true", help="no trends: every probability held constant")
    parser.add_argument("--stdout", action="store_true", help="print the CSV instead of writing data/")
    args = parser.parse_args()
    rows = generate(args.seed, args.flat)
    if args.stdout:
        write_csv(rows, sys.stdout)
        return
    out = os.path.join(DATA_DIR, "job_postings.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        write_csv(rows, f)
    print(f"wrote {len(rows)} postings to {os.path.normpath(out)}")


if __name__ == "__main__":
    main()
