# SkillAlign v2 ("Journeys" redesign): what a visitor sees (captured 2026-11-13, local build)

Screenshots are in `shots-v2/`: 01-03 are desktop, 04-09 are phone at 375 px. The data and the engine are the same as v1, except for these fixes:
- the "transformers" → Machine Learning bug is fixed
- the "learn next" pick now prefers common, job-specific skills
- the forecast range is shown

## 0. First load
The page itself appears at once, on phone and desktop alike. A small grey line at the top reads "Loading the SkillAlign engine and job postings…" with a small spinner (shot 04). The home text, the three journey buttons and the course form can all be read and filled in while the line shows. If you press "Check this course" before the engine is ready, the button reads "Getting ready…" and runs by itself once the engine is ready. The download is still about 12 MB the first time.

## 1. Header and navigation
Desktop: logo · Home · Check my course · What should I learn? · Job market · How it works · Your data. On the right is an orange pill reading "● Practice data ▾".
Phone (shots 05-09): the logo and the "Practice data ▾" pill sit at the top. A fixed bar at the bottom of the screen always shows four icons with labels: Home · My course · Learn next · Market.
Tapping the pill opens: "Practice data. These 2,216 job ads are made up, to show how SkillAlign works, so the numbers are not facts about real jobs. [Switch to real job ads] or use your own file." It also has a dropdown (Practice data / Real job ads, India 2026) and the line "2,216 job ads · 2024-Q4 to 2026-Q3". The old yellow banner is gone.

## 2. Home (shots 01, 05)
H1 "Do skill courses teach what jobs ask for?"
"On the practice data, **6 of 10 example courses** miss skills that their own jobs ask for. Check yours in a minute."
"What do you want to do?" Three large buttons:
- 📘 **Check my course**: "Paste a syllabus. See which skills jobs want that it misses. For trainers, ITIs and institutes." →
- 🎯 **What should I learn?**: "Pick the job you want and say what you know. See the one skill to learn next." →
- 📊 **See the job market**: "Which skills employers ask for, which are rising, and how example courses score." →

Three small facts follow: "Asked for most: Workplace Safety, in 23% of job ads" · "Rising fastest: Battery Management Systems, up 213% on last year" · "Job ads read: 2,216, Practice data".
"No sign-up. Nothing you type leaves your phone or computer. How SkillAlign works."

## 3. Check my course (shot 07)
Crumb "Home / Check my course". Lede: "Paste your course outline, one module per line, with hours. SkillAlign compares it with job postings for the jobs the course trains for."
Fields:
- Course name [My course]
- Jobs this course trains for, hint "comma separated, as they appear in job ads, e.g. "data analyst, MIS executive"" [data analyst]
- Syllabus, hint 'one module per line, with hours, e.g. "Advanced Excel (40 hrs)". Write [mandatory] after modules you are not allowed to drop.', pre-filled with 4 lines

Under the syllabus, green chips update live as you type: "Skills found as you type: Communication, Data Analysis, Data Entry, MS Excel, SQL & Databases, Typing Speed".
A fold reads "Add NSQF level or QP code (optional)". When opened, it shows both fields and the note "These are printed on the report for your records. SkillAlign does not look them up."
Buttons [Check this course] [Try an example (two-wheeler mechanic)].
The result appears right under the form, and the page scrolls to it:
"My course · Your course · Compared with 150 job ads for: data analyst · Practice data" [Print or save as PDF]
A box with a coloured left edge holds a big "51/100" and the text: "It teaches about 51% of what these jobs ask for, so it is partial. It misses 5 of 9 skills that 15% or more of these job ads ask for. Likely between 49 and 53 (that range crosses a grade line, so the grade is borderline). If the course stays the same, about 43 next year, because the jobs are changing."
"What to change, most important first":
1. ADD Data Visualisation: asked for in 68% of job ads for these roles (95% range 57%-77%).
2. ADD Python: 59% …
3. ADD Generative AI Tools: 28% …, up 306% on last year.

