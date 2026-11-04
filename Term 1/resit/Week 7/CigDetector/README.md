# CigDetector --- AI-Powered Cigarette Litter Detection

**AI FOR GOOD \| Hackathon 7: Eyes on Earth**

*Computer Vision · Roboflow · RF-DETR · Python · Streamlit*

  Project information    Details
  ---------------------- --------------------------------------------
  Project                CigDetector
  Student                Pavitra Pradeep
  Hackathon              Hackathon 7 --- Eyes on Earth
  Required tool          Roboflow
  Detection model        RF-DETR Medium
  SDG                    SDG 15 --- Life on Land
  Programming language   Python
  Application            Streamlit
  Inference              Local, using a downloaded model checkpoint

------------------------------------------------------------------------

## 1. Project overview

CigDetector is a computer vision application designed to detect and
count discarded cigarette butts in photographs of outdoor environments,
including parks, gardens, forest paths and other green spaces in the
Netherlands.

Cigarette butts are small and can blend into soil, grass, leaves and
other surroundings. Manually inspecting photographs and counting
individual pieces of litter can be time-consuming. CigDetector uses an
object detection model to identify possible cigarette butts, mark their
locations with bounding boxes and provide an estimated count.

The application uses a model trained through the Roboflow workflow and
integrates the resulting RF-DETR Medium checkpoint into a Streamlit
interface. A user can upload a photograph, run detection, inspect
confidence scores and download an annotated result.

CigDetector is intended as a supporting tool for environmental
monitoring. It does not replace physical inspections or determine
whether an area is environmentally safe.

## 2. Problem definition: cigarette litter in green spaces

Discarded cigarette butts are a visible form of litter in public outdoor
spaces. Cigarette filters can retain chemical residues, and discarded
filters may expose soil, water and wildlife to pollutants. Cigarette
litter can also accumulate in places that are difficult to inspect
consistently.

This creates a practical monitoring problem for people responsible for
maintaining parks, gardens, recreational areas and other green spaces.
Staff and volunteers may need to inspect many locations, while small
cigarette butts can be difficult to notice in photographs.

**The problem addressed by CigDetector is:** how can computer vision
help identify and count visible cigarette butts in photographs of Dutch
outdoor environments, so that people can review locations that may need
cleaning?

The prototype focuses on one clearly defined object class: discarded
cigarette butts. It does not attempt to detect all types of litter or
measure chemical contamination.

## 3. SDG relevance --- SDG 15: Life on Land

CigDetector addresses **United Nations Sustainable Development Goal 15:
Life on Land**, particularly the broader aim of protecting terrestrial
ecosystems and reducing environmental degradation.

Discarded cigarette filters can remain in outdoor environments and may
release harmful substances. Identifying visible cigarette litter can
support monitoring and help maintenance teams decide where further
inspection or cleaning may be useful.

The intended contribution is indirect:

1.  A user photographs an outdoor area.
2.  CigDetector identifies possible cigarette butts in the photograph.
3.  The user reviews the detections and estimated count.
4.  The information can help the user decide whether the location needs
    further inspection or cleaning.

The application does not itself remove litter, measure biodiversity or
prove an improvement in ecosystem health. It provides a tool that may
support people working towards cleaner terrestrial environments.

## 4. Intended users

### Primary users

The primary intended users are municipal environmental maintenance teams
in the Netherlands who are responsible for public parks, gardens,
recreational spaces and other green areas.

They may already collect photographs during inspections. CigDetector
could help them review those photographs by highlighting possible
cigarette litter for human verification.

### Other potential users

-   Park and forest rangers.
-   Landowners and grounds-maintenance teams.
-   Environmental organisations.
-   Local volunteers involved in litter monitoring.

### Who is not the intended user?

CigDetector is not designed to identify individual smokers, determine
who discarded litter, measure chemical contamination or make automatic
municipal enforcement decisions. It is also not a replacement for
physical inspections.

The current prototype processes one photograph at a time and requires a
computer capable of running the model locally.

## 5. Solution: what the application does

CigDetector is a working image-upload and object-detection application.

### Input

The user uploads a photograph in JPG, JPEG, PNG or WEBP format.

### Processing

