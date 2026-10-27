import json
import os

import pytest

from engine import api
from engine.alignment import assess_program, grade
from engine.dataset import Posting, parse_postings, program_from_syllabus, quarter_of
from engine.demand import fit_line, trend_table
from engine.learner import assess_learner
from engine.taxonomy import SkillExtractor, load_taxonomy

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture(scope="module")
def skills():
    return load_taxonomy(os.path.join(DATA, "skills.json"))


@pytest.fixture(scope="module")
def extractor(skills):
    return SkillExtractor(skills)


def posting(title, quarter, skills):
    return Posting(title=title, description="", date="", quarter=quarter, skills=set(skills))


# --- extraction -------------------------------------------------------------

def test_synonyms_map_to_one_skill(extractor):
    assert extractor.extract("Needs AWS or Azure, and Google Cloud") == {"cloud"}


def test_java_does_not_match_javascript(extractor):
    assert extractor.extract("Strong JavaScript") == {"javascript"}
    assert extractor.extract("Core Java and JavaScript") == {"java", "javascript"}


def test_longest_phrase_wins(extractor):
    # "cloud security" must not also count as plain "cloud"
    assert extractor.extract("Experience in cloud security") == {"cloud_security"}


def test_case_and_punctuation(extractor):
    assert extractor.extract("PYTHON, sql; Power BI.") == {"python", "sql", "data_viz"}


def test_no_partial_words(extractor):
    assert extractor.extract("positive attitude, blissful") == set()


def test_evidence_lists_matched_phrases(extractor):
    found = extractor.extract_with_evidence("MySQL and PostgreSQL")
    assert found == {"sql": ["MySQL", "PostgreSQL"]}


def test_every_synonym_belongs_to_one_skill(skills):
    seen = {}
    for s in skills.values():
        for syn in s.synonyms:
            assert syn not in seen, f"{syn} in {seen.get(syn)} and {s.id}"
            seen[syn] = s.id


# --- parsing ----------------------------------------------------------------

def test_quarter_of():
    assert quarter_of("2025-01-31") == "2025-Q1"
    assert quarter_of("2025-12-01") == "2025-Q4"
    with pytest.raises(ValueError):
        quarter_of("31/01/2025")


def test_parse_reports_bad_rows(extractor):
    csv_text = "Title,Description,Date\nData Analyst,SQL and Excel,2025-02-10\nX,,2025-02-10\nY,python,yesterday\n"
    postings, problems = parse_postings(csv_text, extractor)
    assert len(postings) == 1 and postings[0].skills == {"sql", "excel"}
    assert len(problems) == 2


def test_parse_rejects_missing_columns(extractor):
    with pytest.raises(ValueError, match="date"):
        parse_postings("title,description\na,b\n", extractor)


def test_syllabus_hours(extractor):
    program = program_from_syllabus("X", ["data analyst"], "Advanced Excel (40 hrs)\nSQL basics - 20h\nPython", extractor)
    assert [m.hours for m in program.modules] == [40, 20, 10]
    assert program.skills() == {"excel", "sql", "python"}


# --- demand -----------------------------------------------------------------

def test_fit_line_exact():
    slope, intercept = fit_line([0, 1, 2, 3], [1, 3, 5, 7])
    assert slope == pytest.approx(2) and intercept == pytest.approx(1)


def test_trend_growth_and_forecast():
    quarters = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"]
    postings = []
    for i, q in enumerate(quarters):
        # 10 postings per quarter; "genai" appears in i of them
        postings += [posting("Data Analyst", q, ["genai"] if k < i else ["sql"]) for k in range(10)]
    table = trend_table(postings)
    genai = table["genai"]
    assert genai["previous"] == pytest.approx((0 + 1 + 2 + 3) / 40)
    assert genai["share"] == pytest.approx((4 + 5 + 6 + 7) / 40)
    assert genai["growth"] == pytest.approx((0.55 - 0.15) / 0.15)
    assert genai["slope"] == pytest.approx(0.1)
    assert genai["forecast"] == pytest.approx(1.0)  # 0.7 + 4 * 0.1 = 1.1, capped at 100%


