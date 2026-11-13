# Round 1 persona interviews: SkillAlign v1 (model: opus, claude-opus-5-5)

Simulated screening only. n real = 0. Each section is one persona answering the script in `interview.md`, written separately. Where the fact sheet or walkthrough does not say what happens, the persona says so.

Problem tags: STUCK = cannot go on · MISREAD = understood something wrong · SLOW = got there with effort · QUIT = stopped.

---

## 1. fac-hod-sceptic (faculty, laptop)

**Q1 (past behaviour).** Last semester a team showed me a very glossy placement-prediction dashboard. Animations, a dark theme, the lot. I asked one question: where did these numbers come from? The boy who presented looked at the girl who wrote the scraper, she looked at the floor. I gave them low marks. I trust a project when each student can point to a number on the screen and tell me which file it came from and which line of code they wrote. I give up the moment I feel I am being shown a template.

**Card line that shapes use:** "Asks 'where is the real data, who would use this, what did YOU write'."

**Q2 (walkthrough, 10 minutes, decide on the interface and what to ask).**
1. I open the link. "Starting the Python engine in your browser. Loading Python (about 12 MB…)". Five to ten seconds of nothing. Fine, but in a viva I will note it. **SLOW.**
2. The first thing I read properly is the yellow box: "These job postings are synthetic, generated to show how the method works, so the numbers are not facts about real jobs." So the headline numbers are invented. I respect that they say it, but now everything on the first screen is decoration to me. My first question to them is already written: why is the default view the fake data?
3. Heading "Are skill programs teaching what jobs ask for?" A question, not an answer. Tiles: "70.9 average program alignment here (out of 100)". Alignment of what with what? I don't know yet. **MISREAD (mild):** I took "average program alignment here" to mean something about the district filter; it is the average of the ten program scores. I only worked that out after visiting Programs.
4. I switch the menu to "Real postings: India 2026". The banner says "Two quarters only: shares and scores, no trends." But the card still says "Share of postings in the latest four quarters". Two quarters or four? **MISREAD**: for a minute I thought they had four quarters of real data. They have two. That is exactly the kind of sloppiness I ask about.
5. Programs tab. Every program says "(illustrative)". So the programs are invented too. "6 of 10 programs below Strong" on the first page was about invented programs scored on invented jobs. I write down: what in this project is real?
6. I click "Junior Software Developer". Nothing seems to happen at the top; the report is far below the table. I scroll. **SLOW.** "43 alignment today · Weak" and next to it "100% of 400 hours on core skills". All hours spent on core skills, yet weak. I do not understand how both are true. **MISREAD**, I think it is a bug; probably it means the hours go to skills that are core but the many other core skills are missing. Not explained on the tile.
7. How it works. "Mantel-Haenszel", "Bonferroni", "400 employer resamples". This reads like a textbook or a chatbot. Second-year students who wrote all this? I stop reading after section 2. My viva questions: who wrote the skill reader, show me the Bonferroni code, why 15%, why 200 hours.
8. I stop here. I have my questions.

**Q3.**
- Wording 1 (rank all seven): How it works, Your data, Programs, Check a syllabus, Market pulse, Gap matrix, For learners. How it works first only because it is where I will catch them out.
- Wording 2 (keep three): How it works, Your data, Check a syllabus. If they cannot defend the method page, nothing else matters; uploading real data is the only way past the synthetic problem; the syllabus check is the only part a user actually does something in.

**Q4 (trust).** "Generative AI Tools … +201%". This is on synthetic data. A 201% rise in a skill in data the students generated themselves tells me only what the generator was told to do. Also "The dashed line is a straight-line forecast four quarters ahead: 26%, 95% range ." with the range simply missing. A blank where a number should be. I would ask them to show me that in the code.

**Q5.**
- W1 (chance I rate interface and UX good or better): 4.
- W2 (full marks for usability): 1. Full marks require the default screen to show something real.

**Q6 (decoy Programs page).** A table with "jsd_01", "S", "R", "N", "H" and "recs: +cloud,+python…". No headings, no explanation. That is a database dump, not an interface. 1.

**Q7 (fixes).**
1. Make the first screen say plainly what is real and what is made up, and open on the real data if it exists.
2. Stop the leftovers: "latest four quarters" on two-quarter data, the blank "95% range ." Small errors make me doubt the large claims.
3. Put a one-line "how this number is made" under each big number instead of sending me to a long page of statistics vocabulary.

**Q8.** Not applicable (card does not say Hindi or Marathi first).

---

## 2. fac-ta-phd (faculty, projected screen in lab)

**Q1.** Rubric sheet, projector, five minutes per team. Last time I flagged a team whose bar charts had no axis units and no sample size. I trust a demo when every number on screen tells me its denominator. I lose patience when the team has to say "this one means…" out loud because the screen doesn't.

**Card line:** "Cares whether the demo story is clear in 5 minutes and whether numbers on screen are explained."