1.  Streamlit receives the uploaded image.
2.  Pillow opens the image, applies EXIF orientation correction and
    converts it to RGB.
3.  The application loads the trained RF-DETR Medium model from the
    local `weights.pt` checkpoint.
4.  The image is passed to the model for prediction.
5.  The user-selected confidence threshold filters predictions.
6.  The application draws a bounding box and confidence label for each
    remaining detection.

### Output

The application displays:

-   The original photograph.
-   The annotated photograph with predicted cigarette butts highlighted.
-   The number of possible cigarette butts detected.
-   A confidence score for each displayed detection.
-   A download option for the annotated PNG image.

The application also reminds users that predictions need human review
and that no detections do not necessarily mean an area is clean.

### Workflow

``` text
Photograph uploaded by user
          |
          v
     Streamlit app
          |
          v
  Pillow image processing
          |
          v
 Local RF-DETR Medium model
       (weights.pt)
          |
          v
    Object detection
          |
          v
 Confidence-threshold filtering
          |
          v
 Bounding boxes and estimated count
          |
          v
 Annotated image and download
```

## 6. Roboflow dataset and manual annotation

Roboflow was the required tool for this hackathon. It was used for the
computer vision dataset workflow, including image management, annotation
and model training.

The original project dataset contained **320 labelled images** of
discarded cigarettes and cigarette butts collected in outdoor
environments in the Netherlands.

Images were labelled with bounding boxes using the class name
`cigarette_butts`.

### My individual dataset contribution

I personally contributed photographs to the dataset, uploaded images to
the Roboflow workspace and manually annotated cigarette butts using the
bounding-box annotation interface.

My annotation work involved:

1.  Opening photographs in Roboflow.
2.  Identifying visible cigarette butts.
3.  Drawing bounding boxes around the objects.
4.  Assigning the `cigarette_butts` class.
5.  Checking the labels to ensure that the intended objects were marked.
6.  Preparing labelled images for the object-detection workflow.

This manual annotation work is important because an object detection
model learns from examples that indicate both what an object is and
where it appears in an image.

### Original dataset split

  Dataset subset      Images   Percentage
  ---------------- --------- ------------
  Training               224          70%
  Validation              64          20%
  Testing                 32          10%
  **Total**          **320**     **100%**

The training subset was used for model learning, the validation subset
supported development and model selection, and the test subset was
reserved for evaluation on images not used for training.

*The figures above describe the original project dataset. The final
resit repository should include the actual Roboflow dataset/version
evidence so that the image count and split can be checked.*

## 7. Model development and evaluation

The original project explored different object detection models and
model sizes. RF-DETR Small and RF-DETR Medium were evaluated, and YOLO26
was also explored. RF-DETR Medium was selected for the application based
on the reported evaluation results.

RF-DETR is an object detection model. Unlike a simple image classifier,
which would only classify an entire photograph, an object detector
predicts the locations of objects within the image. This makes it
suitable for CigDetector because the application needs to highlight and
count individual cigarette butts.

### Original reported model comparison

  Metric                   RF-DETR Small   RF-DETR Medium
  ---------------------- --------------- ----------------
  Confidence threshold               37%              47%
  Precision                        80.2%            90.1%
  Recall                           62.0%            60.7%
  F1 score                         69.9%            72.5%
  mAP@50                           69.8%            71.8%
  False positives                     23               10
  False negatives                     57               59

These are the original project's reported results, not a new independent
evaluation conducted for this resit.

### What the metrics mean

-   **Precision:** the proportion of predicted objects that were
    correct. Higher precision means fewer false detections.
-   **Recall:** the proportion of actual labelled objects that the model
    detected. Lower recall means more objects were missed.
-   **F1 score:** a combined measure of precision and recall.
-   **mAP@50:** a measure of object-detection performance using an
    intersection-over-union threshold of 0.50.

### Why RF-DETR Medium was selected

The Medium model achieved higher reported precision, F1 score and mAP@50
than the Small model, and produced fewer false positives. The Small
model had slightly higher recall, so the Medium model did not detect
every additional object that the Small model found.

The Medium model was selected as a practical balance for the
application. Its reported starting confidence threshold was 47%.

