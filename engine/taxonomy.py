"""Skill taxonomy and skill extraction from free text.

A skill has one id, a display name, a category and a list of synonyms
(the different ways job postings and syllabi write the same skill).
Extraction turns any text - a job posting, a module outline, a resume -
into the set of skill ids it mentions.

How extraction works: the text is split into words (spaces, hyphens,
slashes and punctuation separate words; "+", "#" and "." stay inside a
word so "C++", "C#" and "Node.js" survive). At each word we look up the
longest run of up to N words that is a known synonym, in a dictionary,
then jump past it. Dictionary lookups are fast, and "cloud security" is
found before "cloud" because longer runs are tried first.

Synonym rules (in skills.json):
- matching ignores case, except synonyms written with a leading "=",
  which must appear exactly as written or in capitals ("=Excel" matches
  "Excel" and "EXCEL" but not the verb "excel");
- spaces, hyphens and slashes are interchangeable ("rest api" = "REST-API");
- a plural "s" / "es" on the last word is accepted ("test case(s)");
- Marathi words may carry a case ending ("सेवांचा" still finds "सेवा");
- a skill right after "no", "not", "without", "except", "excluding" or
  "nor" (up to two words later, same clause) is not counted;
- synonyms written with a leading "~" only count inside a skills LIST
  (a "Python|SQL|C" column from a job board), where a bare "C" or "R" can
  only mean the language. In a list, "=" synonyms also ignore case,
  because "excel" in a list of skills can only mean Excel.
"""

import json
import re
import unicodedata
from dataclasses import dataclass

INVISIBLE = dict.fromkeys(map(ord, "​‌‍⁠﻿­"))
WORD = re.compile(r"[^\s\-–—,;:()\[\]{}\"'!?/|•<>=*]+")
NEGATORS = {"no", "not", "without", "except", "excluding", "nor"}
CLAUSE_BREAK = re.compile(r"[.;:!?\n]")
DEVANAGARI = re.compile(r"[ऀ-ॿ]")


@dataclass(frozen=True)
class Skill:
    id: str
    name: str
    category: str
    synonyms: tuple


def load_taxonomy(path):
    """Read skills.json and return {skill_id: Skill}."""
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    skills = {}
    for row in rows:
        if row["id"] in skills:
            raise ValueError(f"duplicate skill id: {row['id']}")
        skills[row["id"]] = Skill(row["id"], row["name"], row["category"], tuple(row["synonyms"]))
    return skills


def clean_text(text):
    """Normalise pasted text: unify look-alike characters, drop invisible ones."""
    return unicodedata.normalize("NFKC", text or "").translate(INVISIBLE)


def fold(word):
    """Case-insensitive form of a word ('İnventory' -> 'inventory')."""
    return word.lower().replace("̇", "")


def words_of(text):
    """[(word, start, end)] with trailing full stops trimmed ('Python.' -> 'Python')."""
    out = []
    for m in WORD.finditer(text):
        word, start, end = m.group(0), m.start(), m.end()
        while word.endswith(".") and len(word) > 1:
            word, end = word[:-1], end - 1
        out.append((word, start, end))
    return out


class SkillExtractor:
    """Finds taxonomy skills inside text with a longest-match dictionary scan."""

    def __init__(self, skills):
        self.skills = skills
        self.lookup = {}   # tuple of folded words -> (skill id, exact forms or None, list only?)
        self.longest = 1
        for skill in skills.values():
            for synonym in skill.synonyms:
                list_only = synonym.startswith("~")
                exact = synonym.startswith("=")
                parts = [w for w, _, _ in words_of(clean_text(synonym.lstrip("=~")))]
                key = tuple(fold(w) for w in parts)
                owner = self.lookup.get(key)
                if owner and owner[0] != skill.id:
                    raise ValueError(f"synonym '{synonym}' used by {owner[0]} and {skill.id}")
                if owner and not owner[2] and list_only:
                    continue  # the same words already count everywhere
                if exact:
                    forms = {" ".join(parts), " ".join(parts).upper()}
                    if owner and owner[1] is None:
                        continue  # a case-insensitive synonym for the same words already exists
                    if owner:
                        forms |= owner[1]
                    self.lookup[key] = (skill.id, forms, False)
                else:
                    self.lookup[key] = (skill.id, None, list_only)
                self.longest = max(self.longest, len(key))

    def _candidates(self, folded_last):
        """Spellings of the last word to try: as written, without a plural,
        and for Marathi without a case ending."""
        yield folded_last
        if folded_last.endswith("es"):
            yield folded_last[:-2]
        if folded_last.endswith("s"):
            yield folded_last[:-1]
        if DEVANAGARI.search(folded_last):
            for cut in range(len(folded_last) - 1, 1, -1):
                yield folded_last[:cut]

    def _match_at(self, words, i, as_list=False):
        """Longest synonym starting at word i: (skill id, words used) or None."""
        for n in range(min(self.longest, len(words) - i), 0, -1):
            run = words[i:i + n]
            head = tuple(fold(w) for w, _, _ in run[:-1])
            for last in self._candidates(fold(run[-1][0])):
                entry = self.lookup.get(head + (last,))
                if not entry:
                    continue
                skill_id, forms, list_only = entry
                if list_only and not as_list:
                    continue
                if forms is not None and not as_list:
                    written = " ".join(w for w, _, _ in run)
                    stem = written[:len(written) - (len(fold(run[-1][0])) - len(last))]
                    if written not in forms and stem not in forms:
                        continue
                return skill_id, n
        return None

    def _negated(self, text, words, i):
        for j in range(max(0, i - 3), i):
            if fold(words[j][0]) in NEGATORS and not CLAUSE_BREAK.search(text, words[j][2], words[i][1]):
                return True
        return False

    def _matches(self, text, as_list=False):
        text = clean_text(text)
        words = words_of(text)
        i = 0
        while i < len(words):
            found = self._match_at(words, i, as_list)
            if not found:
                i += 1
                continue
            skill_id, n = found
            if as_list or not self._negated(text, words, i):
                yield skill_id, text[words[i][1]:words[i + n - 1][2]]
            i += n

    def extract(self, text, as_list=False):
        """Return the set of skill ids mentioned in text. as_list=True for a
        job board's skills list ("python|sql|excel"): see the module docstring."""
        return {skill_id for skill_id, _ in self._matches(text, as_list)}

    def extract_with_evidence(self, text):
        """Return {skill_id: [the exact phrases that matched]}."""
        found = {}
        for skill_id, phrase in self._matches(text):
            found.setdefault(skill_id, [])
            if phrase not in found[skill_id]:
                found[skill_id].append(phrase)
        return found

    def unrecognised(self, text):
        """Items in a list-like text (comma, semicolon or line separated)
        that contain no known skill - shown to the user so they know what
        the score could not see."""
        items = re.split(r"[,;\n•|]+|\band\b", clean_text(text))
        missed = []
        for item in items:
            item = re.sub(r"\(?\d[\d.,]*\s*(?:hours?|hrs?|h)\)?\.?$", "", item.strip(), flags=re.I)
            item = re.sub(r"^(?:unit|module|chapter|week|part)\s*[\divx]+\s*[:.)\-]\s*", "", item.strip(" .:-\t()"), flags=re.I)
            if 2 <= len(item) <= 60 and not self.extract(item) and item not in missed:
                missed.append(item)
        return missed
