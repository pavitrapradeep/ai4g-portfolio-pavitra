# Scrolly

> Turn dense English-language study material into short, interactive learning cards that students can scroll through, translate into a supported language, and use to check their understanding.

**Live app:** https://studyscrolly.lovable.app  
**Team:** Pavitra and Minhyeok Sung  
**Required tool:** Lovable AI  
**SDG:** SDG 4 – Quality Education  
**Demo:** A demonstration video accompanies this submission.

---

## 1. The problem

### The learning challenge

Scrolly focuses on a specific challenge: students who study in English as an additional language can need more time and effort to understand dense academic reading, particularly when the material contains unfamiliar specialist vocabulary, long sentences, or complex concepts.

A relevant example from our project context is a student in an English-taught programme at The Hague University of Applied Sciences (THUAS) who has to study a chapter from a subject-specific textbook such as *A Basic Guide to International Business Law*. The student may need to pause frequently to understand terminology, translate unfamiliar expressions, reread sentences, and work out how a concept applies. This is an illustrative use case, not a claim that every student or every course experiences the same difficulty.

Research supports the underlying language-processing challenge. In an eye-tracking study, Dirix et al. found that participants needed approximately 20% more time to study texts in their second language than in their first language. The study also found that the additional time compensated for less efficient processing, with similar recognition-test scores across the two language conditions (Dirix et al., 2020). This result comes from a specific experimental study; it should not be interpreted as a universal estimate for every student, language pair, or course.

The challenge is not simply that students have a lot to read. It is that dense material can be difficult to break down, and reading alone does not always help a student identify which concepts they have understood and which they need to revisit. Without a quick way to check understanding, students may only discover gaps when preparing for an assessment or receiving feedback later.

### Why this is relevant in the THUAS context

THUAS's 2023 Annual Report records 3,253 students from abroad, representing 12.8% of its total student population based on non-Dutch prior education. The report also states that THUAS offered eleven bachelor's programmes taught in English at that time (The Hague University of Applied Sciences, 2024). These figures show that international students and English-taught programmes are part of the institution's educational context. They do not tell us how many students are non-native English speakers or how many experience the specific reading difficulty described above.

At national level, Nuffic reported 129,764 international degree students in publicly funded Dutch higher education in the 2025–26 academic year. International students represented 9% of the student population at universities of applied sciences (Nuffic, 2026). This provides broader context for international participation in Dutch higher education, but it is not a direct measure of the number of students who need language support.

**Problem statement:** Students in English-taught higher-education programmes who are less comfortable with academic English may find it difficult and time-consuming to process dense study material, identify its key ideas, and check their understanding while studying independently.

We have used this problem to guide the prototype. We have not yet conducted formal interviews or a controlled study with target users, so we do not claim that Scrolly has already been proven to improve grades, reading speed, or learning outcomes. User interviews and usability testing are important next steps.

---

## 2. Who Scrolly is for — and who it is not for

### Primary target users

Scrolly is designed primarily for students in English-taught university or university-of-applied-sciences programmes who use English as an additional language and find dense academic reading difficult to process.

A representative user is a first-year or early-stage student who:

- studies from digital textbooks, lecture notes, or academic articles;
- encounters unfamiliar academic, technical, or subject-specific vocabulary;
- needs to understand material independently between classes;
- benefits from shorter explanations, examples, and opportunities to check understanding; and
- may prefer to review explanations in one of the languages supported by the prototype.

The need may be particularly noticeable when students begin a new programme or subject and encounter unfamiliar terminology. This is a design assumption and use case, not a finding from formal user research.

### Who is not the primary target user?

Scrolly is not designed as:

- a replacement for teachers, lecturers, textbooks, or official course materials;
- an authoritative source for legal, medical, or other high-stakes advice;
- a specialist assistive-technology product for learners who require individually tailored support;
- an offline learning platform for users without internet access; or
- a tool that currently supports every language or every accessibility need.

Native English speakers may also use Scrolly, but reducing the additional effort of studying in English is not the central problem the prototype was designed around. The app has not been specifically designed or evaluated for primary- or secondary-school pupils.

---

## 3. What we built and how it works

Scrolly is an AI-powered learning application that transforms user-provided study material into a sequence of interactive cards. The aim is to make a long piece of text easier to navigate and to give students opportunities to check what they have understood.

### User journey

1. **Provide study material.** The student pastes text into the input area or uploads a document, such as a textbook PDF.
2. **Choose a language.** The student selects one of the five languages supported by the prototype.
3. **Choose a learning focus.** The student can select a balanced mix or focus on particular card types: concepts, definitions, examples, “Why it matters” explanations, or quick-check questions.
4. **Generate the deck.** The student selects **Create Deck**. The application's AI functionality processes the submitted material and the selected options to generate structured learning content.
5. **Study the cards.** The material is presented as scrollable cards, with one main idea at a time.
6. **Check understanding.** Quick-check questions let the student test their understanding and receive immediate feedback. The student's score builds as they progress through the deck.
7. **Review the summary.** The deck ends with a summary of the material.