A confidence threshold is not the same as model accuracy. It controls
the minimum confidence a prediction must have to be displayed. Lowering
the threshold can show more possible detections but may also increase
false positives. Raising it can reduce false positives but may hide
genuine cigarette butts.

## 8. My individual contributions

This resit repository documents the work I personally carried out on the
CigDetector project.

### Dataset contribution and preparation

-   Personally contributed photographs of discarded cigarette butts.
-   Uploaded images to the Roboflow workspace.
-   Helped prepare the image dataset for object detection.

### Manual annotation

-   Personally labelled cigarette butts in Roboflow.
-   Drew bounding boxes around visible objects.
-   Assigned the `cigarette_butts` class.
-   Checked the annotations as part of preparing labelled data.

### Model evaluation

-   Examined the reported evaluation results for RF-DETR Small and
    Medium.
-   Worked with precision, recall, F1 score and mAP@50.
-   Considered false positives and false negatives.
-   Contributed to assessing which model was more suitable for the
    application.

### Application development and local deployment

-   Worked on the Python and Streamlit application that integrates the
    trained model.
-   Set up a Python virtual environment on macOS.
-   Installed and configured the application dependencies.
-   Resolved the missing `rfdetr` dependency during setup.
-   Configured the local model checkpoint path.
-   Integrated the downloaded `weights.pt` checkpoint.
-   Successfully ran the application locally using Streamlit.
-   Tested the image-upload and prediction workflow.
-   Worked on displaying bounding boxes, confidence scores and detection
    counts.
-   Implemented the annotated-image download workflow.

### Documentation and demonstration

-   Prepared the project documentation and README.
-   Documented the problem, intended users, SDG relevance, model
    workflow and limitations.
-   Prepared the application for a working demonstration.

**Training transparency:** The original RF-DETR training experiments
were primarily carried out by my project partner. I do not claim to have
independently performed those original training experiments. My
individual contribution includes the dataset work and manual annotation
described above, evaluation work, application implementation and local
testing, and project documentation. The existing trained checkpoint is
reused for the resit application.

## 9. Technical implementation

  -----------------------------------------------------------------------
  Technology                          Role in the project
  ----------------------------------- -----------------------------------
  Roboflow                            Dataset management, manual
                                      annotation and model-training
                                      workflow

  RF-DETR Medium                      Cigarette-butt object detection

  Python                              Application logic and inference

  PyTorch                             Model execution

  Streamlit                           Interactive user interface

  Pillow                              Image loading, orientation handling
                                      and image annotation

  GitHub                              Source-code hosting and version
                                      control

  Git LFS                             Storage of the large model
                                      checkpoint
  -----------------------------------------------------------------------

### Local inference

The application loads the trained model from `weights.pt`, located in
the same directory as `app.py`.

Predictions are performed locally on the computer running the
application. The application does not send uploaded photographs to a
Roboflow hosted prediction API.

The current implementation uses CPU inference. Performance will depend
on the computer's hardware and the size of the uploaded photograph.

## 10. Ethical reflection and limitations

The dataset consists of photographs of cigarette litter collected in
outdoor environments in the Netherlands. The original dataset contains
320 labelled images, with bounding boxes assigned to visible cigarette
butts. This is a relatively small dataset and cannot represent every
possible location, season, surface, lighting condition or type of
outdoor environment.

The model may miss cigarette butts when they are small, partially
covered by grass or leaves, distant from the camera, or visually similar
to their surroundings. It may also mistake other small objects or debris
for cigarette butts.

The original Medium model's reported recall was 60.7%, meaning that a
substantial proportion of labelled objects were missed in its
evaluation. A photograph with no detections must therefore not be
interpreted as proof that an area is free of cigarette litter.

False negatives could cause a maintenance team to overlook a polluted
location. False positives could lead to unnecessary inspections or
wasted cleaning resources. For this reason, the output should be treated
as an estimate and checked by a person before it informs a real-world
decision.

Photographs taken in public spaces may also contain identifiable people
or other personal information. Images should be reviewed and identifying
details blurred or removed before public sharing. The application
processes images locally, but this does not remove the user's
responsibility to handle photographs appropriately.

The prototype has not been validated in an operational municipal
deployment. It should support human inspection rather than replace it.

