# Round 2 holdout interviews (model: sonnet). 5 personas x v1 and v2 = 10 sessions

All persona facts are [guess]; n real = 0. These are simulated screening answers, not user data. Each of the 10 sessions was answered separately.

---

# 1. fac-pl-prof (faculty) 

Card line that shapes use: "Has seen many dashboards that look good and hide nothing behind them." (Also: "Last time: cut marks from a team whose demo crashed on load.")
Task: "You have 10 minutes to decide how good this project's interface is and what to ask the team."

## v1

**Q2 walkthrough**
1. I open the link on my laptop. A spinner and "Starting the Python engine in your browser. Loading Python (about 12 MB, first visit only; later visits work offline)…". My first reaction is: demo risk. If this were on a projector over college wifi I would mark them down. Here it is a few seconds, so I wait. SLOW (not a defect, but it is the exact thing that cost the last team their marks).
2. Page loads: "Are skill programs teaching what jobs ask for?" and a yellow banner "Demo data. These job postings are synthetic…". Fine, honest. I like that they say it. Then four tiles: "70.9 average program alignment here (out of 100)". Alignment of what with what? I did not teach statistics, I do not want to decode this. MISREAD: I read 70.9 as a grade of the whole system, it is an average across ten made-up programs.
3. "Most demanded skills" list, grey change numbers. I click Python, skill trend opens "at the bottom of the page", I see nothing change on screen at first and think the click failed. SLOW. When I scroll down I find the chart and the line "The dashed line is a straight-line forecast four quarters ahead: 26%, 95% range ." with the range blank. That is a visible bug. It tells me they did not test the output. I note it as a question for the team.
4. Programs tab. "Training programs, scored against the jobs they train for". Table is clear enough, but "SCORE AND RANGE", "HOURS ON DEMAND 100%" for a program scored 43 Weak confuses me: 100% of hours on demand yet weak? MISREAD. I click Junior Software Developer; the report opens below the whole table; I click again thinking nothing happened, then scroll. SLOW.
5. I try "Check a syllabus" because that is where I can test it myself. Pre-filled text, I press "Score this syllabus". Result: "SQL & Databases: asked for in 79% of postings but given 15 h". I typed (it was pre-filled) 30 hrs. This is wrong on its face and I would stop here: a number on screen contradicts the input. MISREAD / trust break. I would ask the team how the split works. That is the best question I find, it tests whether they understand their own code.
6. I stop around minute 8: I never read "How it works" (long prose, Mantel-Haenszel, Bonferroni; I would skim and ask them to explain it).

**Q4 trust**: "SQL & Databases: asked for in 79% of postings but given 15 h; 16 h would earn full credit." I gave 30 hrs, so I would not believe it without an explanation. Also "6 of 10 programs below Strong here" is built on made-up programs.

