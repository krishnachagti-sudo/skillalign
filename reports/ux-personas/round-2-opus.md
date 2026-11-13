# Round 2 (v2 "Journeys" redesign) — model: opus

Simulated persona interviews, v2 only (`walkthrough-v2.md`, `shots-v2/`). Phone personas used shots 04-09; laptop and projector personas used shots 01-03. Everything here is simulated screening (n real = 0). Where the materials do not show what a screen would say (for example the "Learn next" result for a job other than data analyst), the persona says they don't know rather than inventing it.

Device per card: phone = fac-external, judge-nsdc-pm (first pass), learn-sceptic-switcher, learn-iti-trainee, prov-sceptic-owner, prov-ngo-coord. Laptop/projector = the rest. prov-private-head's card names no device; he says he'd use the office laptop, which is his own guess.

---

## 1. fac-hod-sceptic (faculty, laptop)

Card line that shapes use: *"Asks 'where is the real data, who would use this, what did YOU write'."*

**Q2 — walkthrough (10 minutes, what to ask the team)**
1. Opens home. Reads "Do skill courses teach what jobs ask for?" then "On the practice data, **6 of 10 example courses** miss skills that their own jobs ask for." — *"Practice data. Example courses. So the headline claim is about invented courses scored against invented ads. That's the first question for the viva."* MISREAD avoided only because he reads the word "practice" with suspicion; he takes it to mean "test data", which is right.
2. Clicks the orange "Practice data ▾". Reads "These 2,216 job ads are made up, to show how SkillAlign works, so the numbers are not facts about real jobs." — *"At least they admit it. Good. Now where's the real one."* Sees "Switch to real job ads". Switches. Doesn't know what the real set is; nothing in the pill tells him who collected it. SLOW: he has to go to How it works to find the source.
3. Clicks "Check my course", leaves the pre-filled data analyst syllabus, presses "Check this course". Reads "51/100" and "Likely between 49 and 53 (that range crosses a grade line, so the grade is borderline)." — *"Fine, they computed an interval. On what? I'd ask them to explain it, not read it."*
4. Reads "16 h would earn full credit". — *"Who decided 16 hours is full credit? That's a rule someone wrote. Which of them wrote it?"* MISREAD-risk he flags as a viva question, not a bug.
5. Scrolls the footer: "SkillAlign is a student prototype for Smart India Hackathon problem SIH26134 … Built in Python, run in the browser with Pyodide. … Source code". Looks for a team page. There is none. STUCK on "what did YOU write": the site gives no answer, he will have to ask in person.
6. Stops. Has his list of questions.

**Q4 — trust**
- "6 of 10 example courses miss skills that their own jobs ask for" — it's the biggest sentence on the page and it's about made-up courses on made-up ads. He would not accept it as a finding.
- "about 43 next year, because the jobs are changing" — a forecast from synthetic data is decoration.

**Q5** — Wording 1 (rate UI/UX good or better): **4**. "It's cleaner than most I see, I'll give them that, but clean is cheap now." Wording 2 (full marks for usability): **2**.

**Q7 — fixes**
1. Open on the real job ads, and put the source and sample size of that data where the claim is.
2. A "who built what" section, module by module, so each student can be held to their part.
3. Show the rule behind "full credit" hours on the report itself, not in a separate page.

---

## 2. fac-ta-phd (faculty, projected screen in a lab)

Card line: *"Cares whether the demo story is clear in 5 minutes and whether numbers on screen are explained."*

**Q2 — walkthrough (from the projector)**
1. Home is projected. "What do you want to do?" with three cards. — *"OK, that's a story in one screen: course, learner, market. Good."* The three small facts under it ("Asked for most … in 23% of job ads", "up 213% on last year", "2,216 Practice data") are small grey text; from the back of a lab they're unreadable. SLOW.
2. Team clicks "Job market" → "Example courses". Desktop table: "COVERS WHAT ITS JOBS ASK FOR · SCORE · NEXT YEAR IF UNCHANGED". Junior Software Developer "43 Weak", "34 ↓". — *"Units: score out of 100, fine. 'Next year if unchanged' — a forecast; is it the point estimate? I'll check."*
3. Row opens inline: "Likely between 40 and 46. If the course stays the same, about 34 next year". — *"So there's a range on the current score but none on next year's. Inconsistent."* MISREAD-risk: she first reads 34 as having the same interval.
4. "It misses 13 of 20 skills that 15% or more of these job ads ask for." Then she glances at the Gaps tab, where the same course shows only "Python 59%, Cloud Computing 45%". MISREAD: thinks the two pages disagree (13 vs 2). True: the Gaps list probably shows only fully missing core skills while the report also counts skills taught with too few hours, but nothing on screen says so.
5. Opens How it works: "score = 100 × Σ(share × credit) ÷ Σ share, over skills in 15% or more of ads". — *"Good, that's what I wanted. What's 'credit' exactly — linear in hours?"* SLOW: the credit function isn't in the one-line box.
6. Ticks "numbers explained: mostly" on her sheet. Stops.

