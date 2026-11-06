# The Last Customer

**AI for Good — Hackathon 4: Picture the Planet**
*A short AI-generated animated film about extreme heat, street vendors and climate-resilient market infrastructure in Delhi, India.*

**Author:** Pavitra Pradeep
**Demo video:** <https://youtu.be/oyakxVfGqs0>
**SDG:** 13 — Climate Action (Targets 13.1 and 13.3)
**Tool:** ComfyUI (node-based image, video and audio generation)

---

## Project at a glance

| Item | Detail |
|---|---|
| Project title | The Last Customer |
| Deliverable | Eight-shot animated short film, about 28.33 s in the workflow's target timing, with generated instrumental music |
| Tool | ComfyUI |
| Image model | FLUX.2 Klein 4B (FP8 checkpoint) |
| Video model | Wan 2.2 TI2V 5B, quantised GGUF Q6_K |
| Text encoders and VAEs | Qwen 3 4B; UMT5 XXL FP8; FLUX.2 VAE; Wan 2.2 VAE |
| Audio model | ACE-Step 1.5, instrumental music generation |
| Custom node | ComfyUI-GGUF |
| Video format | 1280 × 720, 24 fps (workflow output target) |
| Workflow file | `ramesh_film_4GB_workflow.json` |
| Primary audience | Delhi municipal ward-level officials and urban-market planners responsible for public-market infrastructure and street-vending facilities |
| People the intervention is intended to benefit | Street vendors working in exposed outdoor markets, including fruit and food vendors |
| Demo video | <https://youtu.be/oyakxVfGqs0> |
| Final MP4 | `[TO CONFIRM: path or link to the exported final MP4]` |

---

## Contents

