# Round 2 script: scoring the redesign

Same framing as `interview.md` (read it: the framing paragraph, the tasks by audience, and the output rules all apply). The site has been redesigned. v1 is described in `walkthrough.md` + `shots/`; v2 in `walkthrough-v2.md` + `shots-v2/`. Phone personas look at the phone shots.

For each persona, answer fresh in their voice:
Q2 (walkthrough, on the version(s) you are told to use): step by step as this person really would, quoting on-screen words, marking STUCK / MISREAD / SLOW / QUIT. Stop where they would stop.
Q4 (trust): which number or sentence would they not believe or misunderstand?
Q5 wording 1 and wording 2: exactly as in `interview.md`, 0-10.
Q7: the three changes that would most help, most important first.
Q8: Hindi/Marathi-first personas only, as in `interview.md`.

Output JSON objects with: {"id", "segment", "model", "version": "v1"|"v2", "q5_w1", "q5_w2", "problems": [...same shape as before...], "distrust": [...], "fixes": [...], "hinglish_q5"}.
