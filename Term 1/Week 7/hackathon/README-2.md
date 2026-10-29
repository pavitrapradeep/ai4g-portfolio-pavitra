**Project title:**
Eyes on Earth

**My pair partner:**
Pavitra Pradeep/Jalie Vermeegen

**Tool we had to use:**
Roboflow  

**Demo video:**
[H7 - Demo](https://www.youtube.com/watch?v=v33Kw0U_xJ8)

## SDG we had to address:

SDG 15: Life on Land, especially **target 15.5**, which calls for reducing the degradation of natural habitats, halting biodiversity loss and protecting threatened species [1]. Our project focuses on cigarette litter in forests, parks, personal gardens, and small urban green spaces in the Netherlands. These places can provide habitats for plants and animals, even when they are small or managed by people.

Detecting discarded cigarette butts can help managers like forest-rangers of the local municipality identify places that need cleaning and decide where to focus prevention. This supports the habitat-protection part of target 15.5 by helping reduce one source of pollution. Our contribution is indirect: detecting this litter does not itself remove it or prove that biodiversity improves.

## What problem does it solve, and for whom?

Cigarette butts in green spaces are more than just an eyesore. Animals can accidentally swallow them and be exposed to toxic substances. Research documents ingestion and poisoning in pets, although evidence about the frequency and effects of ingestion in wild animals is more limited, this does show a sign of it being toxic to animals if ingested [2]. Nicotine can also leach from the cigarette butts into soil and be taken up by nearby plants [3]. A greenhouse experiment found that cigarette filters reduced germination and shoot growth in grass and clover [4]. Repeated littering in the same area therefore creates a concern for the healt of the soil and vegetation there, although these studies do not establish a universal harmful number of butts, it still does show that the cigarettes have a toxic influence in the areas they get discarded in.

A cigarette that is still burning can also ignite dry vegetation. For example, Canadian police reported a brush fire near Whitbourne in August 2025 that fire officials believed was started by a carelessly discarded cigarette butt [5]. This is an additional reason to prevent littering, particularly during dry conditions.

Our main intended user is a dutch municipality, park/forest rangers and landowners in the Netherlands who want to tackle this littering issue of specifically cigarette butts. These people often decide where cleaning teams should work and where anti-littering measures are needed. A secondary user could be volunteer groups or just the average everyday person who sees this litter and wants to take action. This tool can thus be used for either preventive measures or proactive measures.

For these users, the problem is deciding where limited cleaning time and budgets are most needed. Cigarette butts are small and can be scattered between grass, leaves and soil, making manual counting across repeated inspection photos time-consuming. Without a consistent overview, staff may struggle to identify which locations need extra cleaning and where litter keeps returning. Our tool helps them review and count visible butts in each photo, supporting these decisions while leaving the final judgement to the user.

The idea is to use photos from inspections to identify cigarette-litter hotspots. If many butts are visible in one location, the coordinator can prioritise a cleanup. If litter repeatedly appears around the same benches or entrances, they can place targeted signs or run local awareness campaigns about disposing of cigarettes properly. An example of this is a short film against forest-fires. This specific short film tries to spread awareness of the danger of discarding/being careless with flammable material, which cigarettes are a part of. Follow-up inspections can help check whether litter returns. These are intended uses; the model alone does not map locations or prove that a campaign works.

People without access to a suitable camera, internet connection or the skills to use the tool may be excluded. Areas that are photographed less often may receive less attention, even if they have a serious litter problem. The user group should therefore combine the detections with regular inspections and reports from residents when deciding where to act.

[1] [United Nations — SDG 15 and target 15.5](https://sdgs.un.org/goals/goal15)  
[2] [Novotny et al. (2011) — Tobacco and cigarette butt consumption in humans and animals](https://pmc.ncbi.nlm.nih.gov/articles/PMC3088460/)  
[3] [Selmar et al. (2018) — Uptake of nicotine from discarded cigarette butts](https://www.sciencedirect.com/science/article/abs/pii/S0269749117346304)  
[4] [Green et al. (2019) — Effects of cigarette butts on grass and clover growth](https://pubmed.ncbi.nlm.nih.gov/31327493/)  
[5] [RCMP (2025) — Suspected cigarette-caused brush fire near Whitbourne](https://rcmp.ca/en/nl/news/2025/08/rcmp-nl-pleads-motorists-not-toss-their-butts-after-discarded-cigarette-sparks-small-fire-near)

## What did you build and what was the purpose?

We made an object-detection model using Roboflow to detect discarded cigarettes and cigarette butts in photos of natural areas, including but not limited to forests, parks and gardens. The model marks individual cigarettes and butts with bounding boxes. There was one class that these cigarettes would be labeled under which was `cigarette_butts`.

The app follows this flow: a user uploads a photo in Streamlit, the local RF-DETR model generates detections, and a confidence threshold filters out predictions below the selected score. The app then displays bounding boxes and a count of possible cigarette butts. The user can review the detections and download the annotated image.

The purpose is to help municipal staff and park rangers review and count visible cigarette litter across inspection photos without having to examine every image manually. These counts can help a maintenance coordinator prioritise cleanups. When photos are linked to locations and inspection dates, they can also help identify places where cigarette litter repeatedly returns. This supports decisions about where targeted signs, awareness campaigns or disposal facilities may be needed.

The main benefit is supporting staff who repeatedly review many inspection photos from different locations or dates. The current app processes one uploaded photo at a time; it does not automatically process entire photo collections. Users still need to check the detections, since hidden or partly covered butts may be missed.

## Roboflow explanation

We created our own image dataset by taking photos of discarded cigarettes and cigarette butts. We uploaded these to Roboflow and manually drew bounding boxes around the visible cigarettes and butts, using one class: cigarette_butts.  
<img width="398" height="176" alt="image" src="https://github.com/user-attachments/assets/bc09b623-f1c4-404e-910f-6e0884669a05" />

Our dataset contains 320 pictures, 224 of those for training, 64 of those for validation and 32 of those for testing.  
Which is a 70/20/10 split for the training of the model. We chose a **70/20/10 split** to keep most images available for training while reserving separate images for validation and testing. The 20% validation set helps us compare models and choose a confidence threshold. The remaining 10% is kept separate for the final evaluation on unseen images. And also because it was recommended by Roboflow itself.  
<img width="481" height="147" alt="image" src="https://github.com/user-attachments/assets/0498685c-5e7d-420d-bf95-7bb3380a9ba6" />

**Which errors matter most?** False negatives are our main concern because these are real cigarette butts that the model misses. This could make a polluted location appear cleaner than it is and receive less attention. False positives also matter because incorrect detections inflate counts and create unnecessary work for municipal staff.

Therefore, **recall is our main priority**, while precision helps keep the results practical. Ordinary accuracy is less suitable for object detection because there is no clear count of all the background objects correctly ignored. We therefore use precision, recall, F1 and mAP to assess the models.

With only 32 test images, the results should still be interpreted cautiously. More independent and varied test images could make the evaluation more reliable, but they would not automatically make the model itself more accurate. The training images are used to teach the model, the validation images help evaluate it during development, and the test images are kept separate for the final evaluation. It was decided to train two model sizes from the Roboflow RF-DETR models: Small and Medium. This was done through using the 'custom-training' option in Roboflow as you can see in the image below, after that small and medium were picked. This model was picked because it allegedly needs less data which seems a good pick for our limited 320 image dataset.
<img width="789" height="222" alt="image" src="https://github.com/user-attachments/assets/5d0be3cb-4550-4cba-a84a-09a6eaf6448a" />
<img width="838" height="145" alt="image" src="https://github.com/user-attachments/assets/f59f757d-86fc-4dbf-80d1-6eea08dc651f" />


A small test was done with another model, being YOLO26, however the results of that one were a lot worse compared to the RF-DETR model. So this one was dropped altogether and not compared in the end. Results of this one can be shown here:
<img width="861" height="164" alt="image" src="https://github.com/user-attachments/assets/8ec54fca-3675-46f8-afcb-bf1e0ed7b7f3" />
This model was not picked since every metric was just significantly lower than the other model, it also had a recall of below 50%.




## Results & conclusion  
We trained and evaluated two Roboflow RF-DETR model sizes to see how the program works and which one would be the best for the idea we had: Small and Medium. The table shows their reported test results at their respective suggested confidence thresholds.

| Metric                     | Small  | Medium |
|----------------------------|--------|--------|
| Confidence threshold       | 37%    | 47%    |
| Precision                  | 80.2%  | 90.1%  |
| Recall                     | 62.0%  | 60.7%  |
| F1 score                   | 69.9%  | 72.5%  |
| mAP@50                     | 69.8%  | 71.8%  |
| Correct detections         | 93     | 91     |
| False negatives            | 57     | 59     |
| False positives            | 23     | 10     |
| Reported Cloud API latency | 5.1 ms | 9.2 ms |

<img width="871" height="137" alt="image" src="https://github.com/user-attachments/assets/31769712-aaee-4cfd-b11a-ecf438e19e86" />


**Confidence thresholds:** Roboflow suggested 37% for Small and 47% for Medium as the optimal balance based on F1. Predictions below these thresholds are filtered out. These percentages are confidence settings, not accuracy scores. A lower threshold generally allows more real butts to be detected, but can also introduce more false positives.

**Which model size did we choose?** We chose the **Medium model because it offers the better overall balance**. Yes the recall for the small model is better and the priority is recall, however small detected only two additional butts, while Medium produced 13 fewer false positives. Medium’s precision was substantially higher, and it also achieved better F1 and mAP@50 scores. For municipal staff reviewing inspection photos, this means fewer incorrect detections to check while finding almost the same number of real butts.

Although recall is our priority, its small difference does not outweigh Medium’s improvements in the other metrics. We use **47% as our starting confidence threshold**. This minimum confidence means that only detections with a model score of 0.47 or higher are shown; predictions below this score are hidden. The score expresses the model’s confidence in a detection, but it is not a verified probability that the detection is correct and does not mean the model has 47% accuracy. Increasing the threshold usually removes more uncertain detections but can also hide real butts. Lowering it can reveal more butts while also introducing more false positives. A possible next step is to try a lower threshold on the validation set and check whether the additional detections justify any increase in false positives.

Both models still missed around 38–39% of labelled butts at these settings. Their results should therefore support human inspections rather than be treated as complete litter counts.

## How to run it

1. Install Python 3.12.
2. Download `hackaton7.py` via [this link](https://github.com/JiwiKiwi/AI-For-Good-JalieVermeegen/blob/main/Term%201/Week%207/hackathon/hackaton7/hackaton7.py) and `weights.pt` via [this link](https://github.com/JiwiKiwi/AI-For-Good-JalieVermeegen/releases/tag/hackaton) and put them in the same folder.
3. Open a terminal in that folder and run:

   ```powershell
   cd "C:\Users\<Yourname>\Downloads\<Your Folder>"         
   py -3.12 -m venv .venv312
   .\.venv312\Scripts\python.exe -m pip install streamlit rfdetr Pillow
   ```

4. Start the app:

   ```powershell
   .\.venv312\Scripts\python.exe -m streamlit run hackaton7.py
   ```

5. Open the local URL shown in the terminal, usually http://localhost:8501. Upload a photo, choose a confidence threshold (default: 47%) and click Detect cigarette butts.

The model runs locally on your CPU, so no API key or Roboflow credits are needed. Processing can take some time. Internet is needed to install the packages.

Link to the live thing

For the video, see the demo:[ H7 - Demo.](https://www.youtube.com/watch?v=v33Kw0U_xJ8)

For the application code, see https://github.com/pavitrapradeep/ai4g-portfolio-pavitra/blob/63dbda62cfd30b57dd1eaed79f5d27d0ea291ca4/Term%201/Week%207/hackathon/hackaton7.py

IMPORTANT: The model weights file was too large to upload directly to GitHub. Download it from the hackaton release page. https://github.com/pavitrapradeep/ai4g-portfolio-pavitra/blob/04246d138b091cf0f56e9687199b4df3853acb1b/Term%201/Week%207/hackathon/weights.pt


## Ethical reflection

We collected our own photos and videos of discarded cigarettes and cigarette butts in public spaces and manually labelled the visible butts in Roboflow. Our dataset contains 320 images, but it does not represent every location, season, lighting condition or background where the tool might be used. Photos taken in public can also accidentally include identifiable people or personal details. We recommend checks before sharing to remove or blur these details and verify that similar photos or frames from the same video stay in the same dataset split. While labeling our own data we removed as much of those details as possible. 

Our selected Medium model achieved **90.1% precision and 60.7% recall**, with 91 correct detections, 59 missed butts and 10 false positives in the reported evaluation. This means it missed around 39% of labelled butts. Small objects, partial coverage by grass or leaves or other vegetation, and limited variation in the dataset are possible explanations, but the scores alone do not establish the cause. Our training data also contained no images without cigarette butts, limiting the examples of clean scenes or any other pictures like taken in the dark/other seasons/etc. A recommended next step is collecting more varied images, including clean areas and more objects that resemble butts beyond twigs and leaves like candy wrappers; these additions have not yet been made in the current dataset. More training alone does not guarantee improvement however and changes should be checked on validation data before a separate final evaluation.

Another risk is if users treat the predictions as facts and don’t double check from time to time, incorrect results could affect real decisions. False positives could lead to unnecessary inspections or cleaning crews being sent to an area, wasting time and money. False negatives could make a polluted area appear clean, causing it to receive no cleanup. Areas photographed less often could also be overlooked. One measure already implemented is an in-app warning to check the results and that no detections does not mean the area is clean. Another issue is also that the picture alone does not point towards where the litter is, so people who make these pictures have to manually mark where these area's are. The app also labels its count as possible cigarette butts, allows users to adjust the confidence threshold, and processes photos locally rather than sending them to Roboflow. Human review before sending cleaning teams, regular inspections and reports from residents are recommended safeguards for real use; we have not tested them in a municipal deployment. Its counts are estimates of visible cigarette litter, not proof that an area is clean or a measurement of environmental damage. Users should use this tool as support for their judgement rather than as the sole basis for cleaning decisions.
