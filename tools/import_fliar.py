"""Import the real Fliar 2026 job-postings sample into SkillAlign's format.

Source: Fliar Research (2026), "Job Postings 2026: India and United States"
(sample release), https://huggingface.co/datasets/fliarbi/job-postings-2026,
licence CC BY-NC 4.0. Download job_postings_2026_sample.csv from there, then:

    python tools/import_fliar.py path/to/job_postings_2026_sample.csv

Writes data/real_postings_india_2026.csv with the columns SkillAlign reads
(title, date, skills, sector, district, state, employer). What it changes,
all counted in the printed summary and listed in docs/DATA-SOURCES.md:

- keeps India rows that have a real skills list (drops empty and "null");
- drops rows whose place is outside India (Dubai, Oman, Singapore ...);
- removes the company name from job titles ("Tata 1mg - Head - Logistics"
  -> "Head - Logistics") and replaces the company with an anonymous code,
  used only to group a company's postings when estimating uncertainty;
- normalises state spellings (Tamilnadu, "Odisha (Orissa)", Delhi-NCR ...),
  fills a blank or wrong state from a known city, and blanks non-places
  ("Anywhere In India", "4Th Floor");
- collapses about 2,000 source categories into 16 sectors.

The output is a derived subset and stays under CC BY-NC 4.0.
"""

import csv
import hashlib
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "data", "real_postings_india_2026.csv")

STATES = {"Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana",
          "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
          "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
          "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar", "Chandigarh",
          "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep",
          "Puducherry"}
STATE_ALIASES = {"Delhi-NCR Region": "Delhi", "Delhi Ncr": "Delhi", "Tamilnadu": "Tamil Nadu", "Orrisa": "Odisha",
                 "Odisha (Orissa)": "Odisha", "Chattisgarh": "Chhattisgarh", "Uttarakhand (Uttaranchal)": "Uttarakhand",
                 "Pondicherry": "Puducherry", "Puducherry (Pondicherry)": "Puducherry", "Chandigarh Region": "Chandigarh",
                 "Jammu & Kashmir": "Jammu and Kashmir", "Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
                 "Up": "Uttar Pradesh"}
CITY_ALIASES = {"Bengaluru (Bangalore)": "Bengaluru", "Bangalore": "Bengaluru", "Indiranagar": "Bengaluru",
                "Mumbai City": "Mumbai", "Mumbai Suburban": "Mumbai", "Borivali": "Mumbai", "Andheri East": "Mumbai",
                "Bandra": "Mumbai", "Ghatkopar": "Mumbai", "South Bombay": "Mumbai",
                "Vashi Navi Mumbai": "Navi Mumbai", "Mahape Navi Mumbai": "Navi Mumbai",
                "Gurugram Sub-District": "Gurugram", "Noida Sector 62": "Noida", "Gaziabad": "Ghaziabad",
                "Cochin": "Kochi", "Kochi (Cochin)": "Kochi", "Mysore": "Mysuru", "Mysore Division": "Mysuru",
                "Nasik": "Nashik", "Thiruvanananthapuram": "Thiruvananthapuram", "Trichy": "Tiruchirappalli",
                "Tuticorin": "Thoothukudi", "Pimpri": "Pimpri-Chinchwad", "Pimpri Chinchwad": "Pimpri-Chinchwad",
                "Aurangabad": "Chhatrapati Sambhajinagar", "Delhi Ncr": "Delhi", "Pondicherry": "Puducherry"}
NOT_A_PLACE = {"", "Anywhere In India", "Any Location", "Others", "Metros", "4Th Floor", "104",
               "Office Number 203 - 204", "India"}
FOREIGN = {"Dubai", "Oman", "South Africa", "Saudi Arabia", "Australia", "Singapore", "Overseas", "Middle East",
           "Qatar", "United Arab Emirates", "Kuwait", "Dublin", "China", "Kenya", "Zimbabwe", "Abu Dhabi"}
# a known city decides its state (fills blanks, fixes e.g. Raipur filed under West Bengal)
CITY_STATE = {
    "Bengaluru": "Karnataka", "Mysuru": "Karnataka", "Mangalore": "Karnataka", "Hubli": "Karnataka",
    "Hyderabad": "Telangana", "Warangal": "Telangana", "Nizamabad": "Telangana",
    "Chennai": "Tamil Nadu", "Coimbatore": "Tamil Nadu", "Madurai": "Tamil Nadu", "Hosur": "Tamil Nadu",
    "Pune": "Maharashtra", "Mumbai": "Maharashtra", "Navi Mumbai": "Maharashtra", "Thane": "Maharashtra",
    "Nagpur": "Maharashtra", "Nashik": "Maharashtra", "Kolhapur": "Maharashtra", "Pimpri-Chinchwad": "Maharashtra",
    "Chhatrapati Sambhajinagar": "Maharashtra", "Solapur": "Maharashtra", "Panvel": "Maharashtra",
    "Delhi": "Delhi", "New Delhi": "Delhi", "Noida": "Uttar Pradesh", "Greater Noida": "Uttar Pradesh",
    "Ghaziabad": "Uttar Pradesh", "Lucknow": "Uttar Pradesh", "Mirzapur": "Uttar Pradesh",
    "Gurugram": "Haryana", "Faridabad": "Haryana", "Panchkula": "Haryana",
    "Kolkata": "West Bengal", "Ahmedabad": "Gujarat", "Gandhinagar": "Gujarat", "Vadodara": "Gujarat",
    "Surat": "Gujarat", "Rajkot": "Gujarat", "Jaipur": "Rajasthan", "Udaipur": "Rajasthan",
    "Kochi": "Kerala", "Thiruvananthapuram": "Kerala", "Chandigarh": "Chandigarh", "Mohali": "Punjab",
    "Jalandhar": "Punjab", "Ludhiana": "Punjab", "Indore": "Madhya Pradesh", "Bhopal": "Madhya Pradesh",
    "Bhubaneswar": "Odisha", "Raipur": "Chhattisgarh", "Patna": "Bihar", "Guwahati": "Assam",
    "Dehradun": "Uttarakhand", "Rudrapur": "Uttarakhand", "Kohima": "Nagaland", "Puducherry": "Puducherry",
}
# job-board role first, then keywords in the source category; anything else is "Other"
ROLE_SECTORS = {"software-eng": "Software & IT", "devops-cloud": "Software & IT", "it-support": "Software & IT",
                "security": "Software & IT", "data": "Data & Analytics", "sales": "Sales", "finance": "Finance & Accounting",
                "marketing": "Marketing", "design": "Design & Media", "product": "Product & Management",
                "hr": "Human Resources", "healthcare": "Healthcare", "operations": "Operations & Logistics",
                "logistics": "Operations & Logistics", "manufacturing": "Manufacturing & Engineering",
                "construction": "Construction", "admin": "Administration", "customer-service": "Customer Service",
                "education": "Education", "legal": "Legal", "science-research": "Science & Research",
                "retail-hospitality": "Retail & Hospitality"}