**Q2 (10 minutes, from the projected screen while the team drives).**
1. Load spinner on the lab machine, 5-10 s. Tolerable. Team should pre-load. **SLOW** (minor).
2. Market pulse. "2,216 postings in this view", "70 different skills found in them": denominators, good. "70.9 average program alignment here (out of 100)": unit given, good.
3. "Most demanded skills": "Share of postings in the latest four quarters that mention the skill." Clear definition. Then the right column: "+6%", "−14%", "+28%". Percent or percentage points? From 23% share, +6% could be 23 vs 21.7 (relative) or 23 vs 17 (points). **MISREAD**: I assumed points first. The trend card later says "6% (not significant) on the year before", which still doesn't settle it.
4. Only "+201%" is green; the rest are grey. On a projector there is no hover, so the "within chance: not a trend" tooltip never shows. I read grey as "less important" rather than "not significant". **MISREAD.** That is the single most important statistical idea on the page and it's hidden behind a mouse-over.
5. The team clicks Workplace Safety. Nothing visible changes; they have to scroll to the bottom. **SLOW.** Then: "95% range 21–26%, 261 of 1,134" (good, counts given) and "forecast four quarters ahead: 26%, 95% range ." Blank. I'd mark that on the sheet.
6. Programs. Score and range "43 40–46". The lede says "The range shows how much the score could move with a different sample of postings." How it works says the score range is 90% while shares use 95%. Mixed intervals on the same report without saying which is which. **MISREAD risk**; I only know because I read the method page.
7. Skill by skill table: "Hours column: hours given / hours needed for full credit." Then "20 / 9" for Git and "/ 8" for Python. It took me a second; first I read "20 / 9" as 20 of 9-something. Also, 9 hours for full credit on Git but the reference course is 200 h? Fine once read. **SLOW.**
8. Gap matrix on the projector: 24 column labels rotated 90°, small grey text. From row three of the lab I cannot read them. **STUCK** for this tab on a projector.
9. I stop at the matrix; I have five minutes of notes.

**Q3.**
- W1: Programs, Check a syllabus, Market pulse, How it works, For learners, Gap matrix, Your data.
- W2: Programs, Check a syllabus, How it works. Programs is the core output; the syllabus check proves the method generalises; how-it-works is what I'd check the numbers against.

**Q4.** "+6%" next to "23%". I would genuinely misunderstand whether that is relative change or percentage points. And the grey colour as the only signal of "not significant": I'd misread every grey number as a real but small trend.

**Q5.**
- W1: 6. The labelling is better than most teams'.
- W2: 3. Blank range, hover-only significance, unreadable matrix on a projector.

**Q6 (decoy).** Columns "P S R N H", no units, no legend. It's the exact thing I flagged last year. 1.

**Q7.**
1. Show significance on the screen itself, e.g. "+6% (not a trend)", not only in a hover tooltip.
2. Open the clicked report or trend card where I'm looking, or jump to it visibly, and fix the blank forecast range.
3. Say "percentage points" or "relative" on every change number, and say 90% vs 95% next to each range.

**Q8.** Not applicable.

---

## 3. fac-external (faculty / external examiner, phone via WhatsApp)

**Q1.** We buy LMS add-ons and skills-gap dashboards at my firm. Vendors send a link, I open it on my phone in the cab. If the first screen does not tell me what decision it helps me make, I close it and ask for a call. Last viva I told a team their dashboard needed a "so what" on the first screen. I trust a tool when it gives me one sentence I could repeat to my VP.

**Card line:** "Cares about whether the tool would help a real training manager; impatient with academic language."

**Q2 (on phone, 10 minutes before the viva).**
1. Tap the WhatsApp link. Spinner, "Loading Python (about 12 MB, first visit only…)". On cab 4G, longer than I'd like. Why do I need to know it's Python? **SLOW.**
2. Logo, data dropdown, "2,216 postings · 2024-Q4 to 2026-Q3", then a tab row cut off at "Chec". I assume there are four tabs. **MISREAD**: there are seven; I never see "For learners", "Your data" or "How it works" unless I swipe, and nothing tells me to.
3. Yellow box fills most of the screen: "the numbers are not facts about real jobs". So the first thing I learn is that it's not real. Not a great "so what".
4. "Are skill programs teaching what jobs ask for?" Then "works out which skills employers want and which are changing beyond chance". "Beyond chance" is the academic language I don't want. Scroll. Two tiles visible at a time. "6 of 10 programs below Strong here" is the only so-what and it's the fourth tile. **SLOW.**
5. Tap Programs. Long paragraph, then a table with only PROGRAM, SCORE AND RANGE, NEXT YEAR. No bar, no hours column on phone. "43 40–46 Weak · 34 ↓". Red arrow down on almost everything. I read that as "these programs are getting worse". **MISREAD**: it's what the score would be next year if the course doesn't change, driven by the job market shifting.
6. Tap Junior Software Developer. Report appears way below the table; I scroll a lot. **SLOW.** "What to change": 13 ADD tags. That's actually what a training manager wants. But 13 adds to a 6-month course with no "drop this" for software? Which first? It lists them in an order but doesn't say it's a priority order.
7. Tap Gap matrix. Two columns visible. I don't know I can drag. **STUCK.**
8. I stop. Viva starts.

