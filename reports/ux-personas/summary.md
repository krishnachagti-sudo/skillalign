# SkillAlign UX persona review (round 1, 2026-11-13)

**Label:** Simulated. n real = 0, so every number here is a ranking, not a measurement. Two models (claude-opus, claude-sonnet) interviewed the same 13 personas separately. Model rank agreement rho = 0.71. Every persona rejected the decoy page (decoy/main ratio 0.28). Wording spread ≤ 8 points. The Hinglish answers moved by 0-2 points. The 5 frozen holdout cards are kept back to score the redesign. Usability agents miss most real failure points (CHI 2026: 3 of 10 without context), so this run is screening only. The real check is 3-5 people doing three tasks while thinking aloud.

## Ranking of sections (both models agree)
Programs > Check a syllabus > Market pulse > For learners > Your data > Gap matrix > How it works.
When told to keep only three sections, most personas kept Programs, Check a syllabus and Market pulse. Gap matrix was kept by 1 of 26 interviews.

## Likelihood (0-10, ranking only)
The lowest scores came from learners (mean 2.3). Next were faculty (3.3) and providers (3.8), then judges (4.1). Two phone learners and the computer-centre owner gave 0-1. The private institute head (laptop, English, has syllabi) gave the highest score, 7. The site works for people who already think like its builders.

## Problems, ranked by how many of the 26 interviews hit them
1. **The phone tab row is cut off after "Gap matrix"/"Check…", with no cue (11).** Learners never found "For learners", and providers never found "Check a syllabus". The fade exists but is too faint.
2. **Results open off-screen (11).** The program report opens below a 10-row table, the trend card at the page bottom, and the syllabus result below the form. People tapped, saw nothing change, and thought the site was broken.
3. **Example programs were read as real or as the persona's own course (9).** "Data Entry Operator 74 Partial borderline" was read as "my course got 74 marks". This made 2 learners quit.
4. **The 12 MB first load leaves dead air (13).** Faculty, judges and phone users all named it. One prepaid-data learner nearly quit.
5. **Numbers were misread (each 2-6):**
   - NEXT YEAR "34 ↓" was read as "jobs or placements falling".
   - Grey change figures (significance shown only on hover) were read as "small".
   - "given 15 h" did not match the 30 hrs typed (the module is split across two skills).
   - "0% (at most 5%)" confused people.
   - "100% of hours on core skills" next to a Weak 43 looked like a bug.
   - "latest four quarters" is shown on 2-quarter real data.
   - "Synthetic" was read as "the site is fake".
6. **There are too many recommendations, in an unclear order.** One course gets 13 ADD tags, and Python at 59% is listed after Cloud at 45%.
7. **The gap matrix does not work on a phone (2 columns, no drag cue) or on a projector (rotated tiny labels) (6).**
8. **There is no take-away (5).** Market pulse cannot be downloaded, and a .md report is not a file a boss or funder can open.
9. **Real data leads to dead ends (4).** 5 of 10 programs are unscored, and the learner gets "None of the listed programs…" with no next step.
10. **Faculty-specific asks:** show who built which part (viva); show the formula so the score can be rebuilt by hand.

## Correctness bugs found (fixed in the engine, 2 tests added; not committed yet)
- "Electrician (ITI trade) covers Machine Learning". Cause: the synonym "transformers" was mapped to ML. It now counts only as a skills-list item, and electrical motors/transformers phrases map to Electric Motors & Transformers.
- "Learn next: Generative AI Tools (29%)" was picked over Data Analysis (75%). Cause: priority boosted skills by growth even when the growth was not significant, with no cap. Now only significant growth counts, and the boost is capped at 2x. This also fixes the order of ADD recommendations.
- Trend card read "95% range ." because the forecast range was not passed to the page.
- The learner score was given from 7 postings with no warning. The API now returns a `low_data` flag; the UI still needs to show it.
- "safety" alone was not recognised. It now maps to Workplace Safety.
- Reduce wording now says "almost no postings ask for it (under 1%…)" instead of "only 0%".

## Redesign directions shown to Krishna
A Journeys (ask who you are, one guided flow each) · B One story (answer first, one picture, one big button) · C Workbench (dense analyst view, details in a drawer).
All three include the shared fixes:
- a page that shows content instantly while Python loads behind it
- an "Example course" label and plain-language scores
- results that open in place
- the top 3 recommendations, with "see all"
- a printable one-page report

## Not done
No real users have tried the site. The holdout scoring is waiting for the chosen redesign. The UI does not yet show the learner `low_data` flag or the hours split.

# Round 2: the "Journeys" redesign (2026-11-13)

**Label:** Simulated, n real = 0.
- **Dev panel:** the same 13 personas rated v2 fresh (Opus).
- **Frozen holdout:** the 5 personas held back from round 1 rated v1 and then v2 (Sonnet).

**Likelihood (Q5 wording 1, 0-10).** Shrunk lift (Layer A-lift) P50 +0.74 (P10 +0.61, P90 +0.90), which clears the 0.5 "clear difference" bar.

| Group | v1 | v2 |
|---|---|---|
| Faculty | 4.7 | 5.7 |
| Judges | 5.7 | 5.3 |
| Learners | 1.7 | 3.3 |
| Providers | 3.8 | 4.2 |
| Holdout | 3.6 | 6.6 |

The holdout gain is probably inflated: those personas saw v1 just before v2, so v2 was judged by contrast. The dev panel judged v2 fresh. Holdout up as well as dev means no sign of overfitting to the dev panel.

**What the redesign fixed** (no longer raised): the hidden tabs, results opening off-screen, dead air while loading, the 13-item recommendation list, the gap matrix on phones, the "next year ↓" misread, and the hours split.

**Still raised in v2** (personas out of 13, Opus):
- 9: practice data still not obvious enough. After this round, the home headline says "made-up" and offers "use real ads".
- 5: English only.
- 4: stats wording. "95% range" became "likely", and "borderline" is now explained.
- 4: growth with no base. It now reads "from 2% to 5%".
- 4: next-year score distrusted. It is now called "a straight-line guess".
- 3: typing a syllabus on a phone.
- 2: no export for the skills list.
- Judges in particular want things a UI can't give: real trade-job data, a district-wise course view, and QP/NOS lookup.

**Not done:**
- Hindi/Marathi UI.
- A "who built what" section (needs the team's names).
- A smaller first download.
- Export of the skills list.
- District-wise course scores.
