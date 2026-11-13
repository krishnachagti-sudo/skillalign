# SkillAlign v1: what a visitor sees (captured 2026-11-13, live site)

URL: krishnachagti-sudo.github.io/skillalign. Screenshots of each step are in `shots/` (01-11 desktop at 1280 wide, 12-14 phone at 375 wide). Read the screenshots too: layout, colour and what sits above the fold matter as much as the words.

## 0. First load
A spinner and "Starting the Python engine in your browser. Loading Python (about 12 MB, first visit only; later visits work offline)…". On a decent connection this takes ~5-10 s; on a 4G phone in a small town, longer. Nothing else is visible until it finishes.

## 1. Header (every page)
Logo "SkillAlign". A dropdown "Synthetic demo data" / "Real postings: India 2026". Next to it: "2,216 postings · 2024-Q4 to 2026-Q3".
Seven tabs: Market pulse | Programs | Gap matrix | Check a syllabus | For learners | Your data | How it works.
On a phone (shot 12) the logo, dropdown and postings line stack; the tab row scrolls sideways and is cut off after "Gap matrix" / "Check…", with no arrow or fade to show more tabs exist.

Yellow banner under the tabs on every page: "**Demo data.** These job postings are synthetic, generated to show how the method works, so the numbers are not facts about real jobs. Switch the data menu to **Real postings**, or upload your own."

## 2. Market pulse (default page, shots 01-03)
H1 "Are skill programs teaching what jobs ask for?"
Lede: "SkillAlign reads job postings, works out which skills employers want and which are changing beyond chance, then scores each training program against that demand."
Filters: Sector (All sectors, Apparel, Automotive, Construction & Trades, Green Energy & EV, Healthcare, IT & Software, Manufacturing, Media & Marketing, Office & BFSI, Retail & Logistics). District / city (12 Maharashtra districts).
Four number tiles: "2,216 postings in this view" | "70 different skills found in them" | "70.9 average program alignment here (out of 100)" | "6 of 10 programs below Strong here".
Card "Most demanded skills" — "Share of postings in the latest four quarters that mention the skill. Click one for its trend." 15 rows, each: name, green bar, share, year-on-year change:
Workplace Safety 23% +6% · Communication 18% −14% · Python 16% +28% · MS Excel 14% +7% · Electrical Wiring 13% +11% · Problem Solving 13% +16% · SQL & Databases 12% +21% · Cloud Computing 11% +40% · Git & Version Control 10% +37% · Data Analysis 9% +11% · Customer Service 8% −11% · Inventory Management 7% +24% · Generative AI Tools 7% +201% · DevOps & Containers 6% +8% · Solar PV Installation 6% +71%.
(Most change numbers are grey = "within chance: not a trend", shown only as a hover tooltip; only +201% is green.)
Card "Emerging" — "Rising by 30% or more, beyond chance, and within the same job roles." Battery Management Systems "5% of postings · +107% within roles" +213% (sparkline) · Generative AI Tools "7% · +191% within roles" +201% · EV Maintenance "6% · +34% within roles" +102%.
Card "Declining" — "No change here passes the significance test with 1,134 recent postings. Smaller samples need bigger changes before SkillAlign calls them a trend."
Clicking a skill opens a card at the bottom of the page (you must scroll to see it): "Workplace Safety: share of postings by quarter", a line chart with a dashed forecast to 26%, and the note: "23% of postings in the latest 4 quarters (95% range 21–26%, 261 of 1,134). 6% (not significant) on the year before. The dashed line is a straight-line forecast four quarters ahead: 26%, 95% range ." (the range is blank).