1. [The project](#1-the-project)
2. [Problem definition](#2-problem-definition)
3. [SDG 13: Climate Action](#3-sdg-13-climate-action)
4. [User group and stakeholders](#4-user-group-and-stakeholders)
5. [Solution: the film](#5-solution-the-film)
6. [How the ComfyUI workflow works](#6-how-the-comfyui-workflow-works)
7. [Reproducing the workflow](#7-reproducing-the-workflow)
8. [Evaluation and limitations](#8-evaluation-and-limitations)
9. [Ethical reflection](#9-ethical-reflection)
10. [AI use and project transparency](#10-ai-use-and-project-transparency)
11. [Sources](#11-sources)
12. [Before submission](#12-before-submission)

---

## 1. The project

Extreme heat is usually discussed as temperature records, heatwaves and public-health warnings. For people who work outdoors, heat is also a workplace and livelihood issue. Street vendors may spend long hours in exposed public spaces, often without reliable access to shade, drinking water or other basic facilities. When temperatures rise, the consequences can include fewer customers, shorter working hours, damaged goods, health problems and lost income.

Our film, **The Last Customer**, tells this issue through Ramesh, a fictional 45-year-old fruit vendor at an outdoor market in Delhi. The film follows him through a hot day: he opens his stall, works in direct sunlight, sees customers disappear and watches his fruit deteriorate. A municipal official notices the conditions. The ending imagines a practical improvement: a durable shade canopy over the vending area and an accessible public drinking-water point.

The film does not claim that one canopy or one water tap solves extreme heat, poverty or the wider challenges facing informal workers. It uses one market as an example of local adaptation infrastructure.

**Central message:**

> Shade. Water. Protection. Climate-resilient markets protect the people who keep our cities running.

Ramesh, the customer, the municipal official and the market are fictional. The evidence about heat impacts comes from published research, not from the events shown in the animation.

---

## 2. Problem definition

### Extreme heat is also a livelihood and workplace issue

Delhi's street vendors work in public spaces that expose them to direct sunlight and high temperatures for long periods. Unlike many indoor workers, vendors may have no air-conditioned room, no reliable shade or drinking water, and no way to stop working without losing income. Their exposure depends on how the places where they work are designed and managed, not only on the weather.

Telling a vendor to drink more water or take a break is not enough when clean water, shade and a safe place to rest are not available at the worksite. Heat protection therefore belongs in market planning and public-space infrastructure.

### Evidence: findings from Delhi

The main evidence is WIEGO Policy Brief No. 34, *Working in the Heat: Street Vendors and Climate Justice in Delhi, India* (Sinha, Unni, Pegu and Valdivia, 2026). The research used two rounds of surveys with nearly 500 street vendors, infrastructure mapping across 17 markets, interviews and policy analysis, covering conditions around the 2025 summer heat.

The brief reports:

- **96%** of surveyed vendors experienced a drop in customer numbers during extreme heat.
- **90%** reduced their working hours because of the heat.
- **72%** reported income losses due to heat damage to their goods.
- None of the 17 mapped markets had municipal water access at the vending sites.
- Serious gaps in shade or shelter and toilet facilities were also found.

These percentages describe the vendors in the study. They are not percentages of every street vendor in Delhi or India, and they are not a measurement of every market or every summer.

Food vendors are especially affected, because perishable goods are damaged by heat. A separate report on the WIEGO study notes that 94% of food vendors surveyed reported damage to goods. We treat this as a subgroup finding, not as a figure for all vendors.

### What the statistics mean for the film

| Research finding | How the film communicates it |
|---|---|
| 96% reported fewer customers | Ramesh's stall grows quieter as pedestrians hurry through the heat. |
| 90% reduced working hours | The film shows the difficulty of working in direct sunlight. It does not claim a number of hours lost by Ramesh. |
| 72% reported income losses from heat damage | Fruit visibly deteriorates, representing the risk to perishable stock. |
| No municipal water access in the 17 mapped markets | The final scene introduces an accessible public drinking-water point as a proposed improvement. |
| Lack of adequate shade or shelter | A durable canopy is introduced over the vending area. |

The percentages are not presented as Ramesh's personal statistics. Any figure shown on screen must be attributed to the WIEGO study and identified as a survey finding.

### The specific problem

The problem is not that vendors fail to protect themselves. It is that many outdoor vending locations lack basic infrastructure that would help workers cope with severe heat. Without shade, drinking water and suitable facilities, vendors carry a disproportionate share of the physical and economic costs.

**Our question:** how can municipal market planning make outdoor vending areas safer and more resilient during extreme heat?

The film highlights two measures, shade and accessible drinking water. They are not a complete heat-action plan. They are visible, understandable examples of climate adaptation infrastructure.

---

## 3. SDG 13: Climate Action

The project addresses **SDG 13, Climate Action**, through two targets.

**Target 13.1: Strengthen resilience and adaptive capacity.** The film applies this to a specific urban setting: outdoor markets where vendors are exposed to extreme heat. Shade structures and drinking-water points are practical local adaptation measures that reduce exposure and help public spaces function during hot conditions.

**Target 13.3: Education and awareness.** The film contributes to awareness by making the livelihood effects of extreme heat visible and by showing how local infrastructure decisions support adaptation.

The project is about **adaptation**, not emissions reduction. It does not claim that the canopy or water point reduces greenhouse-gas emissions.

---

## 4. User group and stakeholders

### Primary audience: municipal decision-makers

The primary audience is **Delhi municipal ward-level officials and urban-market planners** who influence public-market infrastructure, vending locations and local heat-resilience measures. They are the audience because the proposed intervention depends on public-space planning and on providing and maintaining shared facilities, not only on individual vendors changing their behaviour.

The film is designed to be understood in a short viewing. It presents one human example, links it to documented research, and ends with a clear infrastructure message: include shade and accessible drinking-water points in market planning.

**What this audience needs to understand:**

- Extreme heat affects vendors' health, working hours, customers and goods.
- These impacts are connected to the conditions of the public spaces where vendors work.
- Shade and drinking water should be treated as part of heat-resilient market infrastructure.
- Vendors should be included in planning decisions, because they know the conditions and practical needs of their worksites.

### Who benefits

Street vendors are the intended beneficiaries. Customers and other market users may also benefit from shaded public areas and accessible water. The film does not claim that the depicted intervention has been installed in a real market or that its effects have been measured.

### Who is not the primary audience

The film is not primarily designed for:

- Tourists seeking general information about Delhi.
- Individual vendors seeking medical diagnosis or personal heat-stress treatment.
- Climate scientists looking for new temperature or epidemiological data.
- Municipal engineers seeking construction specifications or cost estimates.
- National policymakers looking for a complete heat-action policy.

These groups may still find the film relevant, but it is a short awareness and advocacy piece, not a technical design, medical guide or policy evaluation.

### Stakeholders whose perspectives matter

- **Street vendors:** experience the heat exposure and its effects on livelihoods directly.
- **Vendor organisations and worker representatives:** can communicate workers' priorities and support meaningful consultation.
- **Municipal authorities:** influence public-space design, facilities, maintenance and enforcement.
- **Customers and market visitors:** use the same spaces and may benefit from better heat protection.
- **Public-health and climate-adaptation organisations:** can advise on heat-risk reduction and local resilience.

The film does not replace consultation with these groups. Vendors should help shape the location, design and management of any real intervention.

---

## 5. Solution: the film

### Narrative structure

The film is an eight-shot animation. It moves from the ordinary start of a working day, through the effects of heat, to a practical infrastructure response. The ending is deliberately local: one market area with shade and a water point. It does not show a city transformed overnight.

### Shot list

Each shot is 85 frames at 24 fps, about 3.54 seconds. Prompts and negative prompts are given in the shot-list document. Single-frame previews go in `storyboard/`.

| Shot | Duration | Scene | Purpose | Frame |
|---|---:|---|---|---|
| 1 | 3.54 s | Ramesh opens his fruit stall and arranges mangoes, bananas, oranges and watermelons in the morning market. | Introduces the vendor, his work and the setting. | `storyboard/shot_1.png` |
| 2 | 3.54 s | The afternoon sun becomes harsh. Ramesh wipes sweat while working in direct sunlight. | Makes heat exposure visible. | `storyboard/shot_2.png` |
| 3 | 3.54 s | Customers become scarce as pedestrians hurry past the exposed stall. | Represents the reported decline in customers. | `storyboard/shot_3.png` |
| 4 | 3.54 s | Fruit looks damaged and Ramesh appears exhausted. | Represents the risk to perishable goods and livelihood. | `storyboard/shot_4.png` |
| 5 | 3.54 s | A municipal official notices the exposed stall while Ramesh gestures towards the sun and the lack of facilities. | Introduces municipal responsibility. | `storyboard/shot_5.png` |
| 6 | 3.54 s | A durable shade canopy and a public drinking-water point appear in the market. | Presents the practical adaptation idea. | `storyboard/shot_6.png` |
| 7 | 3.54 s | Ramesh serves a customer under the canopy while another vendor drinks water nearby. | Shows how shared infrastructure could improve working conditions. | `storyboard/shot_7.png` |
| 8 | 3.54 s | A wide view of the market shows the canopy and water point as part of the public space. | Ends on the climate-resilient market message. | `storyboard/shot_8.png` |

**Target duration:** 8 × 85 frames ÷ 24 fps = **28.33 seconds**. This is the duration implied by the workflow settings. It must be checked against the exported MP4 (see [Before submission](#12-before-submission)).

### Character and visual direction

Ramesh is a fictional 45-year-old Indian fruit vendor, designed to stay consistent across the eight shots:

- Warm brown skin, short black hair and a thick black moustache.
- Cream cotton shirt and faded green apron.
- Dark trousers and brown sandals.
- Wooden fruit cart with mangoes, bananas, oranges and watermelons.

The setting is an outdoor Delhi market with fruit carts, Hindi shop signage, scooters, an auto-rickshaw, overhead wires and dense shopfronts. These details establish the location; they do not represent one real market.

The style is traditional hand-drawn 2D cartoon animation: bold black outlines, flat cel shading, expressive movement and painted backgrounds. The negative prompts discourage photorealism, live-action appearance, 3D rendering, CGI and anime styles.

Character-reference images are passed into later keyframe branches to help keep Ramesh's appearance, clothes, cart and setting consistent. This improves continuity but does not guarantee identical appearance in every frame.

---

## 6. How the ComfyUI workflow works

The supplied graph has 194 nodes and 297 links. It generates the eight shots, creates the instrumental score and assembles the clips into one film from a single queued workflow. It is not a single text prompt sent to a video generator; it has separate keyframe, animation, decoding, resizing, encoding, audio and assembly stages.

### 1. Keyframes

Each shot starts from a still keyframe generated with FLUX.2 Klein 4B, using the Qwen 3 4B text encoder and the FLUX.2 VAE.

- Canvas: 1360 × 768.
- Sampling: 28 steps, CFG 5.
- Later shots receive earlier reference images to keep the character and setting consistent.
- Prompts specify the action, framing, character details, market environment and 2D style. Negative prompts discourage inconsistent features, unwanted styles, malformed anatomy, text artefacts and unrelated objects.

### 2. Animation

Each keyframe is passed to a Wan 2.2 TI2V 5B image-to-video node. The supplied workflow uses a quantised **Q6_K GGUF** model rather than the larger 14B expert models of the full-quality graph.

- Generation resolution: 1280 × 704.
- Frames per shot: 85, at 24 fps.
- Sampling: 20 steps, CFG 5, sampler `uni_pc`.
- Tiled VAE decoding reduces peak memory use.
- Clips are resized to 1280 × 720.

### 3. Soundtrack

ACE-Step 1.5 generates an instrumental score inside the workflow. The prompt asks for a gentle cinematic Indian instrumental with sitar, bansuri flute, light tabla, tanpura drone and warm strings, moving from reflective and tense towards a hopeful ending. The score contains no synthetic narrator and no voice clone.

### 4. Assembly

The workflow encodes the eight clips and joins them in order with the video concatenation nodes, with the soundtrack included. The graph's note describes one queued run producing eight keyframes, eight shot clips and an approximately 28.33-second film.

### Overview

```text
Text prompts + reference images
              |
              v
       FLUX.2 Klein 4B
       8 keyframe branches
              |
              v
       Wan 2.2 TI2V 5B
       8 image-to-video branches
              |
              v
       Tiled VAE decoding
              |
              v
       Resize to 1280 x 720
              |
              v
       Encode 8 shot clips  <---- ACE-Step 1.5 instrumental score
              |                              |
              +---------------+--------------+
                              |
                              v
                    Concatenate / assemble
                              |
                              v
                      Final film output
```

---

## 7. Reproducing the workflow

### Requirements

- ComfyUI installed and running.
- The custom node **ComfyUI-GGUF** installed and loaded.
- Enough system RAM, GPU memory and disk space for the model files and intermediate frames.
- The model files below placed in the correct ComfyUI model folders.

### Model files referenced by the workflow

| Model role | Filename in the workflow |
|---|---|
| Qwen text encoder for FLUX.2 | `qwen_3_4b.safetensors` |
| FLUX.2 VAE | `flux2-vae.safetensors` |
| FLUX.2 Klein 4B checkpoint | `flux-2-klein-base-4b-fp8.safetensors` |
| UMT5 text encoder for Wan | `umt5_xxl_fp8_e4m3fn_scaled.safetensors` |
| Wan 2.2 VAE | `wan2.2_vae.safetensors` |
| Wan 2.2 TI2V 5B GGUF | `Wan2.2-TI2V-5B-Q6_K.gguf` |
| ACE-Step audio model | `ace_step_1.5_turbo_aio.safetensors` |

Folder placement depends on the loader nodes and the installed ComfyUI-GGUF extension. If ComfyUI reports missing models, use the loader's expected model category and the extension's instructions, not renamed files.

### Run instructions

1. Install or update ComfyUI to a version compatible with the loaders and custom nodes.
2. Install **ComfyUI-GGUF** and restart ComfyUI.
3. Download the model files above from their official repositories and place them in the relevant model directories.
4. Restart ComfyUI so it refreshes its model list.
5. Load `ramesh_film_4GB_workflow.json`.
6. Check for missing-node or missing-model warnings. Confirm the FLUX.2, Wan GGUF and ACE-Step loaders have the intended files selected.
7. Queue the workflow. It runs all eight shot branches and the final assembly.
8. Keep the machine on power and monitor GPU memory, system memory, disk space and logs.
9. Check the keyframes and clips before treating the output as complete. If a shot has a continuity or motion problem, revise its prompt or seed and regenerate that shot.
10. Open the final MP4 and verify duration, resolution, frame rate, audio, shot order and playback.

### Hardware note

The workflow's note estimates 6–12 hours on an RTX 2050 laptop with 4 GB VRAM and 16 GB RAM. That is the workflow author's estimate for that setup, not a benchmark for other hardware.

An NVIDIA GTX 1080 with 8 GB VRAM was also considered. It has more VRAM, but it is a Pascal-generation GPU without native FP8 tensor-core support, and the workflow uses FP8 model files and newer runtime components. Eight gigabytes of VRAM does not guarantee compatibility. PyTorch, ComfyUI, CUDA and custom-node versions must be checked on the actual machine. The workflow should be described as tested on a given machine only after a complete run and a verified final MP4 on that machine.

### Expected outputs

- Eight keyframes.
- Eight animated shot clips.
- One generated instrumental soundtrack.
- One concatenated final film.

Record the actual output directory and filenames after running the graph. Do not assume a file exists just because its node is present.

---

## 8. Evaluation and limitations

### What counts as a successful prototype?

The project is evaluated on both the film and the reproducibility of the workflow.

| Area | What to check |
|---|---|
| Duration | Final video is 25–35 seconds. The workflow target is 28.33 seconds. |
| Shot count | Final film has 6–10 shots. This workflow is designed for eight. |
| Resolution | Export is at least 720p. Workflow target is 1280 × 720. |
| Continuity | Ramesh's face, moustache, hair, clothing, cart and market setting remain recognisable across shots. |
| Narrative | The film moves from heat exposure to its livelihood effects and then to a practical adaptation measure. |
| Audio | Instrumental score is audible, balanced and free of unintended speech or artefacts. |
| Evidence | Any number shown on screen is accurate, attributed and not presented as Ramesh's personal data. |
| Reproducibility | The workflow JSON opens without missing nodes or models and can be queued on the documented setup. |
| Transparency | The film and README disclose that the images, animation and soundtrack are AI-generated. |

### Limitations

- The film is a short awareness piece, not a heat-risk assessment, medical intervention or engineering plan.
- Ramesh is fictional. His experience is inspired by research findings, not a real interview or case study.
- The film shows one market and two infrastructure measures. Delhi's heat-resilience needs are broader: toilets, electricity, rest facilities, early warnings, worker protections, social protection and inclusive governance.
- A generated canopy and water point do not show that an intervention has been installed, funded, maintained or evaluated in a real market.
- AI imagery can contain inaccurate Hindi signage, street details, hands or fruit. The setting is not documentary evidence.
- Reference images improve consistency but do not guarantee identical appearance in every frame.
- Resolution and duration are graph settings. The exported file still needs technical verification.
- The workflow's runtime estimate is not a measured result on any machine.

---

## 9. Ethical reflection

### Representation: a fictional character standing in for many workers

A single fictional character can make a varied group of workers look more uniform than it is. Vendors differ in gender, age, health, migration history, goods sold, family support, legal status, location and ability to stop work. A male fruit vendor cannot represent all of these experiences.

We reduce this risk by labelling Ramesh as fictional and grounding the wider problem in research with nearly 500 vendors. We do not claim that Ramesh took part in the survey, that his experience is statistically typical, or that every vendor experiences heat the same way. A stronger future version would involve vendor organisations and, with informed consent, real vendors' own perspectives.

### Dignity and stereotypes

AI image generation can reproduce stereotypes about people, occupations, countries and cities, and can make characters look exaggerated or helpless. We designed Ramesh as a working person with agency: he opens his stall, arranges his goods, serves customers and tells the official about his conditions. He is not portrayed as lazy or incapable.

Delhi should not appear as an anonymous place of chaos or poverty. The market details establish a location and should not become shorthand for a stereotype. The stylised hand-drawn look also avoids presenting generated scenes as real documentary footage. The film does not copy the face or identity of any real vendor or official.

### Accuracy and misleading viewers

A short film compresses a complicated issue, which makes it easy to imply more than the evidence supports. The film shows fruit deteriorating, but that does not mean every vendor loses stock every day. The canopy and water point show a possible intervention, not a completed project. The ending must not imply that one small intervention solves heat exposure or guarantees higher income.

We separate research findings from fictional scenes. The percentages come from WIEGO's research, not from observations of Ramesh. Figures placed on screen must name their source and population. We do not invent temperatures, deaths, income amounts, diagnoses, cost savings or measured effects of the canopy.

### Responsibility: not shifting the burden onto workers

Telling vendors to drink water, work less or find shade puts the burden on individuals when the problem is the absence of facilities in public spaces. Reducing working hours can also reduce income. The film therefore does not end with Ramesh buying a hat or deciding to work less. It ends with a shared infrastructure response.

The municipal official shows that local authorities have a role in planning, providing and maintaining heat-resilient public spaces. The film must not imply that one official can solve the problem alone, or that installing a canopy is simple. Real interventions need budgets, permissions, safe design, maintenance, accessible placement and consultation with vendors.

### Fairness and who may be overlooked

A canopy and a water point do not meet every worker's needs. Women vendors may have different safety, sanitation and care responsibilities. Vendors with disabilities, older workers, mobile vendors and those without formal recognition face other barriers. A water point can exist and still be inaccessible, unsafe, unreliable or poorly maintained. Shade can be unevenly distributed.

The proposed intervention is a starting point, not a universal answer. Real planning should assess accessibility, gender safety, maintenance, water quality, location, opening hours and the needs of different vendor groups, and should consider toilets, rest areas, heat warnings and worker participation.

### AI imagery and false documentary evidence

All visuals are generated with AI image and video models. The characters and events are not recordings of real people or a real intervention. Realistic details, official-looking clothing or familiar city features could be mistaken for documentary evidence if the film is shared without explanation.

We therefore disclose that the film is AI-generated and that Ramesh and the events are fictional. We do not use a real person's likeness, fabricate a testimonial, or attribute dialogue to a real vendor or official. Any public upload should keep this disclosure in the description or end credits.

### Environmental cost

Generating eight keyframes, eight video clips and a soundtrack consumes electricity and computing resources. It would be inconsistent to promote climate resilience without acknowledging that cost.

The workflow's runtime figure is an estimate, not a measurement. We do not yet have a verified record of power draw, total GPU energy, failed attempts or electricity use, so we do not state a kWh or CO₂e figure. An honest measurement would record:

- The GPU and computer used.
- Total time spent on keyframes, video, audio and failed attempts.
- The number of complete and partial generations.
- Measured system power during generation, ideally from a wall-power meter.
- Electricity use in kWh, and the emissions factor used to convert it to CO₂e.

GPU power limits or a model's rated power are not the same as measured whole-system consumption. To reduce waste, prompts and keyframes should be checked before all video branches run, and reference images reused where appropriate.

### Human oversight

The workflow generates images, motion and music. It does not decide which infrastructure should be built or whether a real market is safe. The team is responsible for checking factual claims, reviewing generated scenes, selecting the final edit and explaining the limits of the story. Municipal officials and vendors, not the model, would need to assess any real intervention.

**Ethical position.** AI-generated animation can make a documented climate issue easier to understand, especially in a short film. Creative impact does not justify inventing evidence, speaking for workers or presenting a fictional intervention as a real solution. The film uses animation to draw attention to a real, research-supported problem, and states clearly what is fictional, what is evidenced and what lies outside the project's scope.

---

## 10. AI use and project transparency

- **Images:** generated in ComfyUI with FLUX.2 Klein 4B.
- **Video:** generated in ComfyUI with Wan 2.2 TI2V 5B GGUF Q6_K.
- **Audio:** instrumental soundtrack generated in ComfyUI with ACE-Step 1.5.
- **Editing and assembly:** the supplied workflow includes clip resizing, encoding and concatenation.
- **Human contribution:** the team is responsible for the concept, research framing, audience, story, prompts, workflow configuration, output review, factual verification and final submission.
- **Real people:** no real vendor's face or personal testimony is represented. Ramesh and the official are fictional.
- **Disclosure:** the film is labelled as AI-generated animation based on published research, and its characters and events are fictional.

---

## 11. Sources

1. Sinha, S., Unni, A., Pegu, R. and Valdivia, M. (2026). **Working in the Heat: Street Vendors and Climate Justice in Delhi, India.** WIEGO Policy Brief No. 34. [Publication page](https://www.wiego.org/research-library-publications/working-heat-street-vendors-delhi-india/) · [Full policy brief (PDF)](https://www.wiego.org/wp-content/uploads/2026/02/WIEGO-Policy-Brief-34.pdf). Main source for the vendor survey, livelihood impacts and infrastructure mapping across 17 markets.
2. Down To Earth (5 March 2026). **Heatwave cuts working hours for 90 per cent of Delhi street vendors, survey finds.** [Article](https://www.downtoearth.org.in/governance/heatwave-cuts-working-hours-for-90-per-cent-of-delhi-street-vendors-survey-finds). Secondary reporting on the WIEGO research, including food-vendor subgroup findings.
3. United Nations Department of Economic and Social Affairs. **Goal 13: Take urgent action to combat climate change and its impacts.** [SDG 13 targets and indicators](https://sdgs.un.org/goals/goal13). Source for Targets 13.1 and 13.3.
4. ComfyUI. [Official repository](https://github.com/comfyanonymous/ComfyUI). Node-based generative workflow interface.
5. ComfyUI-GGUF. [Custom-node repository](https://github.com/city96/ComfyUI-GGUF). GGUF model loader used by the workflow.
6. Wan-AI. [Wan 2.2 repository](https://github.com/Wan-Video/Wan2.2). Model family used for image-to-video.
7. Black Forest Labs. [FLUX.2 Klein model information](https://huggingface.co/black-forest-labs). Model family used for keyframes. Use the exact repository for the checkpoint actually downloaded.

---

## 12. Before submission

- [ ] Run the complete workflow successfully on the machine used for the final generation.
- [ ] Confirm the final MP4 is 25–35 seconds, has 6–10 shots and is at least 720p.
- [ ] Record the actual frame rate, resolution, runtime and output filename from the exported video.
- [ ] Record the GPU and system RAM used for the final run.
- [ ] Record the number of keyframe, video and audio generations, including failed or repeated attempts.
- [ ] Measure or transparently estimate electricity use. Do not state an energy or CO₂e figure without measurement.
- [ ] Watch the full film for character consistency, motion artefacts, incorrect details and audio problems.
- [ ] Confirm the narration and music comply with the hackathon's sound rules before publishing.
- [ ] Add the final YouTube link and confirm it is public or unlisted.
- [ ] Include the workflow JSON, the shot list with prompts and negative prompts, and one frame per shot in `storyboard/`.
- [ ] Keep the AI-generated and fictional-story disclosure with the published video.
