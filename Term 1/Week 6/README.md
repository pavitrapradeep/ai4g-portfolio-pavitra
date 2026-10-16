# Term 1 - Week 6: Language Models

---

## 1. Homework & workshop assignments -> [`homework/`](homework/)

**What was the assignment?**

**What did I hand in?**
_List the files, or link to them. Notebook exports, screenshots, scripts._

**What did I find difficult, and how did I solve it?**

### Checklist
- [ ] My workshop / homework files are in `homework/`
- [ ] Everything runs without errors, or I explained what does not and why

---


## 2. Hackathon prototype -> [`hackathon/`](hackathon/)

> Your tool and your SDG for this hackathon are announced at the **start of Friday's class**.
> Write them down here once you know them.

**Project title:**
CVE Panic Meter

**My pair partner:**
Lucas, Iqbal
**Tool we had to use:**
A pre-trained sentiment model from Hugging Face, cardiffnlp/twitter-roberta-base-sentiment-latest. We fine-tuned it on our own posts and run it locally with the transformers library. We also compared it with cardiffnlp/twitter-xlm-roberta-base-sentiment and a simple word list with no machine learning. (If your assignment named the tool differently, change this line.)

**SDG we had to address:**
SDG 9, Industry, Innovation and Infrastructure, target 9.1 (resilient infrastructure with equal access for all)


**What problem does it solve, and for whom?**
The user: the information security officer (CISO) of a small or mid-sized Dutch municipality. The Netherlands has 342 municipalities. In a large city this is a whole department, but in a smaller one it is often a single person who also writes policy, answers audit questions and handles incidents. Our example user, “Ingrid”, is made up to make this concrete: 46, the only security specialist in a municipality of about 35,000 inhabitants.
Their decision: every week the officer goes through the new software vulnerabilities (CVEs) with the IT manager or the supplier. They decide which fixes go into the regular patch round and which are urgent enough for an emergency patch. That means downtime, overtime and explaining the choice to management.
The problem: the information they normally rely on arrives too late.
The official score is late or missing. Only 28% of the CVEs published in 2025 got a full analysis from the US National Vulnerability Database (NVD), and on our first day of collecting, 87 of the 89 CVEs named in our posts had no NVD score yet.
The “known exploited” list is a delayed signal. The US agency CISA only adds a flaw to its list after exploitation is confirmed, and it added only 245 in 2025.
Attackers are faster than defenders. In 2025, 28.96% of first-exploited vulnerabilities were already exploited on or before the day their CVE was published.
The early signal exists but nobody can read it. Security specialists often discuss a dangerous flaw online before the official lists catch up. In 2025 a Citrix flaw (CVE-2025-6543) was first described as one that could only crash the system, and it later turned out attackers could take it over. Several critical Dutch organisations were broken into, and the Public Prosecution Service was offline for weeks. Nobody at a small municipality was reading along.
Why it matters now: since 15 August 2026 the Dutch Cybersecurity Act is in force, and the mayor and aldermen are personally responsible for managing cyber risk. Large organisations can buy commercial threat intelligence, but a municipality of 30,000 inhabitants usually cannot.
Who it is for, and who is affected:
The officer gets a short list of what the security community is most alarmed about, with the official score and the “known exploited” status next to it. They also get the posts behind every peak, to show management why they acted, and an honest indication of how much each score is based on.
Residents and municipal staff are affected by the outcome, because the civil registry, benefits and permits depend on the patch decision. An unnecessary emergency patch has a cost too, so the tool should help avoid both mistakes.
Who it is not for: home users, large organisations with their own security operations centre, and anyone looking for a replacement for the NCSC, vendor advisories or a vulnerability scanner. It is one extra signal next to those.


**What did you build?**
We built a tool that keeps reading public posts about new vulnerabilities on Mastodon and Bluesky, and measures how alarmed they sound using a sentiment model we fine-tuned. A Streamlit dashboard shows the alarm per hour and per CVE for the last 24 hours, next to the official CVSS score and the CISA “known exploited” status, with the posts behind every peak. The officer uses it to decide which posts to read first, and it never says “patch now” or “can wait”. Over a collection run of 66.6 hours it stored 1,764 analysed posts and looked up all 848 CVEs.