## 3. Programs (shots 04-06)
H1 "Training programs, scored against the jobs they train for". Lede: "Each program is compared only with postings for its own target roles. The score weights each in-demand skill by how often jobs ask for it and by whether the program gives it enough hours. The range shows how much the score could move with a different sample of postings."
Table columns: PROGRAM | ALIGNMENT (coloured bar) | SCORE AND RANGE | NEXT YEAR | HOURS ON DEMAND. Ten rows, worst first:
Junior Software Developer (Private training institute (illustrative) · 6 months · 195 matching postings) 43 40–46 Weak · next year 34 ↓ · 100%
Automotive Service Technician (ITI trade) 52 44–62 Partial borderline · 31 ↓ · 88%
Retail Sales Associate 54 51–59 Partial · 49 ↓ · 88%
Digital Marketing 68 63–75 Partial · 53 ↓ · 89%
Electrician (ITI trade) 74 69–80 Partial borderline · 71 ↓ · 77%
Data Entry Operator 74 67–77 Partial borderline · 54 ↓ · 93%
General Duty Assistant 84 78–88 Strong · 75 ↓ · 100%
Solar PV Installer 86 81–94 Strong · 76 ↓ · 100%
Cloud and DevOps Associate 87 82–90 Strong · 88 · 100%
Data Analytics Foundation 88 86–89 Strong · 78 ↓ · 100%
(9 of 10 show a red ↓ next year.)
Clicking a row opens the report BELOW the whole table (page scrolls to it). Example, Junior Software Developer:
"Private training institute (illustrative) · 6 months · compared with 195 postings for: software developer, software engineer, full stack developer, frontend developer, front end developer, backend developer, web developer, java developer, python developer, .net developer" [Download report]
Tiles: "43 alignment today · Weak, range 40–46" | "34 alignment next year if unchanged" | "7 / 20 core skills taught" | "100% of 400 hours on core skills".
"What to change": 13 green ADD tags, in this order: Cloud Computing 45% · Python 59% · React 43% · Generative AI Tools 28% · REST APIs 39% · Node.js 25% · Problem Solving 38% · NoSQL Databases 18% · Data Structures & Algorithms 27% · DevOps & Containers 21% · Linux & Shell 19% · Software Testing 23% · C++ 22%. Each: "asked for in 45% of postings for these roles (95% range 35%-54%)."
"Skill by skill" table, "Hours column: hours given / hours needed for full credit." Columns SKILL | SHARE OF POSTINGS (bar) | % | YEAR ON YEAR | FORECAST | IN PROGRAM | HOURS. Rows include: Git & Version Control 65% +34% 79% ✓ taught 20 / 9 · Python 59% +12% 82% ✗ missing / 8 · JavaScript 50% −18% 27% ✓ taught 100 / 7 · Java 45% −5% 43% ✓ taught 120 / 6 · Communication [mandatory] 31% −20% 27% ✓ taught 10 / 5 … 20 rows.
"Modules and the skills found in them": Web Page Design 80 h → HTML & CSS · JavaScript Programming 100 h → JavaScript · Core Java 120 h → Java · Databases 60 h → SQL & Databases · Version Control 20 h → Git · Soft Skills [mandatory] 20 h → Communication, Teamwork.
Digital Marketing report shows a module "Email Campaigns 20 h — no skill recognised: not counted".

## 4. Gap matrix (shot 07; phone shot 14)
H1 "Gap matrix". Lede: "Rows are programs; columns are the skills each program's own target jobs ask for most. The darker a cell, the more that program's jobs ask for the skill. A tick means it is taught; a red outline marks a skill in 15% or more of its jobs that the program does not teach."
10 rows × 24 columns with column names rotated 90°. Cells green shades, ✓ or a red-outlined "!". Legend: rarely asked / asked in most postings / ✓ taught / gap. Most cells empty. On a phone only ~2 columns are visible and the table must be dragged sideways; nothing says so.

## 5. Check a syllabus (shots 08-09)
H1 "Check a syllabus". Lede: "Paste any course outline, one module per line, with hours if you have them. SkillAlign finds the skills it teaches, tells you which lines it could not read, and scores it against the jobs you name."
Form: Program name [My course] · Target roles "comma separated, as they appear in job titles (at least 3 letters each)" [data analyst] · NSQF level (optional) · Qualification pack code (optional) · Syllabus textarea, hint: 'one module per line, e.g. "Advanced Excel (40 hrs)". Add [mandatory] to modules the curriculum requires; they are never advised to cut. You can paste a qualification pack's National Occupational Standards here, one per line.' Pre-filled:
  Spreadsheets: advanced Excel and pivot tables (40 hrs) / SQL for reporting (30 hrs) / Typing and data entry practice (40 hrs) / Business communication (20 hrs) [mandatory]
Buttons [Score this syllabus] [Load an example]. Under the form, live as you type: "Skills found in this syllabus as you type: Communication, Data Analysis, Data Entry, MS Excel, SQL & Databases, Typing Speed".
Result (appears below; page scrolls): "My course · Pasted syllabus · compared with 150 postings for: data analyst" [Download report]
Tiles: 51 alignment today · Partial (borderline) range 49–53 | 43 next year if unchanged | 4 / 9 core skills taught | 69% of 130 hours on core skills.
What to change (order as shown): ADD Generative AI Tools 28% "up 306% on last year" · ADD Data Visualisation 68% · ADD Python 59% · ADD Machine Learning 32% · ADD Statistics 44% · EXPAND SQL & Databases: "asked for in 79% of postings but given 15 h; 16 h would earn full credit." · EXPAND Data Analysis 77% "given 15 h; 16 h would earn full credit" · REDUCE Typing Speed: "only 0% of postings ask for it (at most 5%), yet it takes 20 training hours." · REDUCE Data Entry: same wording.
(The user typed 30 hrs for SQL; the page says "given 15 h" because the 30 h module was split across two skills. "130 hours" total though the user typed 130 — consistent.)

