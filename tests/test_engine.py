import json
import math
import os

import pytest

from engine import api
from engine.alignment import assess_program, grade
from engine.dataset import Posting, parse_postings, parse_syllabus_line, program_from_syllabus, quarter_of
from engine.demand import (bonferroni_z, fit_line, role_family, sort_quarters, split_windows, trend_table,
                           wilson, within_role_growth)
from engine.learner import assess_learner
from engine.taxonomy import SkillExtractor, load_taxonomy

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
QUARTERS = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4", "2026-Q1", "2026-Q2", "2026-Q3", "2026-Q4"]


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
    assert extractor.extract("Experience in cloud security") == {"cloud_security"}


def test_case_punctuation_plural_hyphen(extractor):
    assert extractor.extract("PYTHON, sql; Power BI.") == {"python", "sql", "data_viz"}
    assert extractor.extract("REST-APIs and test cases") == {"rest_api", "testing"}
    assert extractor.extract("HTML/CSS/JavaScript, CI/CD") == {"html_css", "javascript", "devops"}


def test_symbols_inside_words(extractor):
    assert extractor.extract("C++, C# and .NET, Node.js") == {"cpp", "csharp", "nodejs"}
    assert extractor.extract("Programming in C and DBMS") == {"c_lang", "sql"}


@pytest.mark.parametrize("text", ["excel in a fast-paced role", "react quickly", "shipping containers",
                                  "car dashboards", "within 5s", "his software skills", "positive attitude"])
def test_ambiguous_words_are_not_skills(extractor, text):
    assert extractor.extract(text) == set()


def test_case_sensitive_synonyms(extractor):
    assert extractor.extract("Advanced Excel, EXCEL, Excels") == {"excel"}
    assert extractor.extract("5S and kaizen") == {"quality_control"}


def test_negation(extractor):
    assert extractor.extract("No Excel or SQL is covered") == set()
    assert extractor.extract("No experience needed. Must have SQL") == {"sql"}


def test_unicode_never_crashes(extractor):
    assert extractor.extract("İnventory management") == {"inventory"}
    assert extractor.extract("ſql") == {"sql"}
    assert extractor.extract("Py​thon and machine learning") == {"python", "ml"}


def test_trades_and_marathi(extractor):
    assert extractor.extract("plumbing, carpentry, tailoring, beautician, mobile repair") == \
        {"plumbing", "carpentry", "tailoring", "beauty", "mobile_repair"}
    assert extractor.extract("ग्राहक सेवांचा अनुभव, वायरिंग") == {"customer_service", "wiring"}
    assert extractor.extract("MS-CIT certificate") == {"digital_literacy"}


def test_evidence_and_unrecognised(extractor):
    assert extractor.extract_with_evidence("MySQL and PostgreSQL") == {"sql": ["MySQL", "PostgreSQL"]}
    assert extractor.unrecognised("C++, Express, Compiler Design (30 hrs)") == ["Express", "Compiler Design"]


def test_every_synonym_belongs_to_one_skill(skills):
    SkillExtractor(skills)  # raises on a clash


# --- parsing ----------------------------------------------------------------

def test_quarter_of_formats():
    assert quarter_of("2025-01-31") == "2025-Q1"
    assert quarter_of("31/12/2025") == "2025-Q4"
    assert quarter_of("2025/7/4") == "2025-Q3"
    for bad in ("0001-01-01", "2026-02-31", "2025-13-01", "2026-1", "yesterday", "10000-01-01"):
        with pytest.raises(ValueError):
            quarter_of(bad)


def test_parse_reports_bad_rows_and_reads_description_only(extractor):
    csv_text = ("Title,Description,Date\nSolar PV Technician,Wiring and PPE,2025-02-10\n"
                "X,,2025-02-10\nY,python,0999-01-01\n")
    postings, problems = parse_postings(csv_text, extractor)
    assert len(postings) == 1 and postings[0].skills == {"wiring", "safety"}  # no solar from the title
    assert len(problems) == 2


def test_skills_column_and_timestamps(extractor):
    csv_text = "title,posted_date,city,skills\nData Analyst,2026-01-05T10:00:00Z,Pune,Python|SQL|Power BI\n"
    postings, problems = parse_postings(csv_text, extractor)
    assert not problems and postings[0].skills == {"python", "sql", "data_viz"} and postings[0].quarter == "2026-Q1"


def test_parse_separators_aliases_and_errors(extractor):
    postings, _ = parse_postings("job_title;job_description;posted;city\nAnalyst;SQL;2025-01-02;Pune\n", extractor)
    assert postings[0].district == "Pune" and postings[0].skills == {"sql"}
    with pytest.raises(ValueError, match="date"):
        parse_postings("title,description\na,b\n", extractor)
    with pytest.raises(ValueError, match="twice"):
        parse_postings("title,title,description,date\na,b,c,2025-01-01\n", extractor)