## 11. Problem--solution fit

The intended users need a way to review photographs of outdoor spaces
and identify visible cigarette litter. CigDetector addresses this need
by using object detection rather than only classifying an entire image.

A basic image classifier could indicate whether cigarette litter is
present, but it would not show where individual cigarette butts appear
or estimate how many are visible. Object detection is therefore more
appropriate for the task.

The application provides a practical sequence: upload a photograph, run
detection, inspect highlighted objects, review the count and download
the result. It is a working prototype, but it does not yet provide batch
processing, geographical mapping or automatic cleaning recommendations.

## 12. Working prototype and demonstration

The application can be demonstrated end to end:

1.  Start the Streamlit application.
2.  Upload a new photograph.
3.  Adjust the confidence threshold if required.
4.  Run cigarette-butt detection.
5.  Review the annotated image and confidence scores.
6.  Check the estimated detection count.
7.  Download the annotated image.

### Demonstration video

\[Add the demo video link here\]

### Screenshots

Add screenshots to the repository showing:

-   The Roboflow dataset and image annotations.
-   The dataset split and model evaluation.
-   The running Streamlit application.
-   An uploaded photograph.
-   The model's bounding-box predictions and detection count.

## 13. Future improvements

Potential improvements include:

-   Collecting more images from different Dutch outdoor environments.
-   Adding more examples of cigarette butts under different lighting and
    weather conditions.
-   Including photographs without cigarette butts to assess
    false-positive behaviour.
-   Improving recall and reducing missed detections.
-   Supporting batch processing of multiple photographs.
-   Recording inspection locations to identify recurring litter
    hotspots.
-   Testing the application with environmental maintenance teams.
-   Conducting a larger independent evaluation before any operational
    deployment.

## 14. What I learned

This project gave me practical experience with the stages involved in
building a computer vision application, from preparing labelled image
data to integrating a trained model into a usable interface.

Working with Roboflow helped me understand the importance of manual
bounding-box annotation and consistent object labels. Reviewing model
evaluation metrics helped me understand why precision, recall and false
negatives matter differently depending on the intended use of a model.

Integrating RF-DETR into Streamlit gave me experience with Python
environments, dependency installation, model checkpoints, image
processing and local inference. I also learned that a trained model is
not by itself a complete product: users need a working interface, clear
outputs, instructions and an explanation of the model's limitations.

An important lesson from CigDetector is that computer vision predictions
should not be treated as ground truth. Even a model with promising
precision can miss a significant number of objects, so human review
remains essential.

## 15. How to run the application

### Requirements

-   Python 3.12
-   The trained `weights.pt` checkpoint
-   The dependencies listed below
-   A computer capable of running RF-DETR inference

### Repository structure

``` text
CigDetector/
├── app.py
├── weights.pt
├── requirements.txt
├── README.md
├── .gitignore
├── .gitattributes
└── screenshots/
    ├── roboflow_annotations.png
    ├── model_evaluation.png
    └── app_prediction.png
```

### Step 1 --- Clone the repository

``` bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd CigDetector
```

### Step 2 --- Create a virtual environment

``` bash
python3.12 -m venv .venv
```

### Step 3 --- Activate the environment

On macOS or Linux:

``` bash
source .venv/bin/activate
```

### Step 4 --- Install dependencies

``` bash
python -m pip install --upgrade pip
pip install streamlit rfdetr pillow
```

If a `requirements.txt` with tested, pinned package versions is
provided, install using:

``` bash
pip install -r requirements.txt
```

### Step 5 --- Run the application

Make sure `app.py` and `weights.pt` are in the same folder.

``` bash
python -m streamlit run app.py
```

Open the local address printed in the terminal, normally:

``` text
http://localhost:8501
```

Upload a photograph and select **Detect cigarette butts**.

## 16. Project links

-   **GitHub repository:** \[Add repository URL\]
-   **Roboflow workspace:** \[Add Roboflow project URL\]
-   **Demo video:** \[Add video URL\]

------------------------------------------------------------------------

**CigDetector --- AI for Good, Hackathon 7: Eyes on Earth**\
**SDG 15 --- Life on Land**\
**Developed by Pavitra Pradeep**
