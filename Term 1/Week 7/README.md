# Term 1 - Week 7: Computer Vision

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

Eyes on Earth

**My pair partner:**

Jalie Vermeegen

**Tool we had to use:**

Roboflow

**SDG we had to address:**

SDG 15: Life on Land — specifically Target 15.5, which focuses on reducing habitat degradation, protecting threatened species, and halting biodiversity loss.

**What problem does it solve, and for whom?**

Our project addresses the problem of discarded cigarette butts in parks, forests, gardens, and other green spaces in the Netherlands. These butts can harm animals, release toxic substances into the environment, and contribute to pollution. Our main intended users are Dutch municipal staff, park and forest rangers, and landowners who need to identify areas requiring cleaning but have limited time and resources to inspect them manually.


**What did you build?**

We built an AI-powered object-detection prototype using Roboflow and an RF-DETR model. Users can upload a photo of a green space through a Streamlit application, detect visible cigarette butts using bounding boxes, adjust the confidence threshold, and view or download the annotated image. The estimated counts can help users prioritise cleaning and identify potential litter hotspots, although human verification is still necessary.


**Link to the live thing (if any):**

Demo video: https://www.youtube.com/watch?v=v33Kw0U_xJ8

LIVE APP: https://hackaton7-k4bhbahenvwyn6vqiueuvh.streamlit.app/ -> repo and files here

TO RUN LOCALLY: See the how to run it locally in the section below. IMPORTANT the requires weights.pt file is too big for github, this will thus be in a different folder. There will be a link provided to this

SECOND IMPORTANT NOTICE: The code for the LIVE-APP and Locally run app are different!

**How do I run it?**
Install Python 3.12.

Download hackaton7.py and weights.pt from the links above and place them in the same folder.

Open a terminal in that folder and create a virtual environment:

python -m venv .venv

Activate the environment and install the dependencies:

pip install streamlit rfdetr Pillow

Start the application:

streamlit run hackaton7.py

Open the local URL displayed in the terminal, upload an image, choose a confidence threshold, and click Detect cigarette butts.

The model runs locally on the CPU, so no API key or Roboflow credits are required. Processing may take some time.



**Who did what?**

We worked together to brainstorm the project idea, collect the dataset, and develop the overall concept. Jalie primarily handled the model training and testing using Roboflow, while both of us collaborated throughout the project to achieve our goal of detecting cigarette butts in green spaces and addressing environmental pollution.

**Ethical reflection - what are the risks of your tool? Who could it harm?**

Our tool could help municipalities and park rangers identify cigarette-litter hotspots, but its predictions are not always correct. In our evaluation, the selected Medium model achieved 90.1% precision and 60.7% recall, meaning that it missed around 39% of labelled cigarette butts. False negatives could make polluted areas appear cleaner than they are, while false positives could waste cleaning teams' time and public money. Our dataset contains only 320 images and may not represent different seasons, lighting conditions, locations, or backgrounds. People and private details could also accidentally appear in photographs, so images should be checked before sharing. Furthermore, areas that are photographed less frequently could receive less attention. To reduce these risks, the application labels detections as possible cigarette butts, allows users to adjust the confidence threshold, and warns users to verify results. Photos are processed locally rather than sent to Roboflow by the application. Human inspections and reports from residents should complement the predictions, and the tool should support rather than replace human judgement. Its estimated counts are not proof that an area is clean or that biodiversity has improved.

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

The most important thing I learned this week is how AI object-detection models can be trained to identify real-world problems using images and a labelled dataset. I also learned that a model can make mistakes, so evaluating its performance and checking its predictions are important before using it in real situations.

**Where does this connect to "AI for Good"?**

Our project connects to AI for Good because it uses object detection to identify cigarette butts in green spaces, helping municipalities and park rangers prioritise cleaning and reduce environmental pollution. It also taught me that AI should support human decision-making rather than replace it, because missed detections could cause polluted areas to be overlooked.
