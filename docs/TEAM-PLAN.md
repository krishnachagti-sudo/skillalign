# Team plan: who builds what

The course asks for a GitHub repo with contributions from every team member, and a viva where each person explains their own code. So every teammate takes one real piece below, builds it on their own branch from their own GitHub account, and opens a pull request. Each piece is sized at roughly 6-12 hours and touches different files, so the pieces never block each other.

Fill in the owner column, then open one GitHub issue per piece (there is a template in `CONTRIBUTING.md`).

| # | Piece | Owner | Main files | Language skill shown |
|---|---|---|---|---|
| 0 | Engine, scoring method, first site, persona review (done) | Krishna | `engine/`, `site/`, `tools/`, `reports/` | Python, JS |
| 1 | Real user testing: 5 think-aloud sessions | _teammate_ | `reports/user-tests/` | research method |
| 2 | Hindi and Marathi interface | _teammate_ | `site/i18n.js`, `site/app.js`, `site/index.html` | JS, data structures |
| 3 | District view of course scores | _teammate_ | `engine/api.py`, `engine/alignment.py`, `tests/`, `site/app.js` | Python, testing |
| 4 | Lighter first visit and skill-list export | _teammate_ | `build.py`, `site/app.js` | Python build step, JS |
| 5 | Team and credits page | _teammate_ | `site/index.html`, `docs/` | HTML, writing |

## 1. Real user testing (the most valuable piece)
Every finding so far comes from simulated personas, so it ranks problems but cannot measure them. This piece replaces guesses with evidence.
- Recruit 5 people: 2 classmates outside the team, 1 ITI or diploma student, 1 trainer or placement officer, 1 faculty member or TA.
- Each person does three tasks on a phone while thinking aloud: "check this course", "find what to learn for job X", "find the most asked skill". Record time taken, where they got stuck, and quotes. Ask for consent first, and keep no names in the repo.
- Write `reports/user-tests/findings.md`: per task, how many succeeded, the problems in their words, and which simulated findings in `reports/ux-personas/summary.md` held up or did not.
- **Done when** 5 sessions are written up and each problem is linked to a GitHub issue.
- **Viva:** why 5 users, what think-aloud means, which persona predictions were wrong.

## 2. Hindi and Marathi interface
Five of the 13 simulated users asked for it, and many learners read Hindi or Marathi best.
- Move every visible English string in `index.html` and `app.js` into a dictionary in `site/i18n.js`: `{en: {...}, hi: {...}, mr: {...}}`.
- Add a language switch next to the data pill, and remember the choice in `localStorage`.
- Keep skill names in English. They match job ads, which are in English.
- **Done when** all three journeys are fully readable in Hindi and Marathi, there is no missing key in any language (add a small check script), and screenshots are in the PR.
- **Viva:** how the lookup works, what happens to a missing key, why skill names stay English.

## 3. District view of course scores
The simulated skill-department official's main question was "which ITI courses need changing, district-wise".
- Add `api.program_by_district(program_id)`. It scores one course separately in each district with at least 30 matching job ads, reusing `assess_program`.
- Show it as a small table in the course report: district, score, its range, and the top missing skill.
- Write tests: a district with fewer than 30 ads is not scored, and the scores match `assess_program` run on that district's ads.
- **Done when** the tests pass and the table shows on the practice data.
- **Viva:** why 30 ads, what the bootstrap range means, how the test checks the result.

## 4. Lighter first visit and skill-list export
The first visit downloads about 12 MB, and the placement officer could not export the skills list.
- In `build.py`, run the engine once at build time to save the home page facts and the market's top skills as `snapshot.json`, so those pages show real numbers before Python loads.
- Add a "Download as CSV" button to "Skills employers ask for most", with columns skill, share, low, high, change.
- **Done when** the home and market numbers appear without waiting for the engine (check with the network throttled to "Slow 4G"), and the CSV opens in Excel.
- **Viva:** what changes between build time and run time, and how the CSV is built in the browser.

## 5. Team and credits page
Faculty want to know whom to question about which part.
- Add a "Team" section to How it works, listing each member, their piece, and links to their pull requests.
- Add data credits (Fliar Research, CC BY-NC 4.0) and tool credits (Pyodide, IBM Plex).
- **Done when** every member is listed with a working link to their merged PR.

## Rules that keep this honest
- Everyone commits only their own work, from their own GitHub account. Nobody commits for anybody else.
- One branch per piece (`feat/<piece>`), one pull request, and one review by someone else before merging.
- Run `.venv/bin/python -m pytest -q` before every push. Krishna publishes with `./publish.sh` after merging.
