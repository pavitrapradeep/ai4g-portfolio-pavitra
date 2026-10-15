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

**SDG we had to address:**
SDG 9

Readme in hackathon file

**What problem does it solve, and for whom?**
_Name a real, specific user. "Everyone" is not a user._

**What did you build?**
_Two or three sentences. What can a user actually do with it?_

**Link to the live thing (if any):**
[(https://youtu.be/q9XvFl7muOY)](https://youtu.be/q9XvFl7muOY)

**How do I run it?**
_Short instructions so someone else can start it._

**Who did what?**
_Be honest about the split of work between you and your partner._

**Ethical reflection - what are the risks of your tool? Who could it harm?**
_Every hackathon requires this. One honest paragraph beats three vague ones._

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