A link reads "Show 6 more changes". When opened, the Expand items say, for example: "SQL & Databases: asked for in 79% of job ads but given 15 h; 16 h would earn full credit (its 30 h module "SQL for reporting" is shared with Data Analysis)."
Two folded cards follow, "Skill by skill" (Show ▾) and "Modules and the skills found in them" (Show ▾). The module list shows "30 h · 15 h each" when a module teaches two skills.
Below them is the card "Or open an example course: Ten made-up courses, already scored, to show what a report looks like." It holds 10 chip buttons. Tapping one shows its report there, labelled "Example course (made up)".
Print or save as PDF prints only that report, with all folds open.

## 4. What should I learn? (job journey)
Fields: "The job I want" (start typing, then pick from the list) [data analyst]; "What I already know" (skills separated by commas, or paste your resume) [Excel, basic SQL, communication]. Button [Show what to learn]. The result appears under it:
A green box: "LEARN NEXT · **Data Analysis** · asked for in 75% of these job ads."
Next comes a ring showing 37% and the line "37% ready for Data Analyst. Based on the skills in 173 job ads for this job, weighted by how often each is asked for. This is about skills on paper, not about you."
"What employers ask for": green ✓ / red ✗ chips with their shares.
"Courses that teach what you are missing": Data Analytics Foundation [example course] built for this job; Cloud and DevOps Associate [example course]. (The Electrician course no longer appears.)
On real data, for a job with few ads (electrician, 7 ads), the page instead shows:
- the notice "Only 7 job ads for this job in this data, so treat this as a rough guide. Try the practice data to see how it works with more ads."
- Learn next: PLC & Industrial Automation (job-specific skills come before basics like problem solving)
- when no example course fits: "None of the example courses teaches what you are missing. Look for a short course in … on Skill India Digital or at your nearest ITI."

## 5. Job market (shots 08, 09)
Crumb, H1 "The job market", Sector and District filters, then three equal-width tabs: Skills in demand | Example courses | Gaps.
- **Skills in demand.** Four tiles: 2,216 job ads · 70 different skills asked for · "6 of 10 example courses that miss some core skills" · "3 skills rising beyond chance". Next is the card "Skills employers ask for most": "Share of job ads in the latest 4 quarters that mention each skill, and the change on the year before. Tap one to see its trend." Each row shows a bar and a share, plus either "steady" (grey, meaning within chance) or a green "↑ 201%". Tapping a skill opens its trend chart right under that row, with a note such as: "23% of job ads in the latest 4 quarters (261 of 1,134; 95% range 21–26%). No change beyond chance on the year before. Dashed line: a straight-line forecast a year ahead, 26% (95% range 22–31%)." Below that are the cards "Rising" and "Falling".
- **Example courses.** A grey note: "These are made-up example courses, not real institutes. To score your own course, use Check my course." A list follows. On a phone each row shows the course name, its months and matching job ads, the score and grade, and ▾. Desktop also shows a coloured bar and "Next year if unchanged". Tapping a row opens its full report right under that row (shot 06), with the same verdict box, top 3 changes and folds as section 3. On real data, unscored courses get the line "Courses marked "too few" or "unscored" have almost no matching ads in this sample. See them scored on practice data."
- **Gaps.** On desktop this is the old grid, with bigger cells. On a phone it is a list instead (shot 08), one course per row with its missing skills as red chips, e.g. "Junior Software Developer: Python 59%, Cloud Computing 45%", "Data Analytics Foundation: no missing core skills".

## 6. How it works
The same prose as before, plus a grey box at the top, "The course score in one line":
- "Score = the share of what these jobs ask for that the course teaches with enough hours."
- The formula: score = 100 × Σ(share × credit) ÷ Σ share, over skills in 15% or more of ads.
- The grade lines (Strong 75+, Partial 50–74, Weak below 50), and what "borderline" means.

## 7. Your data
The lede is rewritten for placement cells. The CSV rules are now a bullet list ("A CSV file (in Excel: File → Save As → CSV)" …), with the buttons Upload CSV / Download an example file / Back to practice data. The skill reader is unchanged.

## Still the same / not done
English only. There is no "who built what" team section. The download is still 12 MB the first time. Tracking the score over time is not there.
