# Term 1 - Week 4: Strings, Text & Files

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
Below the Waterline:climate adaptation in The Netherlands

**My pair partner:**
Muhammad Iqbal

**Tool we had to use:**
ComfyUI — LTX-2.3 Text-to-Video

**SDG we had to address:**

SDG 13 — Climate Action

Our project addresses SDG 13: Climate Action by focusing specifically on climate adaptation in low-lying areas of the Netherlands. The film explores how extreme rainfall, coastal water pressure and land subsidence create ongoing challenges for Dutch communities and infrastructure. Instead of presenting climate change as a broad global issue, we show a specific Dutch context and then move from environmental risks to adaptation through water-resilient neighborhoods, floating housing and climate-resilient urban design. Our aim is to show young adults that the Netherlands’ relationship with water is not a problem that has already been solved, but an ongoing adaptation challenge.


**What problem does it solve, and for whom?**

Our film addresses a specific climate-adaptation challenge in the Netherlands: how low-lying areas are affected by water-related climate risks and land subsidence, and why continued adaptation is necessary. The film focuses on extreme rainfall, coastal water pressure, low-lying land and land subsidence, before showing possible adaptation approaches such as water-resilient neighborhoods, floating housing and climate-resilient urban design.

The film is designed for young adults aged 18–30 living in urban areas of the Netherlands who have general awareness of climate change and know that the Netherlands has extensive water-management infrastructure, but may not be familiar with the continuing challenges associated with low-lying land, changing water-related risks and land subsidence.
Within 30 seconds, the film moves from a familiar Dutch landscape to environmental pressures and then to adaptation. Its purpose is to make a technically complex issue accessible and communicate that water management is an ongoing adaptation challenge rather than a problem that has already been completely solved.

Problem:
Our film addresses a specific climate-adaptation challenge in the Netherlands: how low-lying areas face increasing water-related risks and how land subsidence adds further challenges.

- 10.7 million people in the Netherlands are at risk of possible flooding if primary flood defences fail. [H2O Waternetwerk, 2026]
- Extreme rainfall and waterlogging can damage homes, infrastructure and vital services. [PBL, 2024/2026]
- Land subsidence, particularly in peatland areas, creates additional challenges for infrastructure, housing and water management. [PBL, 2016]
- PBL states that climate adaptation requires structural choices in areas such as spatial planning, housing and infrastructure. [PBL, 2024]
- Our film therefore moves from climate risks → adaptation, showing water-resilient neighborhoods, floating housing and climate-resilient urban design.

Sources
- H2O Waternetwerk — 10.7 million people at possible flood risk
- PBL — Climate Risks in the Netherlands (2024)
- PBL — Subsiding Soils, Rising Costs (2016)
- PBL — Climate-resilient living environment (2026)
- 
Who is the audience?

Primary audience:
Our primary audience is young adults aged 18–30 living in urban areas of the Netherlands.

They are people who:

- have a general awareness of climate change;
  
- are familiar with the Netherlands' reputation for water management;
  
- may not understand why climate adaptation remains necessary despite existing water-management infrastructure;
  
- may have limited knowledge of land subsidence and its relevance to low-lying areas;
  
- can understand a short visual message but are not expected to have specialist climate or water-management knowledge.
  
Who is it NOT for?

The film is not primarily aimed at specialist audiences, such as:

- climate scientists;
- water-management professionals;
- civil or environmental engineers;
- policymakers;
- researchers specializing in Dutch climate adaptation.
  
These groups may find the film useful as a communication piece, but they are not the intended primary audience. The film is designed as a short, accessible climate-awareness piece rather than a technical or scientific presentation.

**What did you build?**

We built Below the Waterline, a 30-second AI-generated climate-awareness short film created in ComfyUI for young adults aged 18–30 living in urban areas of the Netherlands. The film helps this audience understand how extreme rainfall, coastal water pressure, low-lying land and land subsidence create ongoing climate-adaptation challenges in the Netherlands. It presents practical adaptation approaches, including water-resilient neighborhoods, floating housing and climate-resilient urban design, showing how communities can respond to these changing water-related risks. Through a short visual narrative, the film makes a complex climate issue accessible without requiring specialist knowledge and highlights why continued climate adaptation is necessary. The film ends with the message: “WE CAN’T STOP THE WATER. WE CAN ADAPT.”

