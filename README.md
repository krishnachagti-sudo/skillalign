# SkillAlign

Checks whether a skill development program teaches what job postings ask for, and says what to add, expand or cut. Built for Smart India Hackathon problem SIH26134 as an Introduction to Programming Languages course project.

The engine is plain Python (standard library only). The website runs that same Python inside the visitor's browser with Pyodide, so it is a static site with no server.

## Layout

| Path | What it is |
|---|---|
| `engine/` | The Python engine: taxonomy, dataset, demand, alignment, learner, api |
| `data/skills.json` | 57 skills, 248 phrases |
| `data/programs.json` | 10 illustrative training programs |
| `data/job_postings.csv` | 1,946 SYNTHETIC postings (made by `tools/generate_sample_data.py`) |
| `site/` | The web page (HTML, CSS, JS) |
| `tests/` | 20 pytest tests |
| `build.py` | Builds the publishable `dist/` folder |
| `docs/sources.md` | Verified facts and links used in the report |

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest -q          # 20 tests
python3 build.py                        # writes dist/
python3 -m http.server 3025 --directory dist
```

Open http://localhost:3025. The first load downloads Python (about 10 seconds), then everything is instant.

Regenerate the sample postings: `python3 tools/generate_sample_data.py`.

## Publish on a Conyso subdomain

`dist/` is the whole site. To serve it at, say, `skillalign.conyso.com` with GitHub Pages:

1. Create a new GitHub repo and push the contents of `dist/` to it.
2. Add a file named `CNAME` containing `skillalign.conyso.com`.
3. In the repo's Settings > Pages, serve from the main branch root.
4. At the DNS provider for conyso.com, add a CNAME record: `skillalign` pointing to `<github-username>.github.io`.

Run `python3 build.py` again after any change; every file URL carries a content hash, so visitors never get a mix of old and new files.

## Upload format

CSV with `title`, `description`, `date` (YYYY-MM-DD), and optionally `sector`, `city`. Bad rows are skipped and listed.
