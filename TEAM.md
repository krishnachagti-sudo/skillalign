# Team

Every member adds one real piece to SkillAlign from their own GitHub account, in the browser, with nothing to install. Each takes about 30-60 minutes, and the site and the tests use what you add.

**How (same for everyone):**
1. Sign in to GitHub and open your link below. GitHub offers to fork the repo the first time; say yes.
2. Make your change in the editor, click **Commit changes**, then **Create pull request**.
3. The tests run on the pull request. If one fails, its message says which line to fix. Krishna merges and publishes.

| Member | Piece | Your link | Done when |
|---|---|---|---|
| Krishna Chagti | Engine, scoring method, data cleaning, site, persona review and redesign | (done) | |
| Krishay | Test the site with 2 real people | [create your file](https://github.com/krishnachagti-sudo/skillalign/new/main/reports/user-tests) | 2 files, `reports/user-tests/krishay-1.md` and `-2.md`, filled from `_TEMPLATE.md` |
| Mansha | Hindi translation of the site | [edit hi.json](https://github.com/krishnachagti-sudo/skillalign/edit/main/site/i18n/hi.json) | every `""` filled with Hindi |
| Navya | Marathi translation of the site | [edit mr.json](https://github.com/krishnachagti-sudo/skillalign/edit/main/site/i18n/mr.json) | every `""` filled with Marathi |
| Priyanshu | 2 real ITI trade syllabi | [create your files](https://github.com/krishnachagti-sudo/skillalign/new/main/data/example_syllabi) | 2 files in the `_TEMPLATE.txt` format, from official DGT/NCVT syllabi |
| Sanskar | 2 real short-course syllabi | [create your files](https://github.com/krishnachagti-sudo/skillalign/new/main/data/example_syllabi) | 2 files in the `_TEMPLATE.txt` format, from Skill India / NSDC qualification packs |
| Vishal | 25 test cases for the skill reader | [edit extraction_cases.csv](https://github.com/krishnachagti-sudo/skillalign/edit/main/tests/extraction_cases.csv) | 25 new rows that pass |
| Yashraj | 20 real job ads for trade jobs | [edit trade_job_ads.csv](https://github.com/krishnachagti-sudo/skillalign/edit/main/data/contrib/trade_job_ads.csv) | 20 rows of real ads |

## Details for each piece

**Krishay: user tests.** The biggest gap in the project: every usability finding so far is simulated. Sit with 2 people (ideally one ITI or diploma student and one classmate not on the team). Ask them to do the 3 tasks in `reports/user-tests/_TEMPLATE.md` on their phone while saying what they think. Write down where they get stuck, in their words. Ask permission first, and use first names only.

**Mansha and Navya: translations.** Each line is `"English text": ""`. Type your translation between the second pair of quotes, and leave the English as it is. Example: `"Home": "होम"`. Keep skill names (Python, Excel, SQL) in English, because job ads use them. If a translation needs a `"` inside it, write `\"`. To see your work, pick the language in the menu at the top right of the live site after your pull request is merged.

**Priyanshu and Sanskar: real syllabi.** Copy the format of `_TEMPLATE.txt` into a new file named like `iti-fitter.txt`. Use a real, public syllabus. Pick jobs the practice data has enough ads for, or the course cannot be scored: Priyanshu takes two ITI trades from **welder, plumber, CNC operator, AC technician** (DGT/NCVT curriculum PDFs); Sanskar takes two short courses from **warehouse associate, sewing machine operator, accounts assistant** (Skill India / NSDC qualification packs). Write that job title, exactly as in the bold list, on the `Jobs:` line. Put the real link in `Source:` and your name in `By:`. Every module needs its hours, and you need at least 4 modules. Your syllabi appear as one-tap examples on "Check my course", credited to you.

**Vishal: skill-reader tests.** Each row is a sentence from a job ad, then the skill ids SkillAlign should find, separated by `|` (ids are in `data/skills.json`, for example `excel|sql`), then your name. Try each sentence first on the live site (Your data → Try the skill reader) and add only cases you have checked. If you find a sentence it reads wrongly, add it to your pull request description: that is a real bug found.

**Yashraj: trade job ads.** The real dataset has almost no electrician, welder, fitter or mechanic jobs, so ITI courses cannot be scored. Copy 20 real ads for such jobs from public job portals: title, date (2026-11-13 format), the full description, district, state, and the ad's link in `source`. Put each description in double quotes. Once there are enough, these let SkillAlign score trade courses on real ads.