**Link to the live thing (if any):**
[(https://youtu.be/q9XvFl7muOY)](https://youtu.be/q9XvFl7muOY)
The dashboard is not hosted publicly on purpose. Post texts can be searched online to find their authors, so it only runs on the local machine.

**How do I run it?**
You need Python 3.10 or newer and about 1 GB of free disk space. Run these from the hackathon/ folder.
'''
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt     # Windows
'''
# Linux: first .venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
1.Copy .env.example to .env and fill in CONTACT (an email address). An NVD API key is optional.
Start the collector with .venv\Scripts\python scripts/app/collector.py. The first start downloads the model.
2.In a second terminal, start the dashboard with .venv\Scripts\streamlit run scripts/app/dashboard.py, then open http://localhost:8501.
3.A fresh clone scores with the model as downloaded. To use our fine-tuned model, run the fine-tune command in docs/workflow.md first.


**Who did what?**
Lucas, Muhammad and I came up with the idea together. While brainstorming we talked about how many new vulnerabilities are published every day, and how a small organisation like a municipality cannot keep up with all of them. We all liked the idea of measuring how alarmed the security community sounds about a CVE, and we chose the CISO of a Dutch municipality as our user. We also set the bar for “good enough” together before seeing any results, and we labelled the 100 test posts by hand together.
Lucas ran the technical side. The collector had to run for days and the model was fine-tuned and run locally, so everything was set up on his laptop, and he managed the code, the dashboard and the fine-tuning. I gave ideas and feedback along the way, which Lucas worked into the tool.
Muhammad and I planned the presentation: we chose the structure to match the rubric, decided the order and who presents each part, and reviewed every slide. Lucas gave input on it.
We used AI tools throughout: to brainstorm and check the plan, to write the code under our direction, to label most of the training posts (which we checked and corrected), and to produce the slides from our README. We made the decisions, labelled the 100 test posts ourselves, and checked every number and source. No chat model scores a post: the Hugging Face model does.


**Ethical reflection - what are the risks of your tool? Who could it harm?**
Our tool can harm two groups. The first is the officer, and behind them the residents whose services depend on the patch decision. The second is the people whose posts we analyse, who never asked to be analysed. The most serious risk is that silence gets read as safety. The stream is English-speaking, Western and mostly automated (47 of 209 accounts look automated and wrote 75% of our 1,764 posts), and software used mainly by Dutch municipalities is hardly discussed in it. A dangerous flaw in exactly that software would not show up on the dashboard, and 800 of the 847 CVEs in our posts had too little data to score. So we show post and account counts next to every score, mark thin scores as “low data”, always show the CISA status, and keep a fixed warning: “No alarm does not mean no risk”. The tool may move a vulnerability up the list, never down. The model is a second risk. As downloaded it found only 7 of the 20 posts we labelled alarmed, and it still misreads some posts after fine-tuning, such as news headlines with the word “critical”. It also reads Japanese posts as alarmed (100 of 120) because it cannot read them. After fine-tuning it finds 18 of 20, but its lead over a simple word list is three posts on a small test, so it missed our own second bar (+0.15 F1; we got +0.03). It cannot decide what to patch, only what to read first. The model was also trained and tested on posts from one week, so its result is only true for October 2026. Finally, real people wrote these posts. We store no names or profiles, only a salted hash. We skip accounts that opted out, delete posts that Bluesky authors delete, and keep the dashboard on the local machine. Gaps remain: Mastodon deletions don’t reach us, and anyone could paste a post’s text into a search engine to find its author, so the post texts must never be published. We have also not shown the dashboard to a real security officer.

### Checklist
- [ ] Prototype code (or export / workflow file) is in `hackathon/`
- [ ] This week's slides are in `hackathon/`
- [ ] The prototype actually runs, and I wrote down how to run it
- [ ] Ethical reflection written above

---

## 3. Presentation -> [`presentation/`](presentation/)

*Only fill this in for the week your group was selected to present. You need at least **one** of these across the whole term.*

- [ ] My group presented in this week
- [ ] Slides are in `presentation/`
- [ ] Proof of the live demo is in `presentation/` (recording, screenshots, or link)

**How did it go? What would I do differently next time?**

---

## 4. Reflection

**What is the most important thing I learned this week?**
The most important thing I learned is that a pre-trained AI model is not automatically good at your problem, and you only find that out by testing it honestly. We chose a well-known sentiment model because it was trained on short social-media text and has a neutral label. On our own hand-labelled posts, though, it found only 35% of the posts we labelled as alarmed (F1 0.29), and a simple word list with no machine learning scored far higher (F1 0.83). The second model we tried, a multilingual one, did slightly better on recall (55%) but was still far behind. Without a baseline to compare against, we might have believed the model worked.
The second thing I learned is that fine-tuning on your own data changes the result a lot. After training on 900 posts from our own stream, the model found 18 of the 20 alarmed posts (recall 0.90, F1 0.86). That is just above the word list, but it met only one of the two conditions we set before seeing any results: recall of at least 0.60 was met, and an F1 at least 0.15 above the word list was not (the gap is +0.03).
The third thing is how much an evaluation can mislead if you are not careful. We changed the test after seeing the first results to get more training data. The second test is easier because the same accounts and automated feeds appear in both training and test. It has only 20 alarmed posts, so one post moves recall by 0.05, and the lead over the word list is three posts. Most training labels (783 of 900) came from an AI assistant, so we only trust the 100 posts we labelled ourselves. Reporting these limits openly mattered as much as the score itself.


**Where does this connect to "AI for Good"?**
The project connects to SDG 9 (Industry, Innovation and Infrastructure), target 9.1, which is about resilient infrastructure with equal access for all. A municipality’s IT is infrastructure: it runs the civil registry, benefits and permits, and in January 2020 about 150 to 200 Dutch municipalities had to switch off Citrix systems after a flaw was exploited. Large organisations can buy commercial threat intelligence, but a town of 30,000 usually cannot. Our tool turns public discussion into an early signal for the officers with the least capacity, at a time when the Cybersecurity Act (in force since 15 August 2026) makes the mayor and aldermen personally responsible.
The ethical side is where the project taught us the most:
A quiet line is not a safe line. 72% of our posts came from 26 accounts that look automated, 98 of our first 99 posts were in English, and software used mainly by Dutch municipalities is hardly discussed. So we show post and account counts next to every score, mark thin scores as “low data”, always show the CISA status, and keep a fixed warning on the dashboard. The tool can move a vulnerability up the list, never down.
The people behind the posts did not ask to be analysed. We store a salted hash instead of account names, keep no profiles, skip accounts that opted out, delete posts that Bluesky authors delete, and keep the dashboard on the local machine.
Honesty about the model. The model has not met our own bar, so it orders a reading list and the officer still makes the patch decision.

