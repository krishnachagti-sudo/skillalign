# Interview script (identical for both models)

Read first, in this folder: `facts.md`, `walkthrough.md`, `decoy.md`, `cast/batch-1.md` (the 13 persona cards), and the screenshots in `shots/`. Look at the screenshots: phone personas see shots 12-14 and the phone notes in the walkthrough, not the desktop layout.

## Framing for every persona (do not change)
This is a research interview. Answer as the person described below would actually answer, including being busy, unsure, uninterested or wrong. Real people skim, misread numbers, skip explanations, give up on screens they do not understand, and do not read "How it works". If the card or the fact sheet does not tell you something, say you don't know rather than guessing. Do not say whose project this is or praise it to be polite. Answer one person at a time, in that person's own voice and vocabulary; every answer must be written fresh for that person (no templates, no copying between personas or between wordings).

Before answering Q2, quote the line of the card that most shapes how this person will use the site.

## Tasks by audience (Q2)
- faculty: "You have 10 minutes to decide how good this project's interface is and what to ask the team."
- judge: "You have 7 minutes with this site before scoring it."
- provider: "Check whether one of your own courses teaches what jobs ask for, and get something you could show your boss or funder."
- learner: "Find out what you should learn next to get the job you want."

## Questions
Q1 (past behaviour). The last time you had to judge a similar tool / project / website, or look up what skills a job needs: what did you actually do, and what made you trust it or give up?

Q2 (walkthrough). Doing your task, go through the site as you really would, step by step. For every step: what you click or read, the exact words on screen you are reacting to (quote them), and what you think it means. Mark each problem as STUCK (cannot go on), MISREAD (you understood something wrong — say what you thought and what is true), SLOW (got there but with effort), or QUIT. Stop where this person would stop.

Q3 (ranking). Wording 1: "Rank these sections by how useful they are to you, most useful first: For learners, Gap matrix, How it works, Check a syllabus, Your data, Market pulse, Programs."
Wording 2 (ask separately, and answer fresh): "If the site could keep only three sections, which three would you keep, best first? Options: Programs, Your data, Market pulse, For learners, Check a syllabus, How it works, Gap matrix."

Q4 (trust). Which number or sentence on the site would you not believe, or would you misunderstand? Quote it and say why.

Q5 (likelihood, 0-10, where 0 = no chance and 10 = certain).
- Wording 1: faculty/judge: "What is the chance you would rate this site's interface and user experience as good or better?" provider/learner: "What is the chance you would come back and use this site again in the next month?"
- Wording 2 (answer fresh, not by copying): faculty/judge: "Out of 10, how likely is it that this interface would get full marks for usability from you?" provider/learner: "How likely is it that you would send this link to someone else in your position?"

Q6 (decoy). Same as Q5 wording 1, but for the Programs page shown in `decoy.md` instead of the real one.

Q7 (fixes). The three changes that would most help you, in your own words, most important first.

Q8 (language check, only for personas whose card says Hindi or Marathi first). Redo Q2's last step and Q5 wording 1 as if the whole interview were in Hinglish (Roman-script Hindi-English mix). Report the Hinglish answer and whether the bottom line changed.

## Output
Write `round-1-<model>.md` in this folder (model = opus or sonnet): one section per persona with Q1-Q8 answers in full.
Then write `answers-<model>.json`: a JSON list, one object per persona:
{"id": "...", "segment": "...", "model": "<exact model name>",
 "q5_w1": 0-10, "q5_w2": 0-10, "q6_decoy": 0-10,
 "rank_w1": [7 section names in order], "keep3_w2": [3 names],
 "problems": [{"type": "STUCK|MISREAD|SLOW|QUIT", "where": "tab or element", "quote": "exact on-screen words", "what": "one line"}],
 "distrust": [{"quote": "...", "why": "..."}],
 "fixes": ["...", "...", "..."],
 "hinglish_q5": 0-10 or null, "hinglish_changed": true/false/null}
Do not read any other round-1 or answers file.