### What the AI contributes

AI is used for the central transformation in Scrolly: turning user-provided study material into structured learning content on demand. This includes selecting and explaining key concepts, generating definitions and examples, producing “Why it matters” explanations, creating quick-check questions, and presenting the content in the selected supported language.

This is different from simply displaying a static set of pre-written flashcards. Students can provide different source material and generate a deck for that material. Without the AI-generation step, the application would not be able to create a tailored set of cards and questions for each new input automatically.

**Tool clarification:** We used Lovable to build the application. Lovable's documentation distinguishes the Lovable agent, which helps build and edit a project, from the built-in AI connector, which can add AI features that run inside the published app (Lovable, n.d.). The project documentation explains this distinction, but it does not establish which exact model or provider is configured in this particular Scrolly project. We therefore do not claim a specific underlying model. The demo video should be used to demonstrate the runtime generation flow.

### How to try the prototype

Open https://studyscrolly.lovable.app in a browser. Provide study material, select a supported language and the card types you want, and choose **Create Deck**. Then scroll through the generated cards, answer the quick checks, review the feedback and finish with the summary.

A demonstration video accompanies this submission and shows the prototype's intended end-to-end user journey.

---

## 4. Why this solution fits the problem

The problem is that some students studying in English as an additional language find dense academic material difficult to process and may not have an immediate way to check their understanding. Scrolly responds to these needs through several connected features:

- **Short, structured cards** divide a long text into smaller sections, making it easier to navigate and review.
- **Definitions and examples** help explain unfamiliar terminology and concepts.
- **Language selection** lets users access generated learning content in one of the supported languages.
- **Quick-check questions and immediate feedback** give students an opportunity to retrieve information and notice possible gaps in their understanding.
- **A final summary** gives students a concise recap of the material covered.

A translation tool alone could translate a passage but would not necessarily reorganise it into learning steps or test understanding. A plain summary could shorten the material but would not provide the same sequence of concepts, examples, questions, and feedback. A fixed set of pre-written flashcards would not automatically adapt to each student's own study material. Scrolly combines these functions in one workflow.

The card format is intended to make the learning process feel approachable and easy to navigate, especially during short independent study sessions. However, the effectiveness of this approach for the target group still needs to be tested with students. We therefore describe Scrolly as a learning aid with a plausible problem–solution fit, not as a proven intervention.

---

## 5. Working prototype and demonstration

The prototype is available at:

**https://studyscrolly.lovable.app**

The accompanying demonstration video shows the intended flow from study-material input to generated cards, quick-check questions, feedback, and the final summary.

The prototype's main functionality is intended to be demonstrated end to end:

1. enter or upload study material;
2. select a language and card focus;
3. generate a deck;
4. navigate the learning cards;
5. answer quick-check questions and receive feedback; and
6. review the final summary.

demo video: https://drive.google.com/file/d/1gqMAYWy688loSSLkNhxw-ti5T69StVhp/view

The demonstration video is included as evidence of the working prototype. It shows the product flow; it does not by itself establish that Scrolly improves learning outcomes. That would require testing with representative students and an appropriate evaluation method.

---

## 6. Ethical reflection

Scrolly is designed to support students who may already find academic reading challenging. This creates a responsibility to ensure that the tool does not introduce new barriers or give students misleading confidence. The ethical question is not only whether the application works, but whether students can use it safely, understand its limitations, and remain in control of their learning.

### People affected and ethical values

The primary stakeholders are students using Scrolly to study, particularly students working in an additional language. Lecturers and educational institutions are also affected because generated explanations may influence what students learn and how they prepare for assessments. The team developing the application has a responsibility to communicate limitations honestly and avoid presenting generated content as verified educational material.

The main values at stake are:

- **Accuracy and academic integrity:** explanations, translations, and questions should not distort the source material or encourage students to submit AI-generated work as their own.
- **Autonomy and informed use:** students should know when content is AI-generated and should be able to compare it with the original material and make their own judgements.
- **Fairness and inclusion:** language support should reduce barriers without excluding students whose languages, devices, or accessibility needs are not supported.
- **Privacy and respect for intellectual property:** students should understand how submitted material is processed and should not be encouraged to upload confidential or unauthorised content.
- **Transparency and accountability:** the team should be clear about what the prototype can demonstrate, what has not been tested, and what still needs improvement.