**Q5 w1** (chance I'd rate the UI good or better): 4. Interesting content, but blank forecast range, a number that contradicts the input, and click-then-scroll behaviour. 
**Q5 w2** (full marks for usability): 1.

**Q7 fixes**
1. Fix the blank forecast range and the 15 h vs 30 h display, because bugs in the shown output are what I grade down.
2. Open reports next to the thing I clicked, not below a long table.
3. Say what "alignment" and "95% range" mean in one plain line next to the first number.

## v2

**Q2 walkthrough**
1. Page appears at once; small line "Loading the SkillAlign engine and job postings…". Good. For my purposes this is the fix that matters, I can talk while it loads. No problem.
2. Home: "Do skill courses teach what jobs ask for?" and "On the practice data, 6 of 10 example courses miss skills that their own jobs ask for. Check yours in a minute." Three buttons. I know in five seconds what the project is. Good.
3. "Check my course". Form is shorter. I leave the pre-filled text and press "Check this course". Result right under the form: "It teaches about 51% of what these jobs ask for, so it is partial. It misses 5 of 9 skills… Likely between 49 and 53 (that range crosses a grade line, so the grade is borderline)." I can read this. Better than tiles.
4. "Show 6 more changes" and the Expand line: "SQL & Databases: asked for in 79% of job ads but given 15 h; 16 h would earn full credit (its 30 h module "SQL for reporting" is shared with Data Analysis)." Now the contradiction is explained. But I note: the program splits hours evenly across two skills, that is a design choice, not a law. I would ask the team why, and that is a good viva question.
5. I open "How it works" and see the grey box "The course score in one line" with the formula. I can now ask each student to derive it. 
6. Where I stop: I look for who wrote which part, there is nothing, "There is no 'who built what' team section" (I only know this because there is no link; not that I looked in the footer carefully). For my grading I need to know whom to ask. SLOW, not a UI failing but it affects me.

**Q4 trust**: "6 of 10 example courses miss skills that their own jobs ask for" is on made-up courses and made-up ads; the home page leads with it. The orange "Practice data" pill does flag it but I would still want the sentence to say "made up".

**Q5 w1**: 7. 
**Q5 w2**: 3. Still 12 MB, still no team section, I would not give full marks to anything with a demo-dependency on a first load.

**Q7 fixes**
1. Add a "who built what" section so I can direct questions.
2. Put the practice-data label inside the headline sentence, not only in the pill.
3. Show how the hour-split is decided right next to "given 15 h".

---

# 2. judge-dvet-official (judge)

Card line: "Wants: which ITI courses need curriculum change, district-wise." (and "asked for 'one page I can put in a file note'")
Task: "You have 7 minutes with this site before scoring it."

## v1

**Q2 walkthrough**
1. Office desktop, Chrome. Spinner "Starting the Python engine in your browser." I wait, a little irritated, the vendor dashboards never made me wait.
2. "Are skill programs teaching what jobs ask for?" Yes, that is my question. Banner: "Demo data. These job postings are synthetic… so the numbers are not facts about real jobs." So I am looking at invented numbers. I note it. For scoring a prototype that is acceptable but I cannot use any number.
3. Four tiles and then "Most demanded skills". "Workplace Safety 23%". District / city filter is there, 12 Maharashtra districts. Good, but it filters postings, not courses. I select Jalgaon-type district; I cannot tell what it does to the courses. I go to Programs.
4. Programs: "Junior Software Developer (Private training institute (illustrative)…". My ITI trades are "Electrician (ITI trade) 74 69–80 Partial borderline" and "Automotive Service Technician (ITI trade) 52 44–62". "(illustrative)" means invented. MISREAD risk: I first read 74 as a percentage pass mark or NSQF level, then see "out of 100". "borderline" in a small pill, I do not know whether it is good or bad. No district-wise view of courses. STUCK on my main question: there is no list of "which course needs change in which district".
5. I look for something to print. "Download report" on the report that opens below. I do not know the format. SLOW. I try Chrome print on the page, 24-column Gap matrix with rotated headings is unusable on paper.
6. Check a syllabus has "NSQF level (optional)" and "Qualification pack code (optional)". Good sign that they know my vocabulary. I do not test it.
7. Stop at minute ~7. I would not read "How it works", it is a long page with names of tests I do not know.

**Q4 trust**: "70.9 average program alignment here (out of 100)". I would not trust the average of ten invented programs, and "alignment" is not a word in my file notes. Also "Weak" / "Strong" cut lines are not explained on that page.

**Q5 w1** (chance I'd rate the UI good or better): 4. Right question, wrong shape for me: nothing I can print or put in a file note, nothing district-wise per course.
**Q5 w2**: 2.

**Q7 fixes**
1. A district-wise list of courses with "needs change / does not need change" in plain words.
2. One printable page per course.
3. Mark NSQF level and QP code on the results, not only as optional boxes.

**Q8 Hinglish/Marathi-mix** (Roman script, Hindi-Marathi-English mix): "Last step: print karne ki koshish kiya, 'Download report' dikha lekin kaunsa format pata nahi, aur matrix kagaz pe nahi aata. Q5: chance ki main isko good bolun... 4. District-wise course list nahi hai, isliye file note nahi banta." Bottom line did not change: 4.

## v2

**Q2 walkthrough**
1. Page appears at once. "Do skill courses teach what jobs ask for?" and "6 of 10 example courses miss skills that their own jobs ask for." Plain English, good. Orange pill "● Practice data ▾", I understand it is not real: "These 2,216 job ads are made up".
2. Three buttons. I choose "See the job market" because I want district-wise. It has "Sector" and "District / city" filters and three tabs: "Skills in demand", "Example courses", "Gaps". The grey line "These are made-up example courses, not real institutes." Good, it is honest, but then I cannot use it for decision. Same STUCK as before: there is no per-district course list; "Example courses" has a district filter above it but I cannot tell whether it changes the course scores. MISREAD possibility.
3. Open Electrician (ITI trade): "It teaches about 74% of what these jobs ask for, so it is partial. It misses 3 of 7 skills… Likely between 69 and 80 (that range crosses a grade line, so the grade is borderline)." I can put this sentence in a file note. 
4. "Print or save as PDF" button right there. Good. I do not try it, but I believe it, it says "prints only that report".
5. "Check my course" shows a fold "Add NSQF level or QP code (optional)" with the note "These are printed on the report for your records. SkillAlign does not look them up." Slight disappointment: I wanted it to know my QP codes. But it is honest. 
6. Gaps tab: on desktop the grid. I do not read it.

**Q4 trust**: "Likely between 69 and 80 (that range crosses a grade line, so the grade is borderline)." I understand it, but I would not trust that anyone can score a trade course from invented job ads; and "Example course (made up)" makes me ask what the real result would be. 

**Q5 w1**: 6. 
**Q5 w2**: 3. Missing district-wise, and NSQF not looked up.

**Q7 fixes**
1. District-wise table of real ITI trades vs local jobs.
2. Look up NSQF level and QP code instead of only printing them.
3. A real-data mode with trade jobs; real mode has "very few vocational jobs".

**Q8 Hinglish-mix**: "Last step: 'Print or save as PDF' dikha, ye theek hai, file note ke liye ek page mil jata hai. Q5: 6, but district-wise nahi hai to full marks nahi." Bottom line unchanged (6). 

---

# 3. prov-iti-principal (provider)

Card line: "Hears from placement officer that local MSMEs want electricians who know PLCs." (and "Has never uploaded a CSV", "English reading is slow, Marathi preferred")
Task: "Check whether one of your own courses teaches what jobs ask for, and get something you could show your boss or funder."

## v1

**Q2 walkthrough**
1. Office desktop. Spinner with English text "Loading Python (about 12 MB…". I do not know what Python has to do with me; I wait because the link came from someone.
2. Market pulse. Big heading "Are skill programs teaching what jobs ask for?" That is my question, I stay. The yellow banner "These job postings are synthetic" makes me ask: so is any of this real? I do not read the rest of it. Tiles with numbers: I read "70 different skills found in them" and nothing else.
3. I do not know which tab is my course. I look at tab names: "Programs", "Gap matrix", "Check a syllabus". "Programs" sounds right; I see "Electrician (ITI trade) 74 69–80 Partial borderline". I think: 74, passed? Then "borderline", then "next year 71 ↓". MISREAD: I read 74 as my ITI's actual result. It is an illustrative course, not mine, ("(illustrative)" printed in small grey text I did not read).
4. I want to put in my own course. "Check a syllabus": the form is in English, "Target roles: comma separated, as they appear in job titles (at least 3 letters each)" — what are job titles? The box already says "data analyst", not electrician. SLOW. "Qualification pack code (optional)", I know the NCVT code but not a QP code for this. "Add [mandatory] to modules the curriculum requires" — my curriculum is all set centrally, so I think everything is mandatory, but I am not sure how to type it, 8 trades of text. I would send this to my instructor. QUIT likely at this step: I type "electrician" and paste two lines, and I might get a result; but if it shows "ADD Generative AI Tools" for an electrician course I would not believe it.
5. If I got a result: "REDUCE Typing Speed: only 0% of postings ask for it (at most 5%)" language is about "postings" and "95% range", which I do not read. I want one line: "add PLC module of 40 hours". It does not tell me that.
6. To show boss or funder: "Download report". I do not know what format, I would take a photo of the screen on my phone and send it by WhatsApp.

**Q4 trust**: "Not recognised, so not counted (if these are skills, readiness is understated)" or the "(illustrative)" label; and "Partial borderline". I would not understand "borderline". 

**Q5 w1** (chance I'd come back in the next month): 3. If my placement officer sits with me, maybe, but alone I would not.
**Q5 w2** (send link to another principal): 2.

**Q7 fixes**
1. Marathi, or at least very simple English, with an Electrician example I can open and edit.
2. A box that says what to type for an ITI trade, with PLC as an example.
3. A button that gives me one page in print format for the file.

**Q8 Hinglish (Marathi-English mix in Roman)**: "Last step: report dikhane ke liye 'Download report' hai, par format nahi pata; mi WhatsApp var screenshot pathavin. Q5: ... 4." Changed slightly, 3 to 4, because the language is easier, but the bottom line is the same: I would not use it alone.

## v2

**Q2 walkthrough**
1. Page comes up quickly. Heading "Do skill courses teach what jobs ask for?" and button "Check my course: Paste a syllabus. See which skills jobs want that it misses. For trainers, ITIs and institutes." That says ITIs, I click it. No hunting. 
2. Form: "Course name", "Jobs this course trains for", hint "comma separated, as they appear in job ads, e.g. "data analyst, MIS executive"". I replace it with "electrician, wireman". Syllabus box: I paste my module list. Hours I add ("with hours"). "[mandatory]" hint: "Write [mandatory] after modules you are not allowed to drop." I understand this, my modules are set centrally, so I do it on the core ones. SLOW, I am typing, English slow, but I do not stop.
3. Green chips under the box "Skills found as you type: …" — I like this, I see it read my words. But if "Motor winding" is not a chip I would think it did not read. Not sure what it will show for my modules.
4. Press "Check this course" — result under the form: big number with "It teaches about …% of what these jobs ask for, so it is partial." I can read this sentence. Then "What to change, most important first": top three. If PLC is in there I am happy. I do not know whether it will be, because with electrician data there were only "121 job ads" in the practice set, and in real data electrician has 16 postings so it cannot be scored. MISREAD risk: "Practice data" pill; I would not know the result is from invented ads.
5. "Print or save as PDF". I can print it for my boss. I do not read "Skill by skill" ▾.
6. The NSQF fold: I open it, I know my NCVT/NSQF level, I type it. "SkillAlign does not look them up", fine.

**Q4 trust**: "Compared with 121 job ads for: electrician, electrical technician… · Practice data". If the ads are made-up I cannot show it to my funder. Also "borderline" again.

**Q5 w1**: 6. I may well come back when the placement officer pushes for PLC modules.
**Q5 w2**: 5. I would send it to another ITI principal I know, but not before it is in Marathi.

**Q7 fixes**
1. Marathi version of at least the Check my course page.
2. Real Jalgaon / Maharashtra electrician ads, not made up.
3. A line that says which short add-on module to add, with hours.

**Q8 Hinglish-mix**: "Last step: 'Print or save as PDF' kiya aur boss ko dikhaya jaa sakta hai. Q5 w1: 6." Bottom line unchanged.

---

# 4. learn-bcom-grad (learner)

Card line: "Wants to know what to learn next in 2 months." (and "Uses phone mostly, laptop at a cyber cafe sometimes")
Task: "Find out what you should learn next to get the job you want."

## v1 (phone)

**Q2 walkthrough**
1. Open on phone, 4G in Nashik. Spinner, "Loading Python (about 12 MB…". I would wait maybe 20 seconds. If it hung I would close. SLOW.
2. Top of the page: logo, a dropdown, "2,216 postings · 2024-Q4 to 2026-Q3", then tab row "Market pulse | Programs | Gap matrix | Check…". Then a yellow box taking half the screen: "Demo data. These job postings are synthetic…". I do not read all. I think: demo, so fake? 
3. I scroll Market pulse: I see "Python 16% +28%", "MS Excel 14%", "SQL & Databases 12%". That actually interests me, I know Excel, I am learning SQL. But I want "data analyst". I am looking for the tab. The tab row is cut after "Check…". I did not know it could scroll. If I had not tried swiping I would have used "Programs" instead, a list of courses I cannot enrol in. STUCK for a while, SLOW if I swipe. I swipe by chance (I am used to horizontal chips).
4. "For learners": "How ready am I for a job?" I type job "data analyst" (start typing, picks). In "What I can do" I put my Excel, SQL line. Press "Check my readiness".
5. Result: "37% ready for Data Analyst." And "Learn next: Generative AI Tools, asked for in 29% of these postings and rising." Hmm. My job is MIS executive, I need Power BI or Python first; Generative AI is a buzzword. MISREAD: I read the 37% as "your chance of getting the job". It says "Weighted by how often each skill appears in 173 postings for this job". 
6. Red/green chips: "✗ Data Analysis 75%" is the one I must learn, and I do see it. But the "learn next" line says something else. Confusing. Then "Programs that close your gaps": "2 YEARS Electrician (ITI trade) covers Machine Learning." That looks like a joke to me. I would stop trusting the page. 
7. I would stop here and Google "data analyst skills".

**Q4 trust**: "2 YEARS Electrician (ITI trade) covers Machine Learning." A wiring course does not teach ML. Also "37% ready" I would believe as chance of getting a job, which is not what it says.

**Q5 w1**: 4. 
**Q5 w2** (send to someone like me): 4. A friend who is also a BCom grad wanting MIS jobs, perhaps; but not with the bug in programs.

**Q7 fixes**
1. Put "For learners" first or make the tabs visible on the phone.
2. "Learn next" should be the basic skill in my 2 months (Data Analysis / Power BI), not a trend.
3. Show real course names or links where I can learn it.

## v2 (phone)

**Q2 walkthrough**
1. Page appears instantly, thin line "Loading the SkillAlign engine and job postings…". OK. 
2. Home: "Do skill courses teach what jobs ask for?" Three big buttons. Which one is mine: "What should I learn?" "Pick the job you want and say what you know. See the one skill to learn next." That is it. I tap it. At the bottom there is also a bar "Home · My course · Learn next · Market". Easy.
3. "The job I want": the box has "data analyst" pre-filled; I change to "MIS executive" ... I do not know if it exists in the list. If no match I would pick "data analyst", fine. "What I already know": I type "Excel, basic SQL, communication", press "Show what to learn".
4. Green box: "LEARN NEXT · Data Analysis · asked for in 75% of these job ads." Clear. This is what I wanted. 
5. Ring "37% ready for Data Analyst. Based on the skills in 173 job ads for this job, weighted by how often each is asked for. This is about skills on paper, not about you." Good, I no longer read it as my chance. 
6. "Courses that teach what you are missing": "Data Analytics Foundation [example course] built for this job". I wanted to enrol; "example course" means no. SLOW/MISREAD, I think it is a real course until I read the grey tag. The 4-month duration is longer than my 2 months.
7. The orange pill "● Practice data": "These 2,216 job ads are made up". So all the numbers are made up? I would not know whether to tap "Switch to real job ads". If I did I would get fewer ads.
8. Stop here: I know what to learn; I go to YouTube for it.

**Q4 trust**: "asked for in 75% of these job ads" — because the pill says the ads are made up. Also "37% ready", "on paper".

**Q5 w1**: 7. 
**Q5 w2**: 6.

**Q7 fixes**
1. Real jobs by default for this journey, not "practice data".
2. Real courses or YouTube-type links for "Data Analysis" within 2 months.
3. A simple 2-month order: first this, then this.

---

# 5. learn-diploma-auto (learner)

Card line: "hears EVs are coming and wants to know if he should do an EV course." (and "Phone, Marathi and some English.")
Task: "Find out what you should learn next to get the job you want."

## v1 (phone)

**Q2 walkthrough**
1. Phone, Kolhapur, mobile data between service jobs. Spinner "Loading Python (about 12 MB, first visit only…". 12 MB is a lot for my data pack. SLOW, almost QUIT; I wait because a friend sent the link.
2. Page: "Are skill programs teaching what jobs ask for?" Long English. Yellow banner "Demo data. These job postings are synthetic, generated to show how the method works". I do not know "synthetic". I guess "demo". 
3. I scroll. I see "Emerging... Rising by 30% or more, beyond chance, and within the same job roles." Then "Battery Management Systems", "EV Maintenance +102%". EV Maintenance, that I know! But I do not understand "beyond chance". MISREAD: I think +102% means the salary doubles or EV jobs doubled. Actually it is the share of postings, and it is synthetic data.
4. I do not know which tab is for me. Tabs after "Gap matrix" are cut off. I tap "Programs": rows like "Automotive Service Technician (ITI trade) 52 44–62 Partial borderline". 52? Out of what? Phone shows only 3 columns "PROGRAM, SCORE AND RANGE, NEXT YEAR". I think my course is weak, next year 31 ↓ means it is going to be useless. MISREAD: it means the invented course would score lower next year if unchanged. It scares me. 
5. I try Gap matrix on the phone: two columns visible, need sideways drag. STUCK. I leave.
6. I never reach "For learners".

**Q4 trust**: "Automotive Service Technician (ITI trade) 52 44–62 Partial borderline · 31 ↓". I would believe I am going to be out of work; I would also not trust it since I do not know it is invented.

**Q5 w1** (come back in next month): 3. 
**Q5 w2** (send to a friend in my position): 3.

**Q7 fixes**
1. First screen should say "Should I do an EV course?" in Marathi/simple words.
2. Fewer numbers and a plain yes/no/what to learn.
3. Make the tab row clear on the phone.

**Q8 Hinglish/Marathi-mix**: "Last step: Programs madhe '31 ↓' baghun mala vatla maza course band hoil, mag Gap matrix var jaun sideways ओढायला जमलं nahi. Q5: 3." Bottom line unchanged: 3 (my honest guess, I am not sure of a difference).

## v2 (phone)

**Q2 walkthrough**
1. Page appears at once, small grey loading line. Good for my data, I can read while it loads.
2. "Do skill courses teach what jobs ask for?" Under it "Rising fastest: Battery Management Systems, up 213% on last year". Battery, EV, yes this is about me. I do not understand "Battery Management Systems" fully but EV is in my head.
3. Three buttons. I tap "See the job market" (the "What should I learn?" one asks me to pick a job, I do not know the job title for EV). Then three tabs "Skills in demand | Example courses | Gaps". I go to "Gaps": a list: "Automotive Service Technician (ITI trade): EV Maintenance 66%, Electrical Wiring 22%". Now I understand: the car-mechanic course lacks EV maintenance, which 66% of ads ask for. 
4. I do not know "ads" are made up until I tap the "● Practice data" pill: "These 2,216 job ads are made up". So is 66% real? No. I stop and ask: then what do I do? There is the "Switch to real job ads" link; I do not know if I should. (If I did, there are 0 automotive postings in the real set; I would not know that.) MISREAD risk.
5. I try "What should I learn?" anyway, typing "service" in "The job I want" and picking if something comes. I do not know what the list holds. If there is nothing I stop.
6. "Look for a short course in … on Skill India Digital or at your nearest ITI." (that line appears only when no example course fits). Fine, a direction.
7. Stop. I would show the Gaps list to my senior at the service centre.

**Q4 trust**: "EV Maintenance 66%" while the pill says the ads are made up. Also "Battery Management Systems … up 213%" is a made-up figure on the home page.

**Q5 w1**: 7. 
**Q5 w2**: 6.

**Q7 fixes**
1. Real automobile/EV jobs in the data, with a clear "real" label.
2. Marathi.
3. A direct answer: "Should I do an EV course: yes/no and which one near Kolhapur".

**Q8 Hinglish/Marathi-mix**: "Last step: Gaps list madhe 'EV Maintenance 66%' disla, mala samajla ki mazya course madhe EV nahi. Q5: 7." Bottom line unchanged.
