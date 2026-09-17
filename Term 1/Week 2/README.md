# Term 1 - Week 2: Loops & Functions

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
Daily Wellbeing journal

**My pair partner:**
Murat

**Tool we had to use:**
n8n

**SDG we had to address:**

SDG 3 — Good Health and Well-Being: Our project addresses SDG 3 by using AI to support mental and emotional wellbeing. Daily Wellbeing Journal encourages users to regularly check in with their mood, stress, sleep, and thoughts, while analyzing previous entries to help them recognize patterns. By providing personalized reflections, the project promotes self-awareness and encourages users to pay more attention to their overall wellbeing.


**What problem does it solve, and for whom?**

Daily Wellbeing Journal is designed for young adults in specific who wants to journal, monitor their stress, and better understand their experiences over time. Stress can change from day to day, and it is not always easy to recognise what is affecting it or how it has changed. The journal provides a private space to record stress levels and express thoughts without always needing to talk to another person. By keeping a history of entries, it helps the user identify patterns, reflect on their experiences, and receive simple stress-relief tips, supportive affirmations, or suggestions based on what they have shared.

**What did you build?**

We built Daily Wellbeing Journal, an automated stress journaling tool that gives users a private space to track and reflect on their wellbeing. Through a form, users record how stressed they feel, how calm they feel, and a journal entry about their thoughts, feelings, or daily experiences. The responses are stored in Google Sheets, and OpenAI analyses the current entry along with previous entries to identify patterns over time. It then generates a personalised reflection, supportive affirmation, or simple stress-relief tips based on what the user has shared, which is sent to their Gmail.

**Link to the live thing (i[f any):**
https://drive.google.com/file/d/1PTzte61DTfMhqIoOEr56FRyUXYxQiXVo/view?usp=sharing
https://drive.google.com/file/d/1S6EJy-ixSzoYPQltjYdkJYZBxj7vz7rF/view?usp=sharing

hack.png
hackathon.png

**How do I run it?**

1.Download the Daily Wellbeing Journal .json workflow.
2.Open n8n and import the JSON file.
3.Connect the required Google Sheets and OpenAI credentials.
4.Open the Form Trigger link and fill in the journal form.
5.Submit the form to trigger the workflow.
6.The response is stored in Google Sheets, together with the user's previous entries.
7.OpenAI analyses the current stress level and journal entry, while also looking at previous entries to identify patterns in the user's wellbeing over time.
8.Based on this analysis, it generates a personalised reflection and supportive message.
9.The response is automatically sent to the connected Gmail account.

**Who did what?**

We equally contributed to the project. We worked together on designing and building the workflow, setting up the n8n nodes, integrating Google Sheets and AI, testing and troubleshooting the automation, making improvements and preparing the presentation, Both of us were involved in all major parts of the project.

**Ethical reflection - what are the risks of your tool? Who could it harm?**

Daily Wellbeing Journal deals with personal information like mood, stress, sleep, and journal entries, so privacy is an important concern. There is also a chance that the AI could misunderstand what a user is feeling, identify a pattern incorrectly, or give an unsuitable response. Another risk is that someone might rely too much on the tool instead of seeking professional help when needed. The system could also fail because of technical issues, such as the workflow being down, an email not being delivered, or the AI not generating a response correctly. To reduce these risks, we should keep user data secure, only collect the information we need, avoid giving medical diagnoses, and clearly explain that the tool is for self-reflection and not a replacement for professional support. The AI should also be conservative when identifying serious distress and provide appropriate support information rather than trying to handle a crisis itself. Ultimately, automation should support the user’s wellbeing and reflection, while important health or safety decisions should remain with the user and qualified human professionals.

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

The most important thing I learned this week is how different technologies can be connected to create a complete working project. I learned how n8n can connect forms, Google Sheets, AI, and Gmail to automate a process. I also learned that building an AI project is not just about making it work, but also thinking about privacy, ethics, and how it could affect users.

**Where does this connect to "AI for Good"?**

Our project connects to AI for Good by using AI to support people's wellbeing. Instead of using AI only for entertainment or productivity, we use it to help users understand their emotions, notice wellbeing patterns, and encourage regular self-reflection. We also consider privacy and responsible use of AI, making sure it supports users without replacing professional help.