CATEGORY_KEYWORDS = [
    ("Software & IT", r"software|\bit\b|develop|programming|tech|cloud|devops|security|network|\.net"),
    ("Data & Analytics", r"data|analytic|machine learning|\bai\b"),
    ("Finance & Accounting", r"financ|account|bank|tax|audit|insurance|invest"),
    ("Sales", r"sales|business development"),
    ("Marketing", r"marketing|brand|advertis|seo|social media|content"),
    ("Healthcare", r"health|medic|pharma|hospital|clinic|nurs"),
    ("Manufacturing & Engineering", r"manufactur|engineer|production|mechanical|electrical|plant|automotive"),
    ("Design & Media", r"design|creative|media|video|animation"),
    ("Human Resources", r"human resource|\bhr\b|recruit|talent"),
    ("Education", r"educat|teach|academ|training"),
    ("Operations & Logistics", r"logistic|supply chain|warehouse|operations|procurement"),
    ("Retail & Hospitality", r"retail|hospitality|hotel|restaurant"),
    ("Construction", r"construct|civil|architect|real estate"),
    ("Legal", r"legal|law|compliance"),
    ("Customer Service", r"customer|support"),
    ("Administration", r"admin|office|clerical"),
]


def sector_of(role, category):
    if role in ROLE_SECTORS:
        return ROLE_SECTORS[role]
    text = category.lower()
    for sector, pattern in CATEGORY_KEYWORDS:
        if re.search(pattern, text):
            return sector
    return "Other"


def clean_title(title, company):
    """Remove the employer's name from a title like 'Acme - Senior Developer'."""
    if company and company.lower() in title.lower():
        title = re.sub(re.escape(company), " ", title, flags=re.IGNORECASE)
        title = re.sub(r"^[\s\-|:,–]+|[\s\-|:,–]+$", "", title)
        title = re.sub(r"\s+[\-|–]\s+[\-|–]\s+", " - ", title)
    return " ".join(title.split())


def clean_skills(skills):
    items = [s.strip() for s in skills.split("|") if s.strip() and s.strip().lower() != "null"]
    return "|".join(items)


def main(src):
    counts = dict.fromkeys(["read_india", "no_skills", "foreign", "company_in_title", "state_filled",
                            "state_fixed", "state_renamed", "place_blanked", "kept"], 0)
    rows, seen = [], set()
    with open(src, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["country"] != "IN" or r["posting_id"] in seen:
                continue
            seen.add(r["posting_id"])
            counts["read_india"] += 1
            skills = clean_skills(r["skills"])
            if not skills:
                counts["no_skills"] += 1
                continue
            city = CITY_ALIASES.get(re.sub(r"\s+", " ", r["city"]).strip(), r["city"].strip())
            region = r["region"].strip()
            if city in FOREIGN or region in FOREIGN:
                counts["foreign"] += 1
                continue
            state = STATE_ALIASES.get(region, region)
            if state != region:
                counts["state_renamed"] += 1
            if state not in STATES:
                state = ""
            if city in STATES or city in STATE_ALIASES:          # a state written in the city field
                state, city = STATE_ALIASES.get(city, city), ""
            if city in NOT_A_PLACE:
                counts["place_blanked"] += city != ""
                city = ""
            if city in CITY_STATE and state != CITY_STATE[city]:
                counts["state_filled" if not state else "state_fixed"] += 1
                state = CITY_STATE[city]
            title = clean_title(r["title"], r["company"])
            if title != " ".join(r["title"].split()):
                counts["company_in_title"] += 1
            employer = hashlib.sha1(r["company"].strip().lower().encode()).hexdigest()[:10] if r["company"].strip() else ""
            rows.append({"title": title, "date": r["posted_date"].strip(), "skills": skills,
                         "sector": sector_of(r["role"], r["category"]), "district": city, "state": state,
                         "employer": employer})
    counts["kept"] = len(rows)
    rows.sort(key=lambda r: r["date"])
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "date", "skills", "sector", "district", "state", "employer"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} postings to {os.path.normpath(OUT)}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