@pytest.mark.parametrize("line,expected", [
    ("Advanced Excel (40 hrs)", ("Advanced Excel", 40.0, False)),
    ("SQL basics - 20h", ("SQL basics", 20.0, False)),
    ("Capstone (1,000 hrs)", ("Capstone", 1000.0, False)),
    ("SQL (.5 hrs)", ("SQL", 0.5, False)),
    ("Excel (40 Hrs.)", ("Excel", 40.0, False)),
    ("Python 3 (40 hrs)", ("Python 3", 40.0, False)),
    ("Soft skills (20 hrs) [mandatory]", ("Soft skills", 20.0, True)),
    ("Python", ("Python", 10.0, False)),
])
def test_syllabus_lines(line, expected):
    assert parse_syllabus_line(line) == expected


def test_syllabus_rejects_absurd_hours(extractor):
    with pytest.raises(ValueError):
        program_from_syllabus("X", ["data analyst"], "SQL (" + "9" * 400 + " hrs)", extractor)


# --- demand -----------------------------------------------------------------

def test_fit_line_exact():
    slope, intercept = fit_line([0, 1, 2, 3], [1, 3, 5, 7])
    assert slope == pytest.approx(2) and intercept == pytest.approx(1)


def test_quarters_sort_and_calendar_windows():
    assert sort_quarters(["2026-Q1", "2024-Q4", "2025-Q2"]) == ["2024-Q4", "2025-Q2", "2026-Q1"]
    postings = [posting("A", q, []) for q in ["2019-Q1", "2025-Q1", "2025-Q2"]]
    recent, previous = split_windows(postings)
    assert recent == ["2025-Q1", "2025-Q2"] and previous == []  # 2019 is not "last year"


def test_wilson_and_bonferroni():
    low, high = wilson(10, 100)
    assert low == pytest.approx(0.0552, abs=1e-3) and high == pytest.approx(0.1744, abs=1e-3)
    assert bonferroni_z(1) == pytest.approx(1.96, abs=0.01)
    assert bonferroni_z(60) > 3.2


def test_trend_growth_forecast_and_significance():
    postings = []
    for i, q in enumerate(QUARTERS):
        postings += [posting("Data Analyst", q, ["genai"] if k < 10 * i else ["sql"]) for k in range(100)]
    t = trend_table(postings)["genai"]
    assert t["previous"] == pytest.approx(0.15) and t["share"] == pytest.approx(0.55)
    assert t["growth"] == pytest.approx((0.55 - 0.15) / 0.15)
    assert t["slope"] == pytest.approx(0.1) and t["forecast"] == pytest.approx(1.0)
    assert t["significant"]


def test_brand_new_skill_is_new():
    postings = []
    for i, q in enumerate(QUARTERS):
        postings += [posting("Data Analyst", q, ["sql", "genai"] if i >= 4 and k < 50 else ["sql"])
                     for k in range(100)]
    t = trend_table(postings)["genai"]
    assert t["is_new"] and t["growth"] is None and t["significant"]


def test_role_mix_is_not_a_trend():
    # tally stays at 70% of accountant postings, but accountants go from half to a tenth of hiring
    before = [posting("Accountant", "2025-Q1", ["tally"] if k < 70 else []) for k in range(100)] + \
             [posting("Developer", "2025-Q1", []) for _ in range(100)]
    after = [posting("Accountant", "2026-Q1", ["tally"] if k < 14 else []) for k in range(20)] + \
            [posting("Developer", "2026-Q1", []) for _ in range(180)]
    assert within_role_growth(after, before)["tally"] == pytest.approx(0.0)


def test_role_family():
    assert role_family("Sr. Data Analyst (Fresher)") == "data analyst"
    assert role_family("Team Lead - Retail Sales Associate") == "retail sales associate"
    assert role_family("Lead Generation Executive") == "lead generation executive"


# --- alignment --------------------------------------------------------------

def test_alignment_is_share_and_hours_weighted(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "excel"]) for _ in range(60)]
    postings += [posting("Data Analyst", "2026-Q1", ["sql"]) for _ in range(40)]
    program = program_from_syllabus("P", ["data analyst"], "SQL (30 hrs)\nTyping speed (30 hrs)", extractor)
    report = assess_program(program, postings, skills)
    # core: sql 100%, excel 60%. SQL's fair hours = 60 x 1.0/1.6 = 37.5; 30 h >= half of that -> full credit
    assert report["score"] == pytest.approx(62.5)
    actions = {(r["action"], r["id"]) for r in report["recommendations"]}
    assert ("Add", "excel") in actions and ("Reduce", "typing") in actions
    assert report["score_low"] <= report["score"] <= report["score_high"]