**Q3.**
- W1: Programs, Check a syllabus, Market pulse, Your data, Gap matrix, For learners, How it works. (I didn't see the last three tabs on the phone; ranking them from the names the team showed me later.)
- W2: Check a syllabus, Programs, Your data. A training manager wants to paste their own outline and upload their own job data; the illustrative programs are only a demo of that.

**Q4.** "34 ↓" under NEXT YEAR. I'd tell my VP "their program is declining" when it's a projection under an assumption. Also "within the same job roles" in Emerging; I don't know what that qualifier changes and I wouldn't spend time finding out.

**Q5.**
- W1: 4.
- W2: 2. On phone the most useful parts are hidden or cut off.

**Q6 (decoy).** "jsd_01 43 40-46 34 1.00". Meaningless on a phone or anywhere. 1.

**Q7.**
1. Put the so-what first: one sentence like "6 of 10 programs miss skills their jobs ask for; tap one to see what to add."
2. Fix the phone: show all tabs (or a menu), and show a hint on wide tables.
3. Replace "beyond chance", "within roles", "borderline" with plain business words, and label the down arrow as "if unchanged".

**Q8.** Not applicable.

---

## 4. judge-sceptic-stat (judge, laptop, reads every footnote)

**Q1.** I review indices for a living: skill-gap indices, employability scores, district dashboards. Last time I asked a team to show me the exact formula behind their "readiness score" and they could not. I trust a score when I can rebuild it by hand from what is on the page and when its uncertainty is stated. I distrust anything that collapses many judgement calls into one number with one decimal place.

**Card line:** "Suspects job postings mis-measure vocational demand and that a single 'alignment score' hides judgement calls. Reads every footnote."

**Q2 (7 minutes before scoring).**
1. I go straight to How it works. "core = 15%+", "30-posting minimum", "200-hour reference course", "400 employer resamples", "90% range". These are exactly the judgement calls I suspected; at least they're listed. Whether the page gives the full scoring formula as an equation I can't tell from what I saw; it reads as prose. **SLOW.**
2. "Real data": "6% sample", "recognises 50% of skill items", "32% on held-out US postings", "0.2% trade jobs". Honest. It also confirms my prior: postings say almost nothing about vocational demand. Then: "Nothing yet shows that higher scores lead to more placements." I'd underline that; most teams never write it.
3. Market pulse, synthetic. "70.9 average program alignment" to one decimal on synthetic programs and synthetic jobs. False precision. "Declining: No change here passes the significance test with 1,134 recent postings." Good; they are not inventing declines.
4. Grey vs green change numbers; significance only in a tooltip. I hover and find it. **SLOW.**
5. Check a syllabus with the pre-filled example. "compared with 150 postings for: data analyst". Then For learners with "data analyst": "173 postings for this job". Same role, same dataset, different counts. **MISREAD**: I first assumed a bug; probably the learner tab matches job titles differently from the syllabus tab's "target roles". The screen doesn't explain it.
6. Same role, Generative AI: "up 306% on last year" in the syllabus result, "+201%" on Market pulse, "+191% within roles" in Emerging. Three numbers for one skill. Different bases, presumably. Not reconciled on screen.
7. "REDUCE Typing Speed: only 0% of postings ask for it (at most 5%)". 0% with an upper bound of 5%; fine statistically, odd to a layperson.
8. "EXPAND SQL & Databases: … given 15 h; 16 h would earn full credit." The user typed 30 hrs for SQL. The 30 h was split across two skills. A cliff at 16 h means the score is a step function of hours. That's a judgement call that matters, and the screen hides it. **MISREAD** at first: I thought it had misread the hours.
9. Time's up.

**Q3.**
- W1: How it works, Check a syllabus, Programs, Your data, Market pulse, Gap matrix, For learners.
- W2: How it works, Your data, Check a syllabus. The method and the ability to run it on better data are the only defensible parts; the scored illustrative programs are a demo.

**Q4.** "70.9 average program alignment here (out of 100)" — one decimal on an average of ten illustrative programs on synthetic postings. And "SQL & Databases … given 15 h; 16 h would earn full credit" — the user typed 30 hours; the split is invisible, and the threshold implies one more hour flips credit.

**Q5.**
- W1: 6. As an interface, it is careful and labels its uncertainty more than most.
- W2: 3. Inconsistent counts and changes across tabs for the same role.

**Q6 (decoy).** No definitions, no intervals labelled, "1.00" for hours share. I'd score it near zero. 1.

**Q7.**
1. Show the formula for a program's score on the report itself, with the actual numbers plugged in for that program.
2. Reconcile or explain the different posting counts and growth figures for the same role across tabs.
3. Show how module hours were split across skills, so "given 15 h" is traceable to the "30 hrs" the user typed.

**Q8.** Not applicable.

---

## 5. judge-nsdc-pm (judge, phone between meetings, laptop if shortlisted)

**Q1.** Last cycle I shortlisted a tool mainly because a training partner could upload their own placement data and get a dashboard without calling the vendor. I look for QP/NOS codes first; if a tool talks about "courses" and "skills" without QP codes, it hasn't met the system we run. I give up when I need to sit at a desk to understand the first screen.

**Card line:** "Cares about whether QP/NOS codes are used, whether training partners could self-serve."

**Q2 (phone, 7 minutes).**
1. Spinner with 12 MB note. Meeting room Wi-Fi, okay. **SLOW** (minor).
2. Banner: "Demo data… synthetic". Fine for a hackathon. Heading, tiles. I scroll.
3. Tab row cut at "Chec". I swipe the tab row because I'm used to apps; I find "Check a syllabus", "For learners", "Your data". Many reviewers wouldn't. **SLOW.**
4. Programs. "ITI-style trade course (illustrative)", "Short-term skilling course (illustrative)". No QP codes on any program. **MISREAD (mild):** I first thought "Electrician (ITI trade)" was the actual NCVT Electrician trade being scored; it's an invented one.
5. Check a syllabus. "Qualification pack code (optional)" and "NSQF level (optional)". Good, someone thought of us. And "You can paste a qualification pack's National Occupational Standards here, one per line." That is useful. But does entering the QP code fetch anything or change the score? The screen doesn't say. I don't know. **MISREAD risk**: I'd assume it pulls the QP from NSDC; I suspect it does nothing except label the report.
6. The form on a phone: paste a syllabus into a textarea. Possible but painful. **SLOW.**
7. Your data. "Use your own job postings… Nothing leaves your browser." Self-serve, which is what I want. But it's job postings, not the training partner's placement data. The CSV format is a dense paragraph; on a phone I skim it. A TP won't have a CSV with "title, date, description" columns. **SLOW.**
8. I mark it "look at on laptop". Stop.

**Q3.**
- W1: Check a syllabus, Your data, Programs, Gap matrix, Market pulse, For learners, How it works.
- W2: Check a syllabus, Your data, Gap matrix. The two self-serve parts first; the matrix is the slide I'd show my director.

**Q4.** "Qualification pack code (optional)". I would assume it's connected to the QP/NOS database. Nothing on screen tells me what it does. And "Electrician (ITI trade) … 74 Partial borderline" might be quoted by someone as a rating of the real trade.

**Q5.**
- W1: 6.
- W2: 4. On phone, half the tabs are hidden and the forms are hard.

**Q6 (decoy).** "elec_iti 74 69-80 71 0.77". No labels, nothing a TP could use. 1.

**Q7.**
1. Say what the QP code field does, and if possible use it: pull the NOS list from the QP code.
2. Make every tab visible on phone.
3. Make "Your data" accept the kind of sheet a training partner actually has, with a short example table, not a paragraph.

**Q8.** Card says "Hindi and English", not Hindi first. Skipped.

---

## 6. judge-sih-industry (judge, laptop, 7 minutes, 30 teams a day)

**Q1.** At the last hackathon I gave a team a low UI score because their first screen was a wall of text and I had to ask "so what does it do?". The ones I remember had one big visual in the first five seconds and a live demo that didn't stall. I trust a demo when the team clicks once and something impressive happens.

**Card line:** "Expects a crisp landing message and a 'wow' visual."

**Q2 (7 minutes).**
1. Team opens the URL live. Spinner: "Starting the Python engine in your browser." 5-10 seconds of dead air in a 7-minute slot. **SLOW.** (Cool that Python runs in the browser, but tell me that, don't make me wait for it.)
2. First thing above the fold: a yellow warning, "the numbers are not facts about real jobs". That's the opposite of a wow. Then a serif headline as a question. Then a lede. Then filters. Then four tiles. Clean, but plain; it looks like a report, not a product.
3. "Emerging": "Battery Management Systems +213%" with a tiny sparkline. That's the most interesting thing on the page and it's in a side card.
4. Programs: coloured bars, Weak/Partial/Strong badges. Okay. Clicking a row: the report appears below the table, team scrolls. **SLOW.**
5. Gap matrix: this is supposed to be the wow. It's mostly empty white with rotated labels. Some ticks and red boxes. I don't get it in 3 seconds. **SLOW.**
6. For learners: the "37%" ring. That's the closest thing to a wow. "Programs that close your gaps… 2 YEARS Electrician (ITI trade) covers Machine Learning." I laugh. **MISREAD** on the tool's side; I'd note it as a demo bug.
7. Time.

**Q3.**
- W1: For learners, Check a syllabus, Programs, Gap matrix, Market pulse, Your data, How it works.
- W2: For learners, Check a syllabus, Programs. Interactive first. Nobody on a jury reads the method page.

**Q4.** "Electrician (ITI trade) covers Machine Learning." Either the data or the matching is wrong, and it makes me doubt everything else. Also "+201%": on synthetic data, a big green number is theatre.

**Q5.**
- W1: 5.
- W2: 2. No landing message, no wow, a load wait, a visible bug.

**Q6 (decoy).** "P S R N H" table. I'd move on in two seconds. 1.

**Q7.**
1. A landing screen with one sentence and one striking visual (e.g. the program list as a big coloured chart), and the demo-data notice shrunk to a small tag.
2. Pre-load the engine or show something useful while it loads.
3. Fix the matching bug in "Programs that close your gaps" and make the gap matrix readable at a glance.

**Q8.** Not applicable.

---

## 7. learn-sceptic-switcher (learner, phone only, Marathi first)

**Q1.** When I wanted to start working again, I asked my cousin who works in an office in Pune and searched "data entry job near me" on my phone. I looked at Naukri once but it asked for a full profile and showed "experience: 2-5 years" everywhere, so I closed it. I trust what my cousin says. Websites that give you a score, I feel they will tell me I'm not good enough after six years at home.

**Card line:** "sceptical of websites that 'score' people, worried it will say she is not good enough. Phone only. Would quit at the first unclear screen."

**Q2 (phone, find what to learn next).**
1. Open link. White screen, "Starting the Python engine in your browser." Python? Is this for programmers? I wait because my friend sent it. **MISREAD**: I thought the site is only for computer people.
2. Top: "Synthetic demo data" box, "2,216 postings". I don't know "synthetic". Yellow box: "These job postings are synthetic… the numbers are not facts about real jobs." So the jobs are not real? Then why would I use it? **MISREAD**: I think the whole site is fake/a test.
3. Big heading "Are skill programs teaching what jobs ask for?" It is talking about programs, not about me. I don't see anything for me.
4. Tabs: "Market pulse", "Programs", "Gap matrix", "Chec…". Nothing says "for me" or "jobs". I don't know there is "For learners" further right. **STUCK.**
5. I tap "Programs" because I did a course. "Data Entry Operator … 74 … Partial … borderline … 54 ↓". The course I did was data entry. Borderline and red arrow down. **MISREAD**: I think it is saying data entry courses like mine are not good and getting worse, so what I learned is useless. That is exactly what I was afraid of.
6. I close it. **QUIT.**

**Q3.**
- W1: For learners, Programs, Market pulse, Check a syllabus, Gap matrix, Your data, How it works. (I didn't see "For learners" on my phone; when you read me the names, that's the only one that sounds like me.)
- W2: For learners, Market pulse, Programs. If it is for me, I want only the part for me, and maybe the list of jobs that people want.

**Q4.** "the numbers are not facts about real jobs". If they say it themselves, I won't believe anything after it. And "Data Entry Operator … borderline": I would understand it as my course being bad.

**Q5.**
- W1 (come back next month): 1.
- W2 (send to someone like me): 0. I wouldn't send a friend something that made me feel bad.

**Q6 (decoy).** "deo_04 74 67-77". I wouldn't know what it is. 0.

**Q7.**
1. On the first screen, a big button like "I want a job: what should I learn?", in Marathi also.
2. Don't call it fake on top; say it in a simple way, or show real jobs first.
3. Don't make it feel like marks for me; say "you already have these skills" first before what is missing.

**Q8 (Hinglish).**
Last step, Hinglish: "Programs pe click kiya kyunki maine course kiya tha. 'Data Entry Operator 74 Partial borderline' aur laal arrow neeche. Matlab mera data entry course bekaar hai aur aur kharab ho raha hai? Yehi dar tha mujhe. Main band kar deti hoon."
Q5 W1 in Hinglish: "Agle mahine wapas aaungi? Shayad nahi. 1 out of 10. Agar Marathi ya Hindi mein hota aur 'mere liye' wala button upar hota, toh shayad dekhti."
Bottom line changed? No. Still 1. In my own mix of words the fear is even clearer, but the score stays.

---

## 8. learn-btech-fresher (learner, laptop, wants software developer job)

**Q1.** I did what everyone does: opened ten JDs on LinkedIn for "SDE 1" and "full stack developer", pasted them into ChatGPT and asked "what am I missing". Also checked roadmap.sh. Trust came from seeing the same skills in many JDs. I gave up on one of those resume-score sites because I pasted my resume with "Next.js" and it said I don't know React.

**Card line:** "will try to break the tool by pasting their resume."

**Q2 (find what to learn next).**
1. Spinner, Python in the browser via Pyodide. Okay, that's actually neat. Wait 5-10 s.
2. Ignore Market pulse; click "For learners". Clear heading "How ready am I for a job?".
3. "Job I want: start typing to search the jobs in this data". I type "sde". Whether it finds anything for "sde" I don't know; the walkthrough doesn't show it. I try "software developer". Then I paste my full resume into "What I can do", projects, CGPA, everything.
4. What it returns for my resume isn't shown in the material I have, so I don't know my exact percentage. What I can see from the data analyst example: it lists "Skills we read from your text" and only skills in at least 15% of postings. Good that it shows what it read, that's how I'd catch it.
5. I try to break it: I type "I know Excel and basic SQL" for data analyst to compare with the default. "37% ready". "Learn next: Generative AI Tools, asked for in 29% of these postings and rising." Learn next is GenAI over Python (58%) and Data Visualisation (67%)? **MISREAD**: I thought "learn next" meant "most asked-for missing skill". It seems to pick the rising one. Weird priority.
6. "Programs that close your gaps": "2 YEARS Electrician (ITI trade) covers Machine Learning." Broken. Screenshot for the group chat.
7. The yellow box: "synthetic". So "Learn next" is from generated data. I switch to "Real postings: India 2026". That's what I actually want. I'd redo it there.
8. Programs → Junior Software Developer, compared with "195 postings for: software developer, software engineer… .net developer". "ADD Cloud Computing, Python, React, Generative AI Tools…" The order isn't the share order (Python 59% comes after Cloud 45%). **MISREAD**: I assumed sorted by demand; it isn't, and it doesn't say what the order is.
9. I stop. I have my list (it's the same as my ChatGPT list).

**Q3.**
- W1: For learners, Programs, Market pulse, Gap matrix, Check a syllabus, How it works, Your data.
- W2: For learners, Market pulse, Programs. The rest is for colleges.

**Q4.** "Learn next: Generative AI Tools, asked for in 29% of these postings and rising." Why that over things asked for twice as often? And "Electrician (ITI trade) covers Machine Learning."

**Q5.**
- W1 (come back next month): 3. Only if real data gets more SDE postings.
- W2 (send to someone in my position): 3. I'd send it to the batch group mostly to show the electrician-ML bug.

**Q6 (decoy).** "recs: +cloud,+python,+react,+genai…". Honestly I could read that, but no. 1.

**Q7.**
1. Explain "Learn next": by demand, by growth, or both. Let me sort.
2. Fix the program matching (no Electrician for ML).
3. Make real data the default for learners, and say how many postings my role has.

**Q8.** Not applicable.

---

## 9. learn-iti-trainee (learner, budget Android, Hindi first)

**Q1.** Sir ne class ke group mein link daala. Before this, for jobs, I asked seniors who went to a company in Chakan, and I saw a YouTube video about Gulf electrician jobs and what tests they take. I trust seniors. Websites I leave if it asks for login or if it's all English.

**Card line:** "budget Android, prepaid data that runs out by month end; reads Hindi best, simple English with effort."

**Q2 (phone, find what to learn next to get the job).**
1. Tap the link. "Loading Python (about 12 MB, first visit only…)". 12 MB is a lot at month end. Phone is slow. Waits, longer than 10 seconds. **SLOW.** If data were finished, **QUIT** here.
2. Yellow box, many English words. I read "Demo data" and "Real postings". I understand "real" and "demo".
3. Tabs: "Market pulse, Programs, Gap matrix, Chec". I tap "Programs". See "Electrician (ITI trade)" "74" "Partial" "borderline". **MISREAD**: I think my ITI electrician trade got 74 marks, borderline. Teacher shared this, so maybe it is about our ITI.
4. I scroll and my thumb drags the tab row, more tabs come: "For learners". I tap it. **SLOW** (found by accident).
5. "How ready am I for a job?" I understand. I see the menu says "Synthetic demo data"; box said switch to "Real postings". I want real. I change it to "Real postings: India 2026".
6. Job I want: "electrician". What I can do: "wiring, maine ITI kiya hai, motor rewinding, safety". Button "Check my readiness".
7. "29% ready for Electrician." Only 29? I feel bad. "7 postings for this job." 7 jobs? In all of India? **MISREAD**: I think there are only 7 electrician jobs, not that their data has only 7.
8. "Learn next: Problem Solving". Kaise seekhte hain problem solving? Not a thing I can do a course in. Also "PLC & Industrial Automation", I have heard that one from seniors, that is useful.
9. "Not recognised, so not counted… maine ITI kiya hai, safety". Safety not counted? We learn safety from day one. **MISREAD**: I think it means safety is not needed.
10. "None of the listed programs teaches your missing skills." So what do I do now? **STUCK.** I close it.

**Q3.**
- W1: For learners, Programs, Market pulse, Gap matrix, Check a syllabus, Your data, How it works.
- W2: For learners, Programs, Market pulse.

**Q4.** "7 postings for this job" — I'd think there are only 7 electrician jobs. And "29% ready", that I am only 29% good after two years of ITI.

**Q5.**
- W1 (come back next month): 1. Data is costly and it said only 29%.
- W2 (send to a classmate): 2. Maybe I'd forward it back in the group asking "PLC sikhna chahiye kya?"

**Q6 (decoy).** "elec_iti 74". Nothing I can understand. 0.

**Q7.**
1. Hindi language.
2. Make it light so it opens fast without eating my data.
3. Understand normal words like "safety" and tell me where I can learn PLC, not "none".

**Q8 (Hinglish).**
Last step in Hinglish: "Neeche likha 'None of the listed programs teaches your missing skills.' Matlab koi course nahi hai? Toh main kya karun? Problem Solving kahan seekhun? Bas, band kar diya."
Q5 W1 in Hinglish: "Agle mahine phir kholunga? Nahi lagta. 1. Data bhi khatam hota hai aur 29% dekh ke mood kharab ho gaya. Agar Hindi mein hota aur bataata kahan PLC seekhein, toh 4-5 de deta."
Bottom line changed? No, still 1. In Hindi I could say more clearly what would make it 4-5 (Hindi UI, a place to learn PLC).

---

## 10. prov-sceptic-owner (provider, small computer centre, phone only)

**Q1.** Government portal came, Skill India something, they asked for login, OTP, all English. I left it. Students come to my centre because they need CCC for a government job form and Tally for a shop job. Syllabus is what the board gives. I trust what my students' employers tell me, nothing else.

**Card line:** "default-no on new tools: 'students come for the certificate, not the syllabus'. Uses phone only. Will not read long text."

**Q2 (phone, check if my course teaches what jobs ask for, something to show).**
1. Open. Loading, "Python… 12 MB". Python I don't teach. Waiting. **SLOW.**
2. Yellow box, long. Skip. Big heading, long sentence. Skip.
3. "Sector: All sectors". I scroll. List of skills: "MS Excel 14%". Okay, Excel is there. I look for Tally. Not in the 15. CCC, not there. **MISREAD**: I think Tally is not asked by anybody.
4. Tap "Programs". Again long paragraph. Table: "Junior Software Developer", "Automotive Service Technician"... I don't run these. "Data Entry Operator 74" is closest. Is that my course? No, it says "(illustrative)". I don't know that word. **MISREAD**: I think it's some government course rating.
5. I see "Chec…" at the edge but I don't tap half words. There is no "my course" button that I see. **STUCK.**
6. **QUIT.** No time.

**Q3.**
- W1: Programs, Market pulse, Check a syllabus, For learners, Gap matrix, Your data, How it works. (Only saw first three; ranking the rest from names you told me.)
- W2: Market pulse, Programs, Check a syllabus. If I see "Tally" in a list of jobs, that I can show to parents.

**Q4.** "Data Entry Operator … 74 … Partial". I would think someone is giving marks to courses like mine. And the "MS Excel 14%". Only 14? Every office wants Excel. I wouldn't believe it.

**Q5.**
- W1 (come back next month): 0.
- W2 (send to another centre owner): 0.

**Q6 (decoy).** Codes and numbers. 0.

**Q7.**
1. One button: "Check my course", with ready choices like CCC, Tally, Excel, so I don't type.
2. Hindi.
3. Short. One screen, one answer, something I can screenshot and put on my WhatsApp status for parents.

**Q8.** Card doesn't say Hindi or Marathi first. Skipped.

---

## 11. prov-private-head (provider, private IT institute in Pune, laptop)

**Q1.** Six months ago three recruiters separately asked whether our data analytics batch knows GenAI tools. I added a 20-hour module and had to convince the owner. I made a slide with the recruiter names and their exact words. I trust direct recruiter feedback. I tried a couple of "skills intelligence" SaaS demos; gave up because they wanted a sales call before showing anything.

**Card line:** "Wants a quick way to justify adding a module to the owner."

**Q2 (check one of my courses, get something to show the owner).**
1. Load, fine. Banner: "synthetic". Noted; I can't show the owner synthetic numbers.
2. Market pulse quickly: "Generative AI Tools … +201%" green. Nice, but synthetic. I switch to "Real postings: India 2026". Banner: "Two quarters only… no trends." So on real data I lose the growth numbers, which were my argument. Card still says "latest four quarters". **MISREAD** for a second.
3. Check a syllabus. "Load an example" exists but I paste my own: our data analytics outline, eight modules with hours. Target roles "data analyst, business analyst, data scientist". Live chips: skills found as I type. That's good feedback.
4. "Score this syllabus". Result appears below, I scroll. **SLOW.** What my exact score is, I can't say; the material shows only the pre-filled example (51, Partial borderline). For that example: "ADD Generative AI Tools… up 306% on last year", "ADD Data Visualisation 68%", "EXPAND SQL & Databases: … given 15 h; 16 h would earn full credit."
5. I typed "SQL for reporting (30 hrs)". It says "given 15 h". **MISREAD**: I think it misread my hours; it actually split the module between SQL and Data Analysis. Nothing tells me that.
6. "REDUCE Typing Speed: only 0% of postings ask for it (at most 5%)". Good, that's the kind of line the owner likes: something to cut.
7. "Download report". This is the thing for the owner. What format it downloads, PDF, HTML, I don't know from what I've seen. I'd click it and check whether it opens on the owner's phone.
8. I'd also want to see this same result on Real postings. Whether trends show there: no, "no trends". So the "up 306%" line I wanted is synthetic-only.
9. Stop. I have half of what I need.

**Q3.**
- W1: Check a syllabus, Programs, Market pulse, Your data, Gap matrix, How it works, For learners.
- W2: Check a syllabus, Your data, Market pulse. I'd want to upload the postings our placement cell collects; that makes it real for the owner.

**Q4.** "SQL & Databases: asked for in 79% of postings but given 15 h". I gave 30 h. If I show that to the owner and he sees 30 in our syllabus, I look careless. And "up 306% on last year" vs "+201%" on the front page: which one do I quote?

**Q5.**
- W1 (come back next month): 7. I rewrite syllabi twice a year; this would be part of that.
- W2 (send to someone in my position): 6. Other academic heads in Pune, yes, with a warning about synthetic data.

**Q6 (decoy).** "recs: +cloud,+python…" I'd get the gist but I can't show the owner that. 2.

**Q7.**
1. Growth trends on real data. Without "up X% on last year" from real postings, I have no argument.
2. Show how my module hours were split, so "given 15 h" matches what I typed.
3. A one-page download I can forward as is, with the data source written on it.

**Q8.** Not applicable.

---

## 12. prov-placement-officer (provider, polytechnic TPO, laptop)

**Q1.** Last year the HoD asked "what do recruiters want?" I took my Excel of 40 recruiters, typed each one's requirements into a column, made a pivot table by hand, pasted the chart into a Word doc and mailed it. Took two evenings. I trust my own sheet because I know each row. I'd trust a website if its list looks like my sheet.

**Card line:** "wants to show HoD which skills recruiters ask for. Downloads reports into Word to forward."

**Q2 (check a course against jobs, get something for HoD).**
1. Load, banner "synthetic". Okay, so it's a demo.
2. Market pulse. "Most demanded skills": "Workplace Safety 23%, Communication 18%, Python 16%, MS Excel 14%…" That's the pivot table I made by hand. Good. Filter District / city; I pick my district. Which 12 districts are in the list I can't say from what I've seen; if mine isn't there, I pick the nearest. **SLOW.**
3. I want this list in Word. Is there a download on this page? I don't see one; the "Download report" button is only on a program or syllabus report. **STUCK** for exporting the market list. I'd screenshot it.
4. Clicking "Workplace Safety" opens a trend card at the bottom. I didn't see it open; scrolled to find it. **SLOW.** "95% range ." with nothing after. Looks broken in a document for HoD.
5. Your data: "Upload your own and every score on the site is recomputed from them." This is what I want: my recruiter Excel. Required columns "title, date, description and/or skills". My sheet has company, role, skills, CTC, no date per row. "At least eight quarters give trends; fewer still give shares and scores." I'd have to add a date column. **SLOW.** Also it needs CSV; I'd have to "Save as CSV", fine.
6. "Download the sample CSV" — I'd download that and copy my rows into it.
7. Programs → Electrician (ITI trade): "Partial borderline". Our diploma is not ITI; none of the ten programs is a polytechnic diploma. **MISREAD (mild)**: thought "ITI-style trade course" might stand for our diploma.
8. Stop; I'll try the upload another day.

**Q3.**
- W1: Market pulse, Your data, Programs, Check a syllabus, Gap matrix, For learners, How it works.
- W2: Your data, Market pulse, Check a syllabus. My own data first; then the skills list for HoD.

**Q4.** "95% range ." — a blank, looks like an error, can't forward it. "Workplace Safety 23%" at the top of the list: my recruiters are IT and manufacturing, safety is never the first thing they say. I'd suspect the synthetic data.

**Q5.**
- W1 (come back next month): 5. If the upload works with my sheet.
- W2 (send to another TPO): 4.

**Q6 (decoy).** Codes. I'd need a legend before I could even read it. 1.

**Q7.**
1. A download button on Market pulse (Word or Excel) for the skills list with my filters.
2. Let me upload my recruiter sheet without dates, or say exactly what changes without them.
3. Fix the blank range and make the trend card open where I clicked.

**Q8.** Not applicable.

---

## 13. prov-ngo-coord (provider, NGO in Nagpur, Android, Hindi first)

**Q1.** For the CSR funder's monthly report I make a chart in Google Sheets on my phone: enrolled, completed, placed, by course. Last quarter the funder asked "are retail jobs still there in Nagpur?" I asked our placement partner and two shop managers on WhatsApp, and wrote it in two lines. I trust things I can put a source to. I give up on anything that needs a laptop.

**Card line:** "Reports placement numbers to a CSR funder monthly. Would love a chart to put in the funder report."

**Q2 (phone, check my retail / data entry / GDA courses, get a chart for funder).**
1. Load 12 MB on mobile data. **SLOW.**
2. Yellow box: "synthetic… not facts about real jobs". Then I cannot put anything from this in a funder report. Hmm.
3. Programs (one of the tabs I can see). "Retail Sales Associate 54 51–59 Partial 49 ↓", "Data Entry Operator 74", "General Duty Assistant 84 Strong". These are exactly our three courses! **MISREAD**: I think it has scored PMKVY courses like ours. "(illustrative)" I read as "example", but I still think it's the standard PMKVY version. On phone, only three columns, no bars.
4. Tap Retail Sales Associate. Report appears below; I scroll a long way. **SLOW.** "Download report" — on the phone, I don't know what file it gives or whether I can open it.
5. "49 ↓" next year. **MISREAD**: I think retail jobs are falling; funder will panic. It's "if unchanged".
6. I want Nagpur. District / city filter on Market pulse. Whether Nagpur is among the 12 districts I don't know from what I saw. I select it if there.
7. I switch to "Real postings" because funder needs real. Programs: "Retail Sales… Too few postings", "General Duty Assistant 0", "Unscored". Two of my three courses can't be scored with real data. **STUCK** for the funder chart.
8. Market pulse bar chart is nice but synthetic. I screenshot nothing. Stop.

**Q3.**
- W1: Programs, Market pulse, Gap matrix, Check a syllabus, For learners, Your data, How it works.
- W2: Programs, Market pulse, Check a syllabus.

**Q4.** "49 ↓" under NEXT YEAR for Retail Sales Associate. I'd tell the funder retail is declining, which isn't what it means. Also "General Duty Assistant … 0" in real postings, as if there are no hospital jobs; they're just not in this data.

**Q5.**
- W1 (come back next month): 3. Only if real data for Nagpur trades comes.
- W2 (send to someone in my position): 2.

**Q6 (decoy).** "gda_05 84". I wouldn't know which is mine. 1.

**Q7.**
1. Real job data for my courses and city, or tell me clearly it can't do retail/GDA yet.
2. A simple chart image I can download on phone and paste into the funder report, with the source written under it.
3. Hindi, and short words instead of "borderline", "illustrative", "synthetic".

**Q8 (Hinglish).**
Last step in Hinglish: "Real postings pe switch kiya kyunki funder ko asli data chahiye. Retail Sales mein 'Too few postings', GDA mein 0, 'Unscored'. Toh mere teen mein se do course ka score hi nahi aata. Funder report mein kya daalun? Chhod diya."
Q5 W1 in Hinglish: "Agle mahine wapas? 3 out of 10, agar Nagpur ka asli data aaye toh. Abhi toh synthetic hai, funder ko nahi dikha sakti."
Bottom line changed? No. Still 3.
