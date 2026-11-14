# Data sources

| File | What it is | Licence |
|---|---|---|
| `data/job_postings.csv` | **Synthetic** postings made by `tools/generate_sample_data.py` to demonstrate and test the method. Not real jobs. | Part of this project |
| `data/real_postings_india_2026.csv` | **Real** Indian job postings, January to June 2026, derived from the source below by `tools/import_fliar.py` (changes listed below). | CC BY-NC 4.0, as the source |
| `data/skills.json`, `data/programs.json` | Skill taxonomy and illustrative course outlines written for this project | Part of this project |

## Attribution

This project uses data from Fliar Research (2026), *Job Postings 2026: India and United States* (sample release), https://huggingface.co/datasets/fliarbi/job-postings-2026, licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/). The derived file is changed as described below and may only be used non-commercially. Publishing it on a commercial site would need the source's permission.

## What `tools/import_fliar.py` changed

From 19,994 India rows in the source sample:

- 729 rows without a usable skills list (empty or the literal "null") were dropped;
- 49 rows whose place is outside India (Dubai, Oman, Saudi Arabia, Singapore and others) were dropped;
- 684 job titles had the employer's name removed (e.g. "Tata 1mg - Head - Logistics" became "Head - Logistics"); every employer is replaced by an anonymous 10-character code, used only to group a company's postings when estimating uncertainty;
- 551 state names were respelled to one form (Tamilnadu, "Odisha (Orissa)", Delhi-NCR and similar); 3,106 blank states were filled from a known city and 35 wrong ones corrected (e.g. Raipur filed under West Bengal, Gandhinagar under Maharashtra); 219 non-places ("Anywhere In India", "4Th Floor") were blanked;
- about 2,000 source categories were collapsed into 19 sectors.

That leaves 19,216 rows. When SkillAlign loads them, 22 exact reposts (same employer, title, skills and quarter) are counted once, giving 19,194 postings.

## Known limits of the real data

- The source is a 6% sample that keeps every posting of a hash-chosen subset of companies, so a few large employers weigh heavily; SkillAlign's score ranges resample employers, not postings, for this reason.
- Two quarters only (2026-Q1: about 1,800 postings; 2026-Q2: about 17,400), collected unevenly: the source says monthly volume reflects collection effort, so month-to-month counts are not trends.
- It is an online job-board crawl: white-collar and IT roles dominate. Only 41 postings (0.2%) are hands-on trade jobs and 19 (0.1%) nursing or ward care (see `docs/real_findings.md`, made by `tools/real_findings.py`, which lists every title counted).
- Skills lists are written by the source, not verbatim by employers. SkillAlign recognises 50% of the skill items in these India postings, which its taxonomy was grown from, and 32% on held-out United States postings it never saw.