## 6. For learners (shots 10-11)
H1 "How ready am I for a job?" Lede: "Pick the job you want and tell SkillAlign what you can do. It shows what employers ask for, what you're missing, which words it couldn't read, and which program closes the most gaps."
Form: Job I want ("start typing to search the jobs in this data") [data analyst] · What I can do ("paste your resume or list skills, separated by commas") [I know Excel and basic SQL. Good communication skills.] · [Check my readiness]
Result: red ring "37%" — "37% ready for Data Analyst. Weighted by how often each skill appears in 173 postings for this job. Learn next: **Generative AI Tools**, asked for in 29% of these postings and rising."
"What employers ask for — Skills in at least 15% of postings. Green: you have it. Red: missing." ✓ SQL & Databases 79% · ✗ Data Analysis 75% · ✗ Data Visualisation 67% · ✓ MS Excel 62% · ✗ Python 58% · ✗ Statistics 42% · ✓ Communication 41% · ✗ Machine Learning 34% · ✗ Generative AI Tools 29%.
"Programs that close your gaps": 4 MONTHS Data Analytics Foundation (built for this job) covers Data Visualisation, Data Analysis, Python, Statistics · **2 YEARS Electrician (ITI trade) covers Machine Learning.** · 5 MONTHS Cloud and DevOps Associate covers Python.

Same tab on REAL data, job "electrician", text "wiring, maine ITI kiya hai, motor rewinding, safety":
"29% ready for Electrician. Weighted by how often each skill appears in **7 postings** for this job. Learn next: Problem Solving, asked for in 43% of these postings." ✗ Problem Solving 43% · ✗ PLC & Industrial Automation 29% · ✓ Electrical Wiring 29%. "Skills we read from your text: Electric Motors & Transformers, Electrical Wiring. Not recognised, so not counted (if these are skills, readiness is understated): maine ITI kiya hai, safety". "None of the listed programs teaches your missing skills."

## 7. Your data
H1 "Use your own job postings". Lede: "SkillAlign ships two datasets: synthetic demo postings and 19,194 real Indian postings. Upload your own and every score on the site is recomputed from them. Nothing leaves your browser."
Card "CSV format": one dense paragraph (required columns title, date, description and/or skills; optional sector, district/city, state; employer column de-duplicates; separators; date formats; "At least eight quarters give trends; fewer still give shares and scores."). Buttons [Upload CSV] [Download the sample CSV] [Go back to sample data].
Card "Try the skill reader": textarea with "Hiring EV service technician. Must know lithium-ion batteries, EV diagnostics and workplace safety. Spoken English a plus, ग्राहक सेवा अनुभव, hydrogen fuel cells." Chips: Battery Management Systems from "lithium-ion batteries" · Customer Service from "ग्राहक सेवा" · EV Maintenance from "EV diagnostics" · English Proficiency from "Spoken English" · Workplace Safety from "workplace safety" · not recognised: hydrogen fuel cells.

## 8. How it works
Long prose page, 7 headed sections: 1. Reading skills out of text · 2. Measuring demand, honestly (Mantel-Haenszel, Bonferroni) · 3. Scoring a program (core = 15%+, 30-posting minimum, 200-hour reference course, 400 employer resamples, 90% range) · 4. Recommendations (Add / Expand / Prepare / Reduce / Review) · Checked against the truth · Real data (Fliar, 6% sample, recognises 50% of skill items, 32% on held-out US postings, 0.2% trade jobs) · Limits ("Nothing yet shows that higher scores lead to more placements.").

## 9. Real postings mode (dropdown → "Real postings: India 2026")
Banner: "**Real postings.** 19,194 Indian job ads, 2026-Q1 to 2026-Q2, from Fliar Research under CC BY-NC 4.0 … A 6% sample of companies, collected unevenly … Two quarters only: shares and scores, no trends. It holds very few vocational jobs, so trade courses cannot be scored from it."
Market pulse: State filter appears (30 states); District dropdown has ~230 cities in one long list. Card still says "Share of postings in the latest four quarters" though only two exist; every change column shows "–". Tiles: 19,194 postings · 97 skills · 67.9 average alignment · "3 of 5 programs below Strong".
Top skills: SQL & Databases 14% · Communication 13% · Data Analysis 12% · Python 12% · Cloud Computing 11% · Project Management & Agile 10% · Risk & Compliance 9% · Accounting & Finance 9% …
Programs: 5 scored (Junior Software Developer 40 Weak · Data Entry Operator 62 Partial borderline · Digital Marketing 69 · Cloud and DevOps 83 · Data Analytics 86), 5 greyed "Too few postings"/"Unscored" (Electrician 16 postings, Solar PV 0, General Duty Assistant 0, Retail Sales 14, Automotive 0). NEXT YEAR is "–" everywhere.

## 10. Footer
"SkillAlign is a student prototype for Smart India Hackathon problem SIH26134, "Challenges in aligning skill development programs with industry requirements and emerging job market demands". Built in Python, run in the browser with Pyodide. Source code."