**Q4 — trust**
- "95% range 57%-77%" — she believes it's a binomial interval but wants to know if it accounts for duplicate postings from the same employer.
- "13 of 20" vs the two red chips on Gaps — she'd mark it as a possible inconsistency until explained.

**Q5** — Wording 1: **7**. Wording 2: **5**. "Clear story. Small text kills it on a projector, and two pages counting gaps differently will cost them."

**Q7 — fixes**
1. Make the Gaps list and the report count missing skills the same way, or label the difference ("not taught at all" vs "too few hours").
2. Give the next-year number a range too, or say it has none.
3. Bigger type for the home fact strip and table numbers; it will be projected.

---

## 3. fac-external (faculty, phone, opened from WhatsApp)

Card line: *"Cares about whether the tool would help a real training manager; impatient with academic language."*

**Q2 — walkthrough (phone, before the viva)**
1. Taps the link in WhatsApp. Sees the spinner line "Loading the SkillAlign engine and job postings…" and a different subtitle: "SkillAlign compares a course's syllabus with job postings and shows what to add, what to expand and what to cut." — *"Right, that's the so-what. Good."* He can scroll while it loads.
2. When ready the subtitle changes to "6 of 10 example courses miss skills…". — *"Hm, the line changed under me. The first one was better for a training manager."* Minor MISREAD: thought the page had reloaded.
3. Taps "Check my course". Sees the pre-filled data analyst syllabus. Thinks of his own L&D programme (Java onboarding). Clears the jobs box, types "java developer", but doesn't want to type a syllabus on a phone. SLOW. Taps "Try an example (two-wheeler mechanic)" instead. — *"Two-wheeler mechanic. Not my world, but fine, show me the report."*
4. Reads the verdict box. "Likely between … (that range crosses a grade line, so the grade is borderline)". — *"'Crosses a grade line'. That's the academic bit. A training manager wants: add this, drop that."* Then "What to change, most important first: ADD …" — *"That's the bit. That I'd use."*
5. Taps "Market" in the bottom bar → Skills in demand. Rows of "steady". — *"Steady compared to what?"* SLOW, doesn't tap to find out.
6. Stops. Has seen enough to ask "who's your customer".

**Q4 — trust**
- "Nothing you type leaves your phone or computer." — he believes it but suspects a corporate L&D team would want it to save and share, so it reads as a limitation to him, not a feature.
- "(95% range 57%-77%)" — doesn't misunderstand it, just thinks a training manager will skip it.

**Q5** — Wording 1: **6**. Wording 2: **4**.

**Q7 — fixes**
1. Let a manager upload or paste a syllabus from a file; typing on a phone won't happen.
2. Keep the "add / expand / cut" line as the headline; push the range and grade-line language into a fold.
3. Explain "steady" in plain words on the row itself.

---

## 4. judge-sceptic-stat (judge, laptop)

Card line: *"Suspects job postings mis-measure vocational demand and that a single 'alignment score' hides judgement calls. Reads every footnote."*

