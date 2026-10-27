# SkillAlign

Checks whether a skill development program teaches what job postings ask for, and says what to add, expand or cut. Built for Smart India Hackathon problem SIH26134 as an Introduction to Programming Languages course project.

The engine is plain Python (standard library only). The website runs that same Python inside the visitor's browser with Pyodide, so it is a static site with no server.

## Layout

| Path | What it is |
|---|---|
| `engine/` | The Python engine: taxonomy, dataset, demand, alignment, learner, api |
| `data/skills.json` | 100 skills, 718 phrases (incl. ITI trades, business skills and Marathi words) |
| `data/programs.json` | 10 illustrative training programs |
| `data/job_postings.csv` | 2,214 SYNTHETIC postings across 12 Maharashtra districts (made by `tools/generate_sample_data.py`) |
| `data/real_postings_india_2026.csv` | 19,390 REAL Indian postings, Jan-Jun 2026, from Fliar Research (CC BY-NC 4.0), made by `tools/import_fliar.py`; see `docs/DATA-SOURCES.md` |
| `tools/validate.py` | Runs the method on trend-free and trended synthetic data; writes `docs/validation.md` |
| `vendor/pyodide/` | Self-hosted Pyodide 0.28.3 core (MPL-2.0), so the site needs no CDN |
| `site/` | The web page (HTML, CSS, JS) |
| `tests/` | 51 pytest tests |
| `build.py` | Builds the publishable `dist/` folder |
| `docs/sources.md` | Verified facts and links used in the report |

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install pytest
.venv/bin/python -m pytest -q          # 51 tests
.venv/bin/python tools/validate.py      # fake-trend and stability checks
python3 build.py                        # writes dist/
python3 -m http.server 3025 --directory dist
```

Open http://localhost:3025. The first load fetches Python (about 12 MB); after that the site is cached and works offline.

Regenerate the sample postings: `python3 tools/generate_sample_data.py`. Re-import the real postings: download `job_postings_2026_sample.csv` from https://huggingface.co/datasets/fliarbi/job-postings-2026 and run `python3 tools/import_fliar.py <that file>`.

## Publish on a Conyso subdomain

For now the site is on GitHub Pages: commit, then run `./publish.sh` (it refuses to publish uncommitted changes). `dist/` is the whole site. To serve it at, say, `skillalign.conyso.com` with GitHub Pages:

1. Create a new GitHub repo and push the contents of `dist/` to it.
2. Add a file named `CNAME` containing `skillalign.conyso.com`.
3. In the repo's Settings > Pages, serve from the main branch root.
4. At the DNS provider for conyso.com, add a CNAME record: `skillalign` pointing to `<github-username>.github.io`.

Run `python3 build.py` again after any change; every file URL carries a content hash, so visitors never get a mix of old and new files.

## Upload format

CSV with `title`, `date` (2025-08-14, 14/08/2025 or an ISO timestamp), and `description` and/or `skills`; optionally `sector`, `district` (or `city`), `state`. Comma, semicolon, tab or pipe separated. Bad rows are skipped and listed; a file with no usable rows changes nothing.