# --- alignment --------------------------------------------------------------

def test_alignment_score_is_share_weighted(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "excel"]) for _ in range(6)]
    postings += [posting("Data Analyst", "2026-Q1", ["sql"]) for _ in range(4)]
    program = program_from_syllabus("P", ["data analyst"], "SQL (30 hrs)\nTyping speed (30 hrs)", extractor)
    report = assess_program(program, postings, skills)
    # core: sql 100%, excel 60%. Teaches sql only -> 1.0 / 1.6
    assert report["score"] == pytest.approx(62.5)
    assert report["hours_on_demand_pct"] == pytest.approx(50.0)
    actions = {(r["action"], r["id"]) for r in report["recommendations"]}
    assert ("Add", "excel") in actions and ("Reduce", "typing") in actions


def test_program_with_no_matching_postings(extractor, skills):
    program = program_from_syllabus("P", ["astronaut"], "Python", extractor)
    report = assess_program(program, [posting("Data Analyst", "2026-Q1", ["sql"])], skills)
    assert report["score"] == 0 and report["warning"]


def test_grades():
    assert (grade(80), grade(60), grade(10)) == ("Strong", "Partial", "Weak")


# --- learner ----------------------------------------------------------------

def test_learner_readiness_and_program_pick(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "excel", "python"]) for _ in range(10)]
    programs = [program_from_syllabus("Has Python", ["data analyst"], "Python", extractor),
                program_from_syllabus("Has Typing", ["data analyst"], "Typing", extractor)]
    report = assess_learner({"sql", "excel"}, ["data analyst"], postings, programs, skills)
    assert report["readiness"] == pytest.approx(66.7, abs=0.1)
    assert report["next_skill"]["id"] == "python"
    assert [p["name"] for p in report["programs"]] == ["Has Python"]


# --- api on the sample data ------------------------------------------------

def test_api_round_trip():
    meta = json.loads(api.init(DATA))
    assert meta["postings"] > 1000 and meta["problem_count"] == 0
    summary = json.loads(api.programs_summary())
    assert len(summary) == len(meta["programs"])
    assert all(0 <= r["score"] <= 100 for r in summary)
    report = json.loads(api.program_report("automotive"))
    assert report["recommendations"][0]["id"] == "ev_maint"
    learner = json.loads(api.learner("data analyst", '["excel"]', "I know SQL"))
    assert "SQL & Databases" in learner["have"]
    uploaded = json.loads(api.load_uploaded("title,description,date\nData Analyst,SQL,2026-01-02\n"))
    assert uploaded["postings"] == 1 and uploaded["source"] == "uploaded"
    assert json.loads(api.use_sample())["source"] == "sample"


def test_thin_coverage_gets_expand(extractor, skills):
    postings = [posting("EV Service Technician", "2026-Q1", ["ev_maint", "safety"]) for _ in range(10)]
    program = program_from_syllabus("P", ["ev service"], "Workplace safety (190 hrs)\nIntro to EV servicing (5 hrs)", extractor)
    report = assess_program(program, postings, skills)
    assert report["score"] == 100  # both skills are taught...
    assert [r["id"] for r in report["recommendations"] if r["action"] == "Expand"] == ["ev_maint"]  # ...but EV barely


def test_learner_prefers_program_built_for_the_job(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "python", "excel"]) for _ in range(10)]
    programs = [program_from_syllabus("Other job, more overlap", ["software developer"], "SQL\nPython\nExcel", extractor),
                program_from_syllabus("Built for it", ["data analyst"], "SQL", extractor)]
    report = assess_learner(set(), ["data analyst"], postings, programs, skills)
    assert [p["name"] for p in report["programs"]] == ["Built for it", "Other job, more overlap"]
