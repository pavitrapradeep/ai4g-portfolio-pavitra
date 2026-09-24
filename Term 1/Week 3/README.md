# Term 1 - Week 3: Lists & Dictionaries

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
Dutch4You

**My pair partner:**
Evaldas

**Tool we had to use:**
Gemini API

**SDG we had to address:**
SDG 10, Reduced Inequalities, in particular target 10.2 on the social and economic inclusion of everyone. A person who can't read Dutch has a disadvantage when dealing with housing, banks, the municipality and the university. Those are the places where rules and deadlines are written only in Dutch. Dutch4You reduces that gap by giving newcomers the same understanding a Dutch speaker gets immediately.


**What problem does it solve, and for whom?**

Dutch4You addresses the language barrier faced by international students, newcomers, and other non-Dutch speakers in the Netherlands when dealing with important Dutch-language communication.
International students in the Netherlands may receive administrative communication from universities, housing providers, municipalities, banks, and other services in Dutch.i
These messages can contain important information such as:
-deadlines
-payments
-required documents
-appointments
-instructions
-actions the recipient needs to take

For someone who is still learning Dutch, the difficulty is not necessarily translating every individual word. The more important challenge can be identifying what the message means, what information matters, and what action is required.
This creates a language-based information-access barrier.
Dutch4You helps reduce this information gap by converting Dutch communication into clear English explanations, while highlighting important actions, deadlines, and relevant information.


Why This User Group Matters

International students are a significant part of Dutch higher education.
According to Nuffic, there were 131,004 international degree students in Dutch higher education in 2024/25, representing 16.6% of the total student population.
This statistic demonstrates the scale of the population our project is designed for. It does not mean that all international students have difficulty understanding Dutch.
Source: Nuffic — Facts and figures: International students in Dutch higher education 2025


🧑‍🎓 Target Users

-Primary users:
International and exchange students in the Netherlands who:
communicate comfortably in English
are still learning Dutch
receive Dutch administrative or official communication
need help understanding practical information in those messages

Typical situation
A student may receive a Dutch message from their:
university,housing provider,municipality,bank,other administrative service
The message may contain a deadline, payment, required document, or specific action.
The student can paste the text into Dutch4You to get a clearer explanation and identify the practical information they need.


Not intended for:

Dutch4You is not intended to replace:
certified or legally valid translations,professional interpreters,legal advice,professional immigration advice,high-stakes decisions based solely on AI output
The current prototype also accepts pasted text only and does not process images, scans, audio, or handwriting.

**What did you build?**

We built Dutch4You, an AI-powered web application designed to help non-Dutch speakers understand Dutch messages and official communication.
The user can provide Dutch text to the application. Dutch4You then uses the Gemini API to analyse the text and generate an English explanation that is easier for the user to understand.
The purpose is not simply to perform a word-for-word translation. We wanted the application to focus on the information that is useful to someone who needs to understand and act on the message.

⚙️ How It Works

Dutch text
↓
Streamlit
↓
Gemini API
↓
Translate + Explain + Extract
↓
Structured JSON
↓
Clear actionable output


**Link to the live thing (if any):**

 https://dutch4you.streamlit.app/

 
 video demo: https://drive.google.com/file/d/1pLlWkTioQ8HxIcsKJxh2-nPfwO6xOIsT/view?usp=sharing

The live prototype demonstrates the complete process from providing Dutch text to receiving the AI-generated English explanation.

**How do I run it?**

To run Dutch4You locally:
Clone or download the project repository.
Make sure Python is installed.
Install the required dependencies from the project's requirements file.
Configure the Gemini API key in the required environment/configuration.
Start the Streamlit application.
Open the local URL provided by Streamlit.
Enter or paste Dutch text into the application.
Submit the text and review the generated English explanation.
The Streamlit application can be started using:
streamlit run app.py

The filename should be replaced with the actual entry-point file if the project uses a different filename.
A user does not need to interact directly with the Gemini API. The application handles the communication with the AI model in the background.

**Who did what?**

The work was divided between the both of us, with some parts completed individually and other parts done collaboratively.
Evaldas worked primarily on the Streamlit application and its functionality, including the implementation of the application flow.
I focused primarily on the interface and UI design, including how the application and its results are presented to the user.
Both of us worked together on the Gemini API setup and API key configuration, as well as testing the AI functionality.
The documentation, project description, ethical reflection, and overall project development were completed collaboratively.

**Ethical reflection - what are the risks of your tool? Who could it harm?**

The main ethical risk of Dutch4You is that users may rely on an incorrect AI-generated explanation when they cannot independently understand the original Dutch text. This could be particularly harmful if the message contains a deadline, payment, healthcare information, or another important requirement. To reduce this risk, the application provides a confidence level and warning when the AI is uncertain, and users are advised to verify important information with an official source or Dutch speaker. The system is also instructed not to guess when the input is unclear or does not appear to be Dutch, and invalid AI responses are handled instead of being shown as reliable information. Privacy is another concern because users may paste personal information from official letters, so the tool advises users to avoid submitting highly sensitive information unnecessarily. These safeguards are important because a tool designed to reduce information inequality should not create a new risk by making users overly dependent on potentially incorrect AI output.

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

The most important thing I learned was that building an AI solution is not only about making the technology work. We first need to understand the actual problem and the people affected by it.
For Dutch4You, we realised that the problem is not simply that newcomers cannot translate Dutch. They need to understand what important communication means and what action they are expected to take.
I also learned that AI outputs need to be handled carefully. A system can produce a convincing answer that is still incorrect, so testing, error handling, confidence indicators, and clear limitations are important parts of building an AI application.

**Where does this connect to "AI for Good"?**
Dutch4You directly connects to SDG 10 – Reduced Inequalities, particularly Target 10.2, which focuses on promoting the social and economic inclusion of everyone. Our project focuses on one specific barrier to inclusion: language and access to information.
For international students, newcomers, migrants, and other people who are still learning Dutch, language can make it harder to access and act on information that Dutch-speaking residents may understand immediately. This is especially important when dealing with universities, housing organisations, banks, municipalities, healthcare services, and other public services. A person may receive the same information as everyone else, but if they cannot understand the language, they may not have the same ability to respond to it or benefit from the service.
Dutch4You aims to reduce this gap by providing an additional layer of understanding. Instead of only translating Dutch into English, it explains the message in simpler language and identifies practical information such as deadlines, required actions, and amounts. This can help users understand not only what the message says, but also what they are expected to do.
The project therefore supports the idea behind Target 10.2 by making important information more accessible to people who may otherwise face a language barrier. The goal is not to give newcomers an advantage over Dutch speakers, but to help reduce an existing accessibility gap so that language is less of a barrier when accessing everyday services and information.
The project also demonstrates an important aspect of AI for Good: responsible use of technology. While AI can help reduce an information-access inequality, it can also create new risks if its output is inaccurate. Someone who cannot read the original Dutch text may be more likely to rely on the AI's explanation. Therefore, Dutch4You includes confidence information and warnings and encourages users to verify uncertain or important information with an official source or Dutch speaker.
In this way, the project connects to AI for Good on two levels: using AI to improve accessibility and inclusion, while also considering the ethical risks of using AI for people who may depend on its output.
