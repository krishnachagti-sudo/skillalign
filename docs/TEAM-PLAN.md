# Team plan: bigger pieces for later

The current, small pieces (15-20 minutes each) are in `TEAM.md`. The pieces below are larger follow-ons for the final project; the owners listed are a first draft.

The course asks for a GitHub repo with contributions from every team member, and a viva where each person explains their own code. So every member takes one real piece below, builds it on their own branch from their own GitHub account, and opens a pull request. The pieces touch different files, so nobody waits for anybody. Names were assigned alphabetically as a first draft: swap freely, then update the issue.

| # | Piece | Owner | Main files | Size | Skill shown |
|---|---|---|---|---|---|
| 0 | Engine, scoring method, data cleaning, site, persona review and redesign (done) | Krishna | `engine/`, `tools/`, `site/`, `reports/` | done | Python, JS |
| 1 | Real user testing: 5 think-aloud sessions | Krishay | `reports/user-tests/` | 6-8 h | research method |
| 2 | Hindi interface | Mansha | `site/i18n.js`, `site/app.js`, `site/index.html` | 6-8 h | JS, data structures |
| 3 | Marathi interface (after #2's dictionary exists) | Navya | `site/i18n.js` | 4-6 h | JS, testing |
| 4 | District view of course scores | Priyanshu | `engine/api.py`, `tests/`, `site/app.js` | 8-10 h | Python, testing |
| 5 | Lighter first visit (build-time snapshot) | Sanskar | `build.py`, `site/app.js` | 6-8 h | Python build step |
| 6 | Skill-list CSV export | Vishal | `site/app.js`, `site/index.html` | 3-4 h | JS |
| 7 | Team and credits page | Yashraj | `site/index.html`, `docs/` | 3-4 h | HTML, writing |

## 1. Real user testing (the most valuable piece)
Every finding so far comes from simulated personas, so it ranks problems but cannot measure them. This piece replaces guesses with evidence.
- Recruit 5 people: 2 classmates outside the team, 1 ITI or diploma student, 1 trainer or placement officer, 1 faculty member or TA.
- Each person does three tasks on a phone while thinking aloud: "check this course", "find what to learn for job X", "find the most asked skill". Record time taken, where they got stuck, and quotes. Ask for consent first, and keep no names in the repo.
- Write `reports/user-tests/findings.md`: per task, how many succeeded, the problems in their words, and which simulated findings in `reports/ux-personas/summary.md` held up or did not.
- **Done when** 5 sessions are written up and each problem is linked to a GitHub issue.
- **Viva:** why 5 users, what think-aloud means, which persona predictions were wrong.

## 2. Hindi interface
Five of the 13 simulated users asked for their own language, and many learners read Hindi best.
- Move every visible English string in `index.html` and `app.js` into a dictionary in `site/i18n.js`: `{en: {...}, hi: {...}}`, with a `t(key)` lookup that falls back to English.
- Add a language switch next to the data pill, and remember the choice in `localStorage`.
- Keep skill names in English. They match job ads, which are in English.
- **Done when** all three journeys read fully in Hindi, and the PR has phone screenshots.
- **Viva:** how the lookup works, what happens to a missing key, why skill names stay English.

## 3. Marathi interface
Starts once #2's dictionary is merged. The sample data is Maharashtra, so Marathi matters for trainers and officials there.
- Add `mr: {...}` to `site/i18n.js` with every key `en` has, and add Marathi to the switch.
- Add `tools/check_i18n.py`: it fails if any language misses a key that `en` has. Add it as a test.
- **Done when** all three journeys read fully in Marathi and the check passes.
- **Viva:** how the check finds a missing key, and one translation choice you made.

## 4. District view of course scores
The simulated skill-department official's main question was "which ITI courses need changing, district-wise".
- Add `api.program_by_district(program_id)`. It scores one course separately in each district with at least 30 matching job ads, reusing `assess_program`.
- Show it as a small table in the course report: district, score, its range, and the top missing skill.
- Write tests: a district with fewer than 30 ads is not scored, and the scores match `assess_program` run on that district's ads.
- **Done when** the tests pass and the table shows on the practice data.
- **Viva:** why 30 ads, what the bootstrap range means, how the test checks the result.

## 5. Lighter first visit (build-time snapshot)
The first visit downloads about 12 MB before any numbers show.
- In `build.py`, run the engine once at build time and save the home facts and the market's top skills as `snapshot.json`.
- In `app.js`, draw those from the snapshot at once, then swap in live numbers when the engine is ready.
- **Done when** the home and market numbers appear without waiting for the engine (check with the network throttled to "Slow 4G").
- **Viva:** what runs at build time and what runs in the browser, and why that is safe here.

## 6. Skill-list CSV export
The simulated placement officer could not take the skills list away.
- Add a "Download as CSV" button to "Skills employers ask for most", with columns skill, share, low, high, change. Build the file in the browser (a Blob), and respect the current filters.
- **Done when** the file opens in Excel with correct numbers for two different filter settings.
- **Viva:** how the CSV is built, and how commas inside a skill name are handled.

## 7. Team and credits page
Faculty want to know whom to question about which part.
- Add a "Team" section to How it works, listing each member, their piece, and links to their pull requests.
- Add data credits (Fliar Research, CC BY-NC 4.0) and tool credits (Pyodide, IBM Plex).
- **Done when** every member is listed with a working link to their merged PR.

## Rules that keep this honest
- Everyone commits only their own work, from their own GitHub account. Nobody commits for anybody else.
- One branch per piece (`feat/<piece>`), one pull request, and one review by someone else before merging.
- Run `.venv/bin/python -m pytest -q` before every push. Krishna publishes with `./publish.sh` after merging.
