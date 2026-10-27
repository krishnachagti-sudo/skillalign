# Data sources

| File | What it is | Licence |
|---|---|---|
| `data/job_postings.csv` | 2,236 **synthetic** postings made by `tools/generate_sample_data.py` to demonstrate the method. Not real jobs. | Part of this project |
| `data/real_postings_india_2026.csv` | 19,390 **real** Indian job postings, January to June 2026: title, date, skills list, sector, city and state. Derived from the source below by `tools/import_fliar.py` (India rows with a skills list only; company names, salaries and links removed; states filled or corrected from the city for 3,581 rows where the source left them blank or wrong, e.g. Gandhinagar filed under Maharashtra). | CC BY-NC 4.0, as the source |
| `data/skills.json`, `data/programs.json` | Skill taxonomy and illustrative course outlines written for this project | Part of this project |

## Attribution

This project uses data from Fliar Research (2026), *Job Postings 2026: India and United States* (sample release), https://huggingface.co/datasets/fliarbi/job-postings-2026, licensed under CC BY-NC 4.0 (https://creativecommons.org/licenses/by-nc/4.0/). The derived file is changed as described above and may only be used non-commercially.

## Known limits of the real data

- Two quarters only (2026-Q1: 1,780 postings; 2026-Q2: 17,610). The source notes that monthly volume reflects collection effort, so month-to-month counts are not trends.
- Online job boards: white-collar and IT roles dominate; vocational and informal-sector jobs are barely present.
- Skills lists are written by the source, not by employers verbatim. SkillAlign recognises 54% of skill mentions and at least one skill in 92% of postings.