**Link to the live thing (if any):**
https://www.youtube.com/watch?v=EHNvl7A7yRA

**How do I run it?**


1. Open ComfyUI and load the provided workflow JSON.
2. Ensure the required LTX-2.3 models and supporting files are installed.
3. Run the workflow with the provided prompts and seeds to generate the 9 video shots.
4. Generate the voiceover directly in ComfyUI using FL Chatterbox Multilingual TTS.
5. Export the generated video and audio.
6. Assemble the final 30-second film in DaVinci Resolve. 
All AI-generated video and voiceover content was created within ComfyUI.

**Who did what?**
The work was split equally between both of us, with responsibilities shared across the different stages of the project. We both contributed to the concept development, creative direction, ComfyUI workflow, video generation, shot refinement, and final editing. We also shared the work involved in preparing the storyboard, README, ethical reflection, presentation, and other project documentation. Throughout the process, we reviewed the generated visuals together, discussed improvements, refined the film, and worked collaboratively to prepare the final submission.

**Ethical reflection - what are the risks of your tool? Who could it harm?**

Our film uses photorealistic AI-generated video created in ComfyUI to visualize climate-adaptation challenges in the Netherlands, including low-lying land, extreme rainfall, coastal water pressure, land subsidence, and climate-resilient infrastructure. The main risk is that realistic AI imagery could make fictional situations appear to be real events or predictions. To reduce this risk, we replaced two original catastrophic shots with more realistic visualizations of land subsidence and climate adaptation, rather than showing a destroyed or completely submerged Netherlands. Although some scenes are inspired by real Dutch landscapes and infrastructure, none of the footage represents an actual recorded event, and we do not claim that the depicted events happened at those locations. No identifiable people or individual likenesses were intentionally included, so no person’s likeness was used without consent. We make the use of AI transparent by identifying the visuals as AI-generated using ComfyUI in our project documentation, README, and YouTube description. We made 11 video generations in total to produce the final 9-shot film, including the two replacement shots.

We recognize that each generation uses computational resources and therefore has an environmental cost. We limited unnecessary generations and used the outputs for an educational climate-awareness project. This creates a clear tension between using computationally intensive AI to communicate a climate-action message and the environmental impact of AI generation, which we considered when deciding how many generations were necessary.

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


The most important thing I learned this week is that AI for Good requires both technical skills and responsible decision-making. While working on our climate film, I learned how AI-generated visuals can be used to communicate a complex issue in a short and engaging way, but also how easily realistic AI content can become misleading. We had to think carefully about whether a dramatic scene communicated the problem accurately or exaggerated it. This led us to replace two of our original disaster-focused shots with more realistic scenes showing land subsidence and climate adaptation.
Alongside the AI work, I also strengthened my programming fundamentals by learning about strings and lists. I learned how strings are used to store and manipulate text, including accessing characters and working with text values, while lists allow multiple values to be stored and organized together. Understanding these basic data structures helped me see how programming concepts can support larger AI and data-related workflows.

**Where does this connect to "AI for Good"?**

This connects to AI for Good through responsible technology, sustainability and social impact. Our project uses AI to make the specific issue of climate adaptation in the Netherlands easier for a general audience to understand. However, we also had to consider the risks of using photorealistic AI: viewers could mistake generated scenes for real events, and generating AI video also requires computational resources and energy.
We addressed these risks by avoiding exaggerated disaster imagery, clearly treating the scenes as AI-generated visualizations, and disclosing our use of ComfyUI. We also considered the number of generations we made and the environmental cost of using AI. This taught me that AI for Good is not simply about using AI for a positive topic; it also means thinking about how the technology is used, whether it could mislead people, who it affects, and whether its benefits justify its costs.