def test_intro_modules_cannot_game_the_score(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "excel", "python"]) for _ in range(50)]
    honest = program_from_syllabus("H", ["data analyst"], "SQL (40 hrs)\nExcel (40 hrs)\nPython (40 hrs)", extractor)
    gamed = program_from_syllabus("G", ["data analyst"],
                                  "Intro to SQL (1 hrs)\nIntro to Excel (1 hrs)\nIntro to Python (1 hrs)\nYoga (500 hrs)",
                                  extractor)
    assert assess_program(honest, postings, skills)["score"] == 100
    gamed_report = assess_program(gamed, postings, skills)
    assert gamed_report["score"] < 5
    assert {r["action"] for r in gamed_report["recommendations"]} >= {"Expand"}


def test_mandatory_modules_are_never_cut(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql"]) for _ in range(50)]
    program = program_from_syllabus("P", ["data analyst"], "SQL (40 hrs)\nSpoken English (20 hrs) [mandatory]", extractor)
    assert not [r for r in assess_program(program, postings, skills)["recommendations"] if r["action"] == "Reduce"]


def test_program_with_no_matching_postings_is_unscored(extractor, skills):
    program = program_from_syllabus("P", ["astronaut"], "Python", extractor)
    report = assess_program(program, [posting("Data Analyst", "2026-Q1", ["sql"])], skills)
    assert report["grade"] == "Unscored" and report["recommendations"] == [] and report["warning"]


def test_unrecognised_hours_are_flagged(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql"]) for _ in range(50)]
    program = program_from_syllabus("P", ["data analyst"], "SQL (10 hrs)\nCompiler Design (30 hrs)", extractor)
    assert "matched no skill" in assess_program(program, postings, skills)["warning"]


def test_grades():
    assert (grade(80), grade(60), grade(10)) == ("Strong", "Partial", "Weak")


def test_short_roles_rejected(extractor, skills):
    program = program_from_syllabus("P", ["it"], "Python", extractor)
    with pytest.raises(ValueError):
        assess_program(program, [], skills)


# --- learner ----------------------------------------------------------------

def test_learner_readiness_and_program_pick(extractor, skills):
    postings = [posting("Data Analyst", "2026-Q1", ["sql", "excel", "python"]) for _ in range(10)]
    programs = [program_from_syllabus("Other job, more overlap", ["software developer"], "SQL\nPython\nExcel", extractor),
                program_from_syllabus("Built for it", ["data analyst"], "Python", extractor)]
    report = assess_learner({"sql", "excel"}, ["data analyst"], postings, programs, skills)
    assert report["readiness"] == pytest.approx(66.7, abs=0.1)
    assert report["next_skill"]["id"] == "python"
    assert [p["name"] for p in report["programs"]] == ["Built for it", "Other job, more overlap"]
    with pytest.raises(ValueError):
        assess_learner(set(), [""], postings, programs, skills)


# --- api on the sample data ------------------------------------------------

def test_api_round_trip():
    meta = json.loads(api.init(DATA))
    assert meta["postings"] > 1000 and meta["problem_count"] == 0 and "Pune" in meta["districts"]
    summary = json.loads(api.programs_summary())
    assert len(summary) == len(meta["programs"]) and all(0 <= r["score"] <= 100 for r in summary)
    adds = [r["id"] for r in json.loads(api.program_report("automotive"))["recommendations"] if r["action"] == "Add"]
    assert {"ev_maint", "bms"} <= set(adds[:3])
    healthcare = json.loads(api.overview("Healthcare"))
    assert healthcare["postings"] < meta["postings"]
    learner = json.loads(api.learner("data analyst", "not json", "I know SQL, Compiler Design"))
    assert "SQL & Databases" in learner["have"] and "Compiler Design" in learner["unrecognised"]
    uploaded = json.loads(api.load_uploaded("title,description,date\nData Analyst,SQL,2026-01-02\n"))
    assert uploaded["postings"] == 1 and uploaded["source"] == "uploaded"
    assert json.loads(api.use_sample())["source"] == "sample"


def test_failed_upload_keeps_old_data():
    api.init(DATA)
    before = json.loads(api.meta())["postings"]
    with pytest.raises(ValueError):
        api.load_uploaded("title,description,date\nA,b,not a date\n")
    assert json.loads(api.meta())["postings"] == before


def test_json_never_contains_nan():
    api.init(DATA)
    for text in (api.overview(), api.programs_summary(), api.matrix()):
        assert "NaN" not in text and "Infinity" not in text
        json.loads(text)
    assert not math.isnan(json.loads(api.overview())["avg_alignment"])
