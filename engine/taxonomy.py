"""Skill taxonomy and skill extraction from free text.

A skill has one id, a display name, a category and a list of synonyms
(the different ways job postings and syllabi write the same skill).
Extraction turns any text - a job posting, a module outline, a resume -
into the set of skill ids it mentions.
"""

import json
import re
from dataclasses import dataclass


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
        skills[row["id"]] = Skill(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            synonyms=tuple(s.lower() for s in row["synonyms"]),
        )
    return skills


class SkillExtractor:
    """Finds taxonomy skills inside text.

    All synonyms go into one regular expression, longest first. A regex
    alternation tries options left to right, so "cloud security" wins
    over "cloud" when both could match at the same spot, and each piece
    of text is counted for one skill only.
    """

    def __init__(self, skills):
        self.skills = skills
        self.lookup = {}  # synonym -> skill id
        for skill in skills.values():
            for synonym in skill.synonyms:
                owner = self.lookup.get(synonym)
                if owner is not None and owner != skill.id:
                    raise ValueError(f"synonym '{synonym}' used by {owner} and {skill.id}")
                self.lookup[synonym] = skill.id

        ordered = sorted(self.lookup, key=len, reverse=True)
        alternatives = "|".join(re.escape(s) for s in ordered)
        # (?<![\w+]) and (?![\w+]) act like word boundaries that also
        # treat "+" as part of a word, so "java" never matches "javascript".
        self.pattern = re.compile(rf"(?<![\w+])(?:{alternatives})(?![\w+])", re.IGNORECASE)

    def extract(self, text):
        """Return the set of skill ids mentioned in text."""
        if not text:
            return set()
        return {self.lookup[m.group(0).lower()] for m in self.pattern.finditer(text)}

    def extract_with_evidence(self, text):
        """Return {skill_id: [the exact phrases that matched]}."""
        found = {}
        for m in self.pattern.finditer(text or ""):
            skill_id = self.lookup[m.group(0).lower()]
            found.setdefault(skill_id, [])
            if m.group(0) not in found[skill_id]:
                found[skill_id].append(m.group(0))
        return found
