# Contributing

Pick a piece from `docs/TEAM-PLAN.md`. Each piece has an owner, and the owner writes and commits that piece.

## Setup (once)

```bash
git clone https://github.com/krishnachagti-sudo/skillalign.git
cd skillalign
git config user.name "Your Name"
git config user.email "<your GitHub no-reply email>"   # GitHub → Settings → Emails
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest -q
```

Use the no-reply email from your own GitHub settings. Commits made with another address do not show up as yours on GitHub.

## Each piece

```bash
git switch -c feat/<piece>          # e.g. feat/hindi-marathi
# ...work, commit small steps with clear messages...
.venv/bin/python -m pytest -q
python3 build.py && python3 -m http.server 3025 --directory dist   # check it in a browser
git push -u origin feat/<piece>
gh pr create --fill                 # or open the pull request on github.com
```

Someone else on the team reviews the pull request before it is merged. Never push to `main` directly. Only Krishna runs `./publish.sh`, after merging.

## Issue template

```
Piece: <number and name from docs/TEAM-PLAN.md>
Owner: @github-username
Done when: <copied from the plan>
```
