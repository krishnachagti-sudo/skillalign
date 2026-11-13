import json, random
G = "All facts here are [guess]: no real conversation stands behind any card (n real = 0)."
cards = [
 # faculty
 ("fac-pl-prof", "faculty", False, {"device":"laptop","tech":"high","focus":"code"},
  "Assistant professor who teaches Introduction to Programming Languages; 40s; evaluates ~15 team projects in two days, 10-12 min each, on own laptop. Grades: working demo, code quality, whether each student can explain their part, use of language features. Has seen many dashboards that look good and hide nothing behind them. Reads English comfortably; low patience for statistics jargon he did not teach. Last time: cut marks from a team whose demo crashed on load."),
 ("fac-ta-phd", "faculty", False, {"device":"projector","tech":"high","focus":"demo"},
  "PhD student TA who sits in on project demos and pre-scores them on a rubric sheet; late 20s; does the evaluation from the projected screen in a lab, not on own machine. Cares whether the demo story is clear in 5 minutes and whether numbers on screen are explained. Comfortable with Python and stats. Last time: flagged a team whose charts had no units."),
 ("fac-hod-sceptic", "faculty", True, {"device":"laptop","tech":"medium","focus":"rigour"},
  "Senior professor on the evaluation panel; 55; default stance is that student projects overclaim. Asks 'where is the real data, who would use this, what did YOU write'. Distrusts anything that looks like a template or AI-generated. Uses a laptop but not fluent with browser dev tools. Last time: gave low marks to a polished project that could not answer where its numbers came from."),
 ("fac-external", "faculty", False, {"device":"phone","tech":"medium","focus":"impact"},
  "External examiner from industry (a mid-size IT services firm's L&D manager) invited for the final viva; 38; opens the project link on his phone before the session from WhatsApp. Cares about whether the tool would help a real training manager; impatient with academic language. Last time: told a team their dashboard needed a 'so what' on the first screen."),
 # sih judges / officials
 ("judge-dvet-official", "judge", False, {"device":"desktop","tech":"low","focus":"policy"},
  "Deputy director-level official in a state skills department (DVET-type); 50; Marathi first language, reads English official documents fine. Uses office desktop with Chrome; prints anything important. Wants: which ITI courses need curriculum change, district-wise. Thinks in NSQF levels, QP codes, NCVT trades. Last time: was shown a dashboard by a vendor and asked for 'one page I can put in a file note'."),
 ("judge-sih-industry", "judge", False, {"device":"laptop","tech":"high","focus":"novelty"},
  "Hackathon jury member from an edtech startup; 32; sees 30 teams in a day, 7 minutes each, laptop. Scores novelty, feasibility, impact, UI polish, demo smoothness. Expects a crisp landing message and a 'wow' visual. Last time: rated down a team whose first screen was a wall of text."),
 ("judge-sceptic-stat", "judge", True, {"device":"laptop","tech":"high","focus":"rigour"},
  "Jury member who is a labour economist at a policy think tank; 45; default-no on dashboards that score things. Suspects job postings mis-measure vocational demand and that a single 'alignment score' hides judgement calls. Reads every footnote. Last time: asked a team to show the exact formula behind a score and they could not."),
 ("judge-nsdc-pm", "judge", False, {"device":"phone","tech":"medium","focus":"scale"},
  "Programme manager at a sector skill council; 35; reviews submissions on phone between meetings, then laptop for shortlisted ones. Cares about whether QP/NOS codes are used, whether training partners could self-serve. Hindi and English. Last time: shortlisted a tool because it let a training partner upload their own data."),
 # providers
 ("prov-iti-principal", "provider", False, {"device":"desktop","tech":"low","lang":"marathi"},
  "Principal of a government ITI in a district town (e.g. Jalgaon); 52; runs 8 NCVT trades; curriculum is set centrally, he can add short add-on modules. Uses office desktop and WhatsApp; English reading is slow, Marathi preferred. Hears from placement officer that local MSMEs want electricians who know PLCs. Has never uploaded a CSV."),
 ("prov-private-head", "provider", False, {"device":"laptop","tech":"high","lang":"english"},
  "Academic head of a private IT training institute in Pune; 34; runs data analytics and full-stack batches of 30; rewrites syllabus every 6 months based on what placed students say. Comfortable with Excel and Google Sheets. Wants a quick way to justify adding a module to the owner. Last time: added a GenAI module after three recruiters asked."),
 ("prov-ngo-coord", "provider", False, {"device":"phone","tech":"medium","lang":"hindi"},
  "Programme coordinator at an NGO running short PMKVY-style courses (retail, data entry, GDA) for young women in Nagpur; 29; works almost entirely on an Android phone; Hindi first, English okay for reading. Reports placement numbers to a CSR funder monthly. Would love a chart to put in the funder report."),
 ("prov-sceptic-owner", "provider", True, {"device":"phone","tech":"low","lang":"hindi"},
  "Owner of a small computer training centre (CCC, Tally, basic Excel) in a tier-3 town; 46; default-no on new tools: 'students come for the certificate, not the syllabus'. Uses phone only. Will not read long text. Last time: ignored a government portal because it needed a login and English."),
 ("prov-placement-officer", "provider", False, {"device":"desktop","tech":"medium","lang":"english"},
  "Training and placement officer at a polytechnic; 40; keeps an Excel of recruiters and their requirements; wants to show HoD which skills recruiters ask for. Downloads reports into Word to forward. Last time: made a pivot table of recruiter demands by hand."),
 # learners
 ("learn-iti-trainee", "learner", False, {"device":"phone","tech":"low","lang":"hindi"},
  "Second-year ITI electrician trainee; 19; budget Android, prepaid data that runs out by month end; reads Hindi best, simple English with effort. Wants a job in a factory or a Gulf placement. Found the link because a teacher shared it on the class WhatsApp group."),
 ("learn-bcom-grad", "learner", False, {"device":"phone","tech":"medium","lang":"english"},
  "BCom graduate, 22, in Nashik, applying for data analyst and MIS executive roles; knows Excel well, a little SQL from YouTube. Uses phone mostly, laptop at a cyber cafe sometimes. Wants to know what to learn next in 2 months."),
 ("learn-btech-fresher", "learner", False, {"device":"laptop","tech":"high","lang":"english"},
  "Final-year BTech CSE student, 21, a classmate of the team's batch elsewhere; uses laptop; wants a software developer job; will try to break the tool by pasting their resume."),
 ("learn-sceptic-switcher", "learner", True, {"device":"phone","tech":"low","lang":"marathi"},
  "Woman, 31, returning to work after a 6-year break; had done a data entry course; Marathi first language; sceptical of websites that 'score' people, worried it will say she is not good enough. Phone only. Would quit at the first unclear screen."),
 ("learn-diploma-auto", "learner", False, {"device":"phone","tech":"medium","lang":"marathi"},
  "Diploma in automobile engineering, 20, Kolhapur; working at a two-wheeler service centre; hears EVs are coming and wants to know if he should do an EV course. Phone, Marathi and some English."),
]
bank = [{"id":i,"segment":s,"sceptic":sc,"holdout":False,"cell":c,"card":t+" "+G} for i,s,sc,c,t in cards]
# frozen holdout: ~30%, drawn at random within each segment, sceptics never the only sceptic of a segment
rnd = random.Random(20261113)
for seg in sorted({c["segment"] for c in bank}):
    pool = [c for c in bank if c["segment"]==seg and not c["sceptic"]]
    k = 1 if len(pool) <= 3 else 2 if seg=="learner" else 1
    for c in rnd.sample(pool, k): c["holdout"] = True
json.dump(bank, open("bank.json","w"), indent=1, ensure_ascii=False)
for c in bank: print(c["id"], c["segment"], "SCEPTIC" if c["sceptic"] else "", "HOLDOUT" if c["holdout"] else "")
print(len(bank), "cards;", sum(c["holdout"] for c in bank), "holdout;", sum(c["sceptic"] for c in bank), "sceptic")