The risks below consider both the potential harm and the limits of the current prototype. Proposed safeguards are future improvements unless explicitly identified as current functionality.

### 6.1 Incorrect or incomplete AI-generated content

The AI may omit an important point, misunderstand a sentence, or simplify a concept so much that the meaning changes. A student who relies only on the generated cards could miss an exception or qualification in the original material. This is especially concerning in subjects such as law, where a small detail can change the meaning of a rule.

**Current limitation and response:** Scrolly is intended as a supplementary study aid, not a replacement for the original source. Students should compare generated content with their course material.

**Further improvement:** Show the source passage used for each card, make it easy to return to the original text, and display a clear notice that AI-generated explanations may contain errors.

### 6.2 Incorrect quiz questions or feedback

The AI may generate a poorly worded question, an ambiguous answer, or incorrect feedback. Because the feedback appears immediately, students may trust it even when it is wrong. A student who is less confident in the subject or language may find it particularly difficult to challenge the answer.

**Current response:** The prototype provides immediate feedback as part of the learning interaction, but feedback alone does not guarantee that the answer is correct.

**Further improvement:** Link each question to the relevant source passage, review generated questions for accuracy, and allow students to flag questions or answers that appear incorrect.

### 6.3 Translation errors and loss of subject-specific meaning

A word may have different meanings in everyday language and in a specialist subject. AI translation may choose an inaccurate equivalent, particularly for legal, technical, or academic terminology. A student could then learn a misleading explanation or fail to recognise the English term used in class or in an examination.

**Current response:** The prototype offers five language options, but multilingual output should not be assumed to be equally accurate in every language or subject.

**Further improvement:** Display important subject-specific terms in English alongside the translated explanation, test translations with proficient speakers, and make the original wording easy to access.

### 6.4 Passive use and false confidence

Students may scroll through cards quickly, guess quiz answers, or focus on their score rather than understanding the material. This could make them feel prepared without being able to explain or apply the concepts independently.

**Current response:** Quick-check questions and immediate feedback are included to encourage active engagement rather than reading alone. However, a quiz score is not proof of deep understanding.

**Further improvement:** Ask students to commit to an answer before revealing feedback, include application-based questions, and encourage students to explain concepts in their own words.

### 6.5 Over-reliance on summaries instead of the original material

Because the target users may find academic English demanding, they may be tempted to use only the generated cards and skip the original textbook. This could reduce their exposure to the full argument, detailed examples, and specialist language they need for their course.

**Current response:** Scrolly is positioned as a supplementary learning aid.

**Further improvement:** Link cards to their source sections and encourage students to use the cards before or after reading the original material, rather than as a substitute for it.

### 6.6 Privacy and copyright

Students may paste personal information, unpublished work, or copyrighted textbook extracts into the application. Submitted material may be processed by the AI service configured for the app. Users should understand what happens to their content and should not upload material they do not have permission to use.

**Current limitation and response:** The README cannot establish the app's exact data-retention or provider terms. Students should avoid submitting personal or confidential information and should only use material they are permitted to process.

**Further improvement:** Provide a clear privacy notice before submission, explain which AI service processes the content, minimise retention of user-provided material, and review copyright and data-protection requirements.

### 6.7 Unequal access and accessibility

Scrolly requires a suitable device and internet connection and currently supports five languages. Students who lack reliable connectivity, use older devices, or speak an unsupported language may not benefit. Students who rely on assistive technologies may also encounter barriers if the interface is not fully accessible.

**Current limitation:** The prototype does not claim to meet every accessibility need or to be available offline.

**Further improvement:** Test the application with screen readers, keyboard-only navigation, different screen sizes, low-end devices, and slower internet connections. Prioritise additional languages based on feedback from intended users.

### Ethical priorities and trade-offs

There is a trade-off between making study material simpler and preserving the depth and precision of the original. If Scrolly simplifies too aggressively, it may make a topic feel easier while removing nuance that matters. If it translates everything, it may help immediate comprehension but leave students less familiar with the English terminology used in lectures and assessments. The design should therefore support understanding without hiding the original wording or encouraging students to abandon the source material.

The most serious residual risk is that an incorrect explanation or answer may look convincing and be trusted by a student who is using the tool precisely because the original text is difficult. A disclaimer alone is not enough to remove this risk. Source links, clear AI labelling, review mechanisms, and testing with the intended users are needed. Likewise, privacy cannot be guaranteed simply by advising users to be careful: the team must verify the actual AI provider, data handling, and retention settings and explain them clearly before making privacy claims.

Our priorities for responsible development are therefore:

1. **Make outputs verifiable:** connect cards and quiz feedback to the relevant source text so students can check them.
2. **Keep students in control:** label generated content, preserve access to the original, and explain that scores are practice feedback rather than proof of mastery.
3. **Test with the intended users:** conduct usability sessions with students who study in an additional language, including feedback on translation quality and whether the cards preserve meaning.
4. **Verify data handling:** identify the runtime AI provider, review its privacy and retention terms, minimise submitted data, and provide a clear notice before users upload material.
5. **Improve inclusive access:** test keyboard navigation, screen-reader compatibility, mobile layouts, and the needs of students whose languages are not currently supported.

At this stage, Scrolly is a prototype, not a validated educational intervention. We have identified these risks and possible safeguards, but we have not yet demonstrated that all safeguards are implemented or that the application improves learning outcomes. We would need user testing, technical checks, and feedback from educators before making those claims.

---

## 7. Who did what?

**Pavitra:** Developed the main idea of making long and difficult study materials easier and more engaging to learn. Contributed to the overall concept, design and learning features of Scrolly, and participated in building, testing and improving the prototype. Also contributed to the README, ethical reflection and presentation.

**Minhyeok Sung:** Contributed the idea of transforming study material into scrollable, flashcard-style content, which shaped the main interaction and user experience. Participated in developing and designing the prototype, testing and improving its features, and preparing the README, ethical reflection and presentation.

We collaborated throughout the project to develop the concept and turn it into a working prototype.

---

## 8. Conclusion

Scrolly explores how AI can make dense educational material easier to navigate and study. It transforms user-provided text into structured cards, explanations, examples, quick-check questions, feedback, and a final summary. Its multilingual functionality is intended to make the generated learning content more approachable for students who study in English as an additional language.

The project contributes to the broader aim of SDG 4 by exploring a more inclusive and engaging learning support tool. The closest SDG targets for our higher-education user group are Target 4.3, concerning access to technical, vocational and tertiary education, and Target 4.5, concerning equal access and educational inequalities. Target 4.1 concerns primary and secondary education, so we do not claim that a prototype designed for higher-education students directly fulfils that target.

The prototype demonstrates the concept and its intended workflow. Further user research, accessibility testing, source-linked verification, and evaluation of learning outcomes are needed to understand how effective and reliable Scrolly is in real study situations.

---

## 9. References

The following sources support the factual context and SDG descriptions used in this README. The project-specific statements about Scrolly's design, features, team contributions, and demonstration are based on the team's project information and prototype.

1. **Dirix, N., Vander Beken, H., De Bruyne, E., Brysbaert, M., & Duyck, W. (2020).** Reading text when studying in a second language: An eye-tracking study. *Reading Research Quarterly, 55*(3), 371–397. https://doi.org/10.1002/rrq.277  
   Supports the carefully qualified statement that participants in this particular study needed approximately 20% more time to study texts in their second language. The article was first published online on 25 October 2019; the journal issue is dated 2020.

2. **Nuffic. (2026, September 4).** *International students in the Netherlands 2026: Facts, figures, challenges and benefits.* https://www.nuffic.nl/en/onderzoek-en-cijfers/onderzoeken/international-students-in-the-netherlands-2026  
   Supports the national context figures for 2025–26: 129,764 international degree students in publicly funded Dutch higher education and 9% of the student population at universities of applied sciences. Nuffic defines international students using nationality and prior-education criteria; these figures do not measure English-language proficiency or identify all students who may experience academic-language difficulties.

3. **The Hague University of Applied Sciences. (2024).** *Annual report, board report and financial statements 2023.* https://www.thuas.com/media/annual-report-board-report-and-financial-statements-2023  
   Supports the THUAS figures reported for 2023: 3,253 students from abroad (12.8%, based on non-Dutch prior education) and eleven bachelor's degree programmes taught in English. These figures provide institutional context; they do not establish how many students experience the specific problem Scrolly addresses.

4. **United Nations Department of Economic and Social Affairs. (n.d.).** *Goal 4: Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all.* https://sdgs.un.org/goals/goal4  
   Official wording and scope for SDG 4 targets 4.1 (primary and secondary education), 4.3 (technical, vocational and tertiary education, including university), and 4.5 (eliminating disparities and ensuring equal access to education and training).


---

### Evidence and limitations

- The research and institutional statistics above provide context for the problem; they do not prove that Scrolly improves reading speed, comprehension, grades, or learning outcomes.
- The 20% second-language study-time difference is a result from one experimental study, not a universal rate for all second-language learners.
- The national and THUAS international-student figures are not counts of non-native English speakers and should not be presented as such.
- The demo video documents the prototype's demonstrated workflow. Claims about features should match what is visible and working in the submitted version.
- The exact runtime AI model/provider and the app's data-retention configuration should only be named after checking the Scrolly project's own settings and privacy documentation.
