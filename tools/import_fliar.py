"""Import the real Fliar 2026 job-postings sample into SkillAlign's format.

Source: Fliar Research (2026), "Job Postings 2026: India and United States"
(sample release), https://huggingface.co/datasets/fliarbi/job-postings-2026,
licence CC BY-NC 4.0. Download job_postings_2026_sample.csv from there, then:

    python tools/import_fliar.py path/to/job_postings_2026_sample.csv

Writes data/real_postings_india_2026.csv: India rows only, with the
columns SkillAlign reads (title, date, skills, sector, district, state).
Company names, salaries and links are left out. The file is a derived
subset and stays under the source's CC BY-NC 4.0 licence; see
docs/DATA-SOURCES.md.
"""

import csv
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "data", "real_postings_india_2026.csv")
ROLE_SECTORS = {"software-eng": "Software & IT", "devops-cloud": "Software & IT", "data": "Data & Analytics",
                "sales": "Sales", "finance": "Banking & Financial Services", "marketing": "Marketing",
                "design": "Design", "product": "Product", "hr": "Human Resources", "healthcare": "Healthcare",
                "operations": "Operations", "manufacturing": "Manufacturing", "admin": "Administration",
                "customer-service": "Customer Service"}


# The source leaves the state blank for many rows (e.g. most Bengaluru postings) and
# files a few cities under the wrong state (Gandhinagar under Maharashtra). For these
# major cities the state is set from the city; every such correction is counted.
CITY_STATE = {"Bengaluru": "Karnataka", "Mysuru": "Karnataka", "Hyderabad": "Telangana", "Chennai": "Tamil Nadu",
              "Coimbatore": "Tamil Nadu", "Pune": "Maharashtra", "Mumbai": "Maharashtra", "Navi Mumbai": "Maharashtra",
              "Thane": "Maharashtra", "Nagpur": "Maharashtra", "Nashik": "Maharashtra", "Kolhapur": "Maharashtra",
              "Delhi": "Delhi", "New Delhi": "Delhi", "Noida": "Uttar Pradesh", "Lucknow": "Uttar Pradesh",
              "Gurgaon": "Haryana", "Kolkata": "West Bengal", "Ahmedabad": "Gujarat", "Gandhinagar": "Gujarat",
              "Jaipur": "Rajasthan", "Kochi": "Kerala", "Thiruvananthapuram": "Kerala", "Chandigarh": "Chandigarh",
              "Indore": "Madhya Pradesh", "Bhubaneswar": "Odisha"}


def clean_city(city):
    """'Bengaluru (Bangalore)' -> 'Bengaluru'; 'Mumbai City' -> 'Mumbai'."""
    city = re.sub(r"\s*\(.*?\)", "", city or "").strip()
    return {"Mumbai City": "Mumbai", "Mumbai Suburban": "Mumbai", "Gurugram": "Gurgaon"}.get(city, city)


def main(src):
    seen, rows, fixed = set(), [], 0
    with open(src, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["country"] != "IN" or not r["skills"].strip() or r["posting_id"] in seen:
                continue
            seen.add(r["posting_id"])
            city = clean_city(r["city"])
            state = "" if r["region"] == "India" else r["region"].replace(" Region", "").strip()
            if city in CITY_STATE and state != CITY_STATE[city]:
                state, fixed = CITY_STATE[city], fixed + 1
            rows.append({
                "title": r["title"].strip(),
                "date": r["posted_date"].strip(),
                "skills": r["skills"].strip(),
                "sector": r["category"].strip() or ROLE_SECTORS.get(r["role"], ""),
                "district": city,
                "state": state,
            })
    rows.sort(key=lambda r: r["date"])
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "date", "skills", "sector", "district", "state"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} India postings to {os.path.normpath(OUT)} ({fixed} states set from the city)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