**Q2 — walkthrough (7 minutes before scoring)**
1. Skips the hero, goes straight to "How it works". Reads the grey box: "score = 100 × Σ(share × credit) ÷ Σ share, over skills in 15% or more of ads". — *"Thank you. That's the first team this year to put the formula up front."* Then: *"15% threshold, credit cap — both judgement calls. At least visible."*
2. Opens Job market → Skills in demand → taps Workplace Safety: "23% of job ads in the latest 4 quarters (261 of 1,134; 95% range 21–26%). … Dashed line: a straight-line forecast a year ahead, 26% (95% range 22–31%)." — *"Straight line on eight quarters of synthetic data. The range is honest, the model is naive."*
3. Back to home: "Rising fastest: Battery Management Systems, up 213% on last year". — *"From what base? 213% of 1% is nothing."* MISREAD-risk for others; for him it's distrust. He looks for the count. The home tile doesn't give one. SLOW: he has to go to the Rising card.
4. Check my course, default syllabus: "SQL & Databases: … given 15 h; 16 h would earn full credit (its 30 h module "SQL for reporting" is shared with Data Analysis)." — *"So hours are split evenly across skills a module touches. That's an assumption about how teaching works, and it drives the score."*
5. Toggles the pill to real job ads to see if anything survives contact with reality. Doesn't see a note about the 6% company sample or the near absence of trade jobs on the pill itself. SLOW: has to dig in How it works.
6. Stops. Score drafted.

**Q4 — trust**
- "up 213% on last year" — a growth rate with no base count.
- "If the course stays the same, about 43 next year, because the jobs are changing." — a point forecast stated as a sentence of fact, from made-up data.
- "16 h would earn full credit" — false precision from an arbitrary even split of module hours.

**Q5** — Wording 1: **4**. Wording 2: **2**. "Better than most on transparency. The UI is fine; my problem is it presents assumptions as findings."

**Q7 — fixes**
1. Show base counts next to every growth rate ("from 9 to 28 ads").
2. Put the real-data caveats (6% company sample, almost no trade jobs) on the pill when real data is chosen.
3. Show the forecast as a range in the sentence, and say "if the trend holds" instead of "because the jobs are changing".

---

## 5. judge-nsdc-pm (judge, phone first, laptop if shortlisted)

Card line: *"Cares about whether QP/NOS codes are used, whether training partners could self-serve."*

**Q2 — walkthrough**
1. Phone, between meetings. Home: "Check my course … For trainers, ITIs and institutes." — *"Good, training partners named on the first screen."*
2. Taps "My course" in the bottom bar. Sees "Add NSQF level or QP code (optional)". Opens it: "These are printed on the report for your records. SkillAlign does not look them up." — *"So it doesn't map to NOS at all. That's the thing I'd want."* MISREAD first: she assumed the fold meant QP alignment. True: the code is only printed.
3. Looks for the upload-your-own-data part, which is what made her shortlist a tool last time. The bottom bar has Home · My course · Learn next · Market. No "Your data". The header on phone has only the logo and the pill. STUCK for a moment. Taps the pill: "…or use your own file." Finds it there. SLOW.
4. Shortlists it anyway, opens on laptop later. Your data: "A CSV file (in Excel: File → Save As → CSV)" bullet list, "Download an example file". — *"A training partner's MIS person could do this. Yes."*
5. Stops.

**Q4 — trust**
- "SkillAlign does not look them up." — not disbelief, disappointment; she'd misread the fold the first time.
- "6 of 10 example courses miss skills that their own jobs ask for" — she'd want to know which courses before believing a ratio.

**Q5** — Wording 1: **5**. Wording 2: **3**.

**Q7 — fixes**
1. Map courses to QP/NOS from the code, even for a few sectors.
2. Put "Your data" in the phone bottom bar.
3. Hindi, at least for the course check, for training partners in the districts.

---

## 6. judge-sih-industry (judge, laptop, 7 minutes, team 19 of 30)

Card line: *"Expects a crisp landing message and a 'wow' visual."*

**Q2 — walkthrough**
1. Home: "Do skill courses teach what jobs ask for?" Three journey cards. — *"Crisp. Problem in one line, three paths. That passes the first-screen test."* No chart on the first screen. — *"Where's the wow, though?"*
2. Team clicks "Check my course", then "Try an example (two-wheeler mechanic)". Report scrolls into view with a big number "/100". — *"OK, the big number is the visual. It's a number, not a wow."*
3. "What to change, most important first: ADD …" — *"This is the product. Show this first in the pitch."*
4. Job market → Example courses on desktop: red/amber bars, "Weak", "Partial", "borderline" tags. — *"Clean, reads like a real SaaS. 'borderline' tag — I get it."*
5. Notices the "Practice data" pill. — *"Made-up data. Every team uses dummy data, fine, but I'd dock feasibility."*
6. Time's up.

**Q4 — trust**
- "Rising fastest: Battery Management Systems, up 213% on last year" — sounds made up, and he knows it is practice data, so he'd ignore it.

