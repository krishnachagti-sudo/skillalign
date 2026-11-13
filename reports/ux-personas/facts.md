# Fact sheet: SkillAlign UX review (2026-11-13)

Tags: [seen] = checked on the live site or in the repo today · [desk] = from the repo docs or memory notes · [guess] = assumption, not checked.

## Decision this review feeds
Which UI/UX problems to fix first in SkillAlign, and which of 2-3 redesign directions to build, before the IPL course demo/viva and any SIH-style judging.
- Personas MAY: list where they get stuck or misread a number, list objections, rank tabs and fixes, rank redesign options.
- Personas MAY NOT: say how many real users would use it, set a grade the faculty will give, or stand in for real think-aloud tests. Usability agents found only ~3 of 10 real failure points without rich context (CHI 2026), so this run is screening. Real check: 3-5 real people (two classmates outside the team, one ITI/diploma student, one faculty member or TA) each do the same three tasks while thinking aloud.

## What it is
- Static website, no server; Python engine runs in the browser via Pyodide (~12 MB first load). [seen]
- Built by a student team for the "Introduction to Programming Languages" course, as a prototype for Smart India Hackathon problem SIH26134 (skill programs vs industry demand; Maharashtra skills dept sponsor per a third-party catalogue, unconfirmed). [desk]
- Faculty demo and viva expected; each teammate explains their own code. [desk]
- Two built-in datasets: 2,216 SYNTHETIC postings (12 Maharashtra districts, 2024-Q4 to 2026-Q3) and 19,194 REAL Indian postings (Fliar Research, Jan-Jun 2026, CC BY-NC 4.0, 6% company sample, almost no trade jobs). [seen]
- 10 illustrative training programs (none is a real named institute). [seen]
- Seven tabs: Market pulse, Programs, Gap matrix, Check a syllabus, For learners, Your data, How it works. [seen]
- English only in the UI; the skill reader understands some Marathi skill words; no Hindi UI. [seen]

## Context of likely users
- Faculty evaluating a programming course project: typically on a laptop/projector, 10-15 minutes per team. [guess]
- SIH-style judges: 5-10 minutes per team, scan for problem fit, impact, novelty, demo working live. [guess]
- Training providers (ITI principals, private institute heads, NGO skilling coordinators): mostly use phones and WhatsApp; office desktop available at ITIs. [guess]
- Learners (ITI trainees, diploma/BCom/BA graduates): phone-first, often Android with limited data; many more comfortable in Hindi/Marathi than English. [guess]

## UNKNOWN
Actual course rubric and weightage; whether the demo is on projector or the faculty's own laptop; who the faculty is; real device and network of target users; whether any real provider has seen the site.

## Not tested
No real user has used the site yet (n real = 0). Everything in this review is simulated and is a ranking, not a level.