**Q5** — Wording 1: **7**. Wording 2: **5**.

**Q7 — fixes**
1. One strong visual on home: a before/after of a course score after adding the top skill.
2. Make the demo start on real job ads so the numbers aren't dismissed.
3. A 20-second "try it" path that fills itself in for the judge.

---

## 7. learn-sceptic-switcher (learner, phone only, Marathi first)

Card line: *"Sceptical of websites that 'score' people, worried it will say she is not good enough. … Would quit at the first unclear screen."*

**Q2 — walkthrough (find what to learn next)**
1. Opens on phone. Big heading "Do skill courses teach what jobs ask for?" — *"This is about courses, not about me? Maybe this is for teachers."* MISREAD: she nearly leaves thinking the site isn't for job seekers. Then sees "What should I learn? Pick the job you want and say what you know." OK.
2. Taps "Learn next" at the bottom. "The job I want (start typing, then pick from the list)". Types "data entry". I don't know what the list offers her, the screens I was given don't show it.
3. "What I already know (skills separated by commas, or paste your resume)". — *"Resume? I don't have one now, six years gap."* Types "typing, excel, data entry". SLOW.
4. Taps "Show what to learn". The example in the walkthrough shows a ring "37% ready for Data Analyst". I don't know what number she would see for data entry. If it is low like that, the ring is exactly the thing she feared. The line "This is about skills on paper, not about you" helps a little — *"they know it sounds bad."*
5. The "Practice data" pill at the top — she doesn't tap it. She doesn't know the job ads are made up. MISREAD: she thinks the result is about real jobs in her area.
6. QUIT if the percentage is low; if it says one skill to learn, she might screenshot it.

**Q4 — trust**
- The "% ready" ring. She'd read it as a mark on herself, whatever the small line says.
- "Practice data" — she'd read it as "practice mode", not "the job ads are fake".

**Q5** — Wording 1 (come back in a month): **3**. Wording 2 (send to someone in her position): **2**.

**Q7 — fixes**
1. Don't show me a percentage of me. Just say what to learn and why.
2. Marathi.
3. Say in plain words, before I start, that these jobs are examples and not real.

**Q8 — Hinglish (Marathi first; asked in Hinglish)**
Last step: *"Maine 'Show what to learn' dabaya. Upar ek gola aata hai, 'ready' percent ke saath. Agar kam aaya toh bura lagega, main band kar dungi. Neeche likha hai 'skills on paper, not about you', theek hai, par pehle number hi dikhta hai."*
Q5 w1 in Hinglish: *"Agle mahine wapas? Shayad nahi. 3."*
Bottom line changed? No. Same 3; she adds that a Marathi version would matter more than Hindi.

---

## 8. learn-btech-fresher (learner, laptop)

Card line: *"Wants a software developer job; will try to break the tool by pasting their resume."*

**Q2 — walkthrough**
1. Home, clicks "What should I learn?". "The job I want": types "software dev", picks from the list (I don't know the exact list items; assumes "software developer" is there).
2. "What I already know … or paste your resume". Pastes his whole one-page resume including CGPA, phone number line, project names. — *"Let's see if it chokes."* I don't know how the reader handles it; the walkthrough doesn't show this case.
3. "Show what to learn". Sees a "LEARN NEXT" box. I don't know which skill it named for him. In the Gaps list on the Market tab he can see "Junior Software Developer: Python 59%, Cloud Computing 45%" — *"If it tells me Python I'll know it didn't read my resume, Python's on line two."*
4. Taps the "Practice data ▾" pill out of curiosity. "These 2,216 job ads are made up". — *"Wait, so it was all fake?"* Switches to "Real job ads, India 2026". Re-runs. Has to re-enter? He doesn't know if the form keeps the values. SLOW.
5. "Courses that teach what you are missing" — lists "[example course]". — *"Example course, so I can't actually enrol anywhere. Useless for me."*
6. Stops after two tries.

**Q4 — trust**
- The default "Practice data". He'd say the default should be the real 19,194 ads for anyone wanting a job.
- "[example course]" — reads first as real courses, then realises they're invented.

**Q5** — Wording 1: **5**. Wording 2: **3**.

**Q7 — fixes**
1. Default to real job ads for the learner path.
2. Show which skills it pulled from my resume, so I can see it read it right.
3. Link to real courses (NPTEL, free ones), not made-up ones.

---

## 9. learn-iti-trainee (learner, budget Android, prepaid data, Hindi best)

Card line: *"Budget Android, prepaid data that runs out by month end; reads Hindi best, simple English with effort."*

**Q2 — walkthrough**
1. Taps the link from the class WhatsApp group. Spinner: "Loading the SkillAlign engine and job postings…". — *"Loading … chal raha hai."* Page is there but it keeps loading. 12 MB on his data at month end. SLOW; if data is low, QUIT here.
2. Assume data lasts. Heading in English. Reads slowly: "What should I learn?" — *"Haan, yahi chahiye."* Taps it.
3. "The job I want". Types "electrician". Picks it. "What I already know" — types "wiring, motor". Taps "Show what to learn".
4. A green box "LEARN NEXT · …". The walkthrough shows PLC & Industrial Automation only for real data; on practice data (the default) I don't know which skill it shows. He reads whatever it says as true. MISREAD: he doesn't know the ads are made up; "Practice data" to him means nothing.
5. "Courses that teach what you are missing" — sees "Electrician (ITI trade) [example course]" maybe; he thinks it's his own ITI course. Not sure. Doesn't know.
6. Takes a screenshot to ask sir. Stops.

**Q4 — trust**
- "Practice data" — doesn't understand it; believes the numbers are about real factory jobs.
- "95% range" lines — skips them, can't read them.

**Q5** — Wording 1: **2**. Wording 2: **3** — he'd forward it to the class group only because sir did first.

**Q7 — fixes**
1. Hindi.
2. Smaller download, or say how much data it uses before it starts.
3. Gulf / factory jobs in the list, and say clearly if the jobs are not real.

**Q8 — Hinglish**
Last step: *"Electrician daala, 'Show what to learn' dabaya. Hara box aaya, ek skill likha tha. Screenshot liya, sir ko poochunga ki yeh seekhna hai kya. Baaki angrezi bahut hai."*
Q5 w1: *"Agle mahine? Data hi khatam ho jata hai. 2."*
Bottom line changed? No. Still 2. Language makes the page easier but the data cost is the blocker.

---

## 10. prov-sceptic-owner (provider, phone only, tier-3 computer centre)

Card line: *"'Students come for the certificate, not the syllabus'. Uses phone only. Will not read long text."*

**Q2 — walkthrough (check one of his courses)**
1. Opens on phone. "Do skill courses teach what jobs ask for?" — *"My students don't care."* Scrolls anyway.
2. Taps "Check my course". Sees a box full of English text already in it, "Spreadsheets: advanced Excel and pivot tables (40 hrs)". — *"I have to type my whole syllabus? On phone?"* SLOW.
3. "Jobs this course trains for … e.g. "data analyst, MIS executive"". He'd type "Tally" — that's a course, not a job. MISREAD: he thinks the field wants the course name. True: it wants job titles from ads.
4. Doesn't get to the report. QUIT. "No sign-up" was nice, but it's still English and typing.

**Q4 — trust**
- "Check yours in a minute." — Not on a phone, with a syllabus in a file somewhere.

**Q5** — Wording 1: **1**. Wording 2: **1**.

**Q7 — fixes**
1. Let me pick my course from a list (CCC, Tally) instead of typing.
2. Hindi.
3. Tell me in one line if my course gets students jobs, nothing else.

---

## 11. prov-private-head (provider, office laptop — his guess, not on the card)

Card line: *"Wants a quick way to justify adding a module to the owner."*

**Q2 — walkthrough**
1. Home → "Check my course". Sees a data analyst syllabus already filled in. — *"That's almost my batch."* Replaces it with his own modules from his Google Doc: Excel, SQL, Power BI, Python basics, GenAI (20 hrs). Watches "Skills found as you type" chips fill in. — *"Nice, it's reading as I paste."*
2. "Jobs this course trains for": "data analyst, business analyst, MIS executive".
3. Notices "Practice data". Taps it, reads "made up", switches to "Real job ads, India 2026". Re-checks. I don't know the real-data numbers; the walkthrough only shows practice.
4. On the practice run: "ADD Data Visualisation: asked for in 68% of job ads for these roles (95% range 57%-77%)". — *"We teach Power BI. Does it not count Power BI as visualisation?"* MISREAD-risk; he doesn't know whether the reader maps Power BI → Data Visualisation. SLOW: opens "Skill by skill" to check.
5. "Print or save as PDF". — *"This, to the owner, with the GenAI line circled."*
6. Stops.

**Q4 — trust**
- "Generative AI Tools: 28% …, up 306% on last year" on practice data — he'd love to quote it, but it's made up; he'd only use the real-data version.
- "about 43 next year" — he'd not show the owner a forecast he can't explain.

**Q5** — Wording 1: **6**. Wording 2: **5** — he'd send it to one other academic head he knows.

**Q7 — fixes**
1. Show on the report which tools (Power BI, Tableau) counted toward which skill.
2. Put the data source (real ads, period, how many) at the top of the PDF so the owner trusts it.
3. Let me save my syllabus so I can re-run it in six months.

---

## 12. prov-placement-officer (provider, office desktop)

Card line: *"Wants to show HoD which skills recruiters ask for. Downloads reports into Word to forward."*

**Q2 — walkthrough**
1. Home → "See the job market". "Skills employers ask for most" — bars with percentages and "steady". — *"Steady, okay, not changing."* Taps Workplace Safety: trend chart. — *"Good for HoD."*
2. Wants this list as a file. No print or download on the market page; "Print or save as PDF" only appears on course reports. STUCK for exporting the skills list. Tries Ctrl+P on the whole page — not sure how it will look. SLOW.
3. Sees "Your data" in the top menu. Lede rewritten for placement cells. "A CSV file (in Excel: File → Save As → CSV)". — *"My recruiter Excel! Can I put it in?"* Downloads the example file to see columns. SLOW: his sheet is recruiter-wise, not posting-wise; he'd need to reshape it. I don't know if it accepts his columns.
4. Notices "Practice data" pill. — *"These ads are made up? Then the HoD can't see this."* Switches to real job ads.
5. Stops; will try his CSV later.

**Q4 — trust**
- "70 different skills asked for" — he'd ask who decided what counts as a skill.
- "↑ 201%" for Generative AI Tools — HoD will ask "201% of what".

**Q5** — Wording 1: **6**. Wording 2: **4**.

**Q7 — fixes**
1. Download the skills list (Word or Excel), not just the course report.
2. Accept a recruiter-wise sheet, or show exactly how to turn mine into the example format.
3. Show counts beside the % so HoD can sanity-check.

---

## 13. prov-ngo-coord (provider, Android phone, Hindi first, Nagpur)

Card line: *"Reports placement numbers to a CSR funder monthly. Would love a chart to put in the funder report."*

**Q2 — walkthrough**
1. Phone. Taps "Market" in the bottom bar. Tiles: "2,216 job ads · 70 different skills asked for". Filters: District. Looks for Nagpur (the practice data covers 12 Maharashtra districts; the screens don't show whether Nagpur is one of them, so I don't know).
2. Skills in demand: taps "Customer Service 8% steady" (retail). Trend chart opens. — *"Yeh chart funder ko dikhaun?"*
3. Then sees the pill. Taps it: "These 2,216 job ads are made up … not facts about real jobs." — *"Toh yeh chart report mein nahi daal sakti."* Switches to "Real job ads, India 2026". Retail, data entry and GDA have few real ads (I don't know the exact counts; the facts say almost no trade jobs). Expects "too few". SLOW.
4. Tries "My course" with her data entry course. Types the syllabus on the phone, slowly. Gets a report. "Print or save as PDF" — on Android this goes to the print dialog; she isn't sure where the PDF saves. SLOW.
5. Stops; will screenshot instead.

**Q4 — trust**
- Any chart on practice data — she can't put made-up numbers in a CSR report.
- "95% range 21–26%" — she'd misunderstand it as "between 21 and 26 percent of girls get jobs". MISREAD.

**Q5** — Wording 1: **4**. Wording 2: **4** — she'd send it to another coordinator for the course-check part.

**Q7 — fixes**
1. Real data for retail, data entry and GDA in Maharashtra, so the chart can go to the funder.
2. A "download chart as image" button.
3. Hindi.

**Q8 — Hinglish**
Last step: *"Report aaya, 'Print or save as PDF' dabaya, phone ne print ka page khola, PDF kahan gaya pata nahi. Screenshot le liya."*
Q5 w1: *"Wapas aaungi agar asli data ho retail ka. Abhi 4."*
Bottom line changed? No. Still 4; she said she'd read the page faster in Hindi but the funder-chart problem is the same.
