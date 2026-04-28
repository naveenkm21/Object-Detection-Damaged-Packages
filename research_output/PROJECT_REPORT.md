# SMARTFLOW: AUTOMATED DEFECT DETECTION SYSTEM USING YOLOv8 FOR DAMAGED PARCEL DETECTION IN LOGISTICS

**21CSP302L – PROJECT**

*Submitted by*

**ISHANT SINGH [REG NUM]**
**NAVEEN KUMAR MOHANARAJAN [REG NUM]**

*Under the Guidance of*

**Dr. PRIYADHARSHINI K**
*(Designation, Department of Computing Technologies)*

*in partial fulfillment of the requirements for the degree of*

**BACHELOR OF TECHNOLOGY**
in
**COMPUTER SCIENCE ENGINEERING**
*with specialization in (SPECIALIZATION NAME)*

**DEPARTMENT OF COMPUTATIONAL INTELLIGENCE
COLLEGE OF ENGINEERING AND TECHNOLOGY
SRM INSTITUTE OF SCIENCE AND TECHNOLOGY
KATTANKULATHUR – 603 203**

**MAY 2026**

---

## OWN WORK DECLARATION FORM

Department of Computational Intelligence
SRM Institute of Science & Technology

This sheet must be filled in (each box ticked to show that the condition has been met). It must be signed and dated along with your student registration number and included with all assignments you submit – work will not be marked unless this is done.

**Degree / Course:** B.Tech Computer Science and Engineering
**Student Names:** Ishant Singh; Naveen Kumar Mohanarajan
**Registration Numbers:** [REG1]; [REG2]
**Title of Work:** SmartFlow: Automated Defect Detection System using YOLOv8 for Damaged Parcel Detection in Logistics

We hereby certify that this assessment complies with the University's Rules and Regulations relating to Academic misconduct and plagiarism, as listed in the University Website, Regulations, and the Education Committee guidelines.

We confirm that all the work contained in this assessment is our own except where indicated, and that we have met the following conditions:

- ☑ Clearly referenced / listed all sources as appropriate.
- ☑ Referenced and put in inverted commas all quoted text (from books, web, etc.).
- ☑ Given the sources of all pictures, data etc. that are not our own.
- ☑ Not made any use of the report(s) or essay(s) of any other student(s) either past or present.
- ☑ Acknowledged in appropriate places any help that we have received from others.
- ☑ Complied with any other plagiarism criteria specified in the Course handbook / University website.

**DECLARATION:** We are aware of and understand the University's policy on Academic misconduct and plagiarism and we certify that this assessment is our own work, except where indicated by referring, and that we have followed the good academic practices noted above.

<<Student 1 Name & Sign>>      <<Student 2 Name & Sign>>

---

## BONAFIDE CERTIFICATE

**SRM INSTITUTE OF SCIENCE AND TECHNOLOGY, KATTANKULATHUR – 603 203**

Certified that the 21CSP302L – Project report titled **"SmartFlow: Automated Defect Detection System using YOLOv8 for Damaged Parcel Detection in Logistics"** is the *bonafide* work of **Ishant Singh [REG NUM]** and **Naveen Kumar Mohanarajan [REG NUM]** who carried out the project work under my supervision. Certified further, that to the best of my knowledge the work reported herein does not form any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.

| SIGNATURE | SIGNATURE |
|---|---|
| **Dr. PRIYADHARSHINI K** | **DR. R. ANNIE UTHRA** |
| SUPERVISOR | PROFESSOR & HEAD |
| Professor | DEPARTMENT OF |
| Department of Computing Technologies | COMPUTATIONAL INTELLIGENCE |

Examiner 1: __________________  Examiner 2: __________________

---

## ACKNOWLEDGEMENTS

We express our humble gratitude to **Dr. C. Muthamizhchelvan**, Vice-Chancellor, SRM Institute of Science and Technology, for the facilities extended for the project work and his continued support.

We extend our sincere thanks to **Dr. Leenus Jesu Martin M**, Dean-CET, SRM Institute of Science and Technology, for his invaluable support.

We wish to thank **Dr. Revathi Venkataraman**, Professor and Chairperson, School of Computing, SRM Institute of Science and Technology, for her support throughout the project work.

We encompass our sincere thanks to **Dr. M. Pushpalatha**, Professor and Associate Chairperson - CS, and **Dr. C. Lakshmi**, Professor and Associate Chairperson - AI, School of Computing, SRM Institute of Science and Technology, for their invaluable support.

We are incredibly grateful to our Head of the Department, **Dr. R. Annie Uthra**, Professor and Head, Department of Computational Intelligence, for her suggestions and encouragement at all stages of the project work.

We convey our thanks to our Project Coordinators, Panel Head, and Panel Members, Department of Computational Intelligence, SRM Institute of Science and Technology, for their inputs during the project reviews and continued support.

We register our immeasurable thanks to our Faculty Advisor, **……………**, Department of Computational Intelligence, SRM Institute of Science and Technology, for leading and helping us to complete our course.

Our inexpressible respect and thanks to our guide, **Dr. Priyadharshini K** and co-guide **Dr. Sowmiya B**, Department of Computing Technologies, SRM Institute of Science and Technology, for providing us with an opportunity to pursue our project under their mentorship. They provided us with the freedom and support to explore our area of interest in computer vision for logistics quality control. Their passion for solving real-world problems has always been inspiring.

We sincerely thank all the staff members of the Department of Computational Intelligence, School of Computing, SRM Institute of Science and Technology, for their help during our project. Finally, we would like to thank our parents, family members, and friends for their unconditional love, constant support, and encouragement.

**Authors
Ishant Singh
Naveen Kumar Mohanarajan**

---

## ABSTRACT

Automated visual inspection for package defects is critical in logistics and supply chain quality control, where manual inspection is labor-intensive, subjective, and prone to errors. Defects such as scratches, dents, misalignments, and water damage can occur during handling, packing, transit, or unloading, and the cost of a missed defect (false negative) is typically far higher than that of a false positive. This project presents **SmartFlow**, an automated defect detection system that leverages state-of-the-art YOLO (You Only Look Once) architectures to inspect packages at key logistics stages: warehouse dispatch, loading, transit checkpoints, and final delivery.

A rigorous comparative analysis of three medium-complexity YOLO variants—**YOLOv8m**, **YOLOv11m**, and **YOLOv12s**—was performed on a custom package defect dataset of 10,000 high-resolution images. Using full training logs over 150 epochs (100 for YOLOv12s), models were evaluated on detection accuracy (Precision, Recall, F1-score, mAP50, mAP50-95), training stability (coefficient of variation of validation mAP50-95), convergence behavior, and efficiency.

Results demonstrate that **YOLOv8m** achieves the highest F1-score (**0.759**) and mAP50-95 (**0.403**), indicating a superior balance between precision and recall and excellent localization accuracy. YOLOv11m attains competitive mAP50-95 (0.396) but suffers from lower recall (F1 = 0.733) and moderate training instability. YOLOv12s, while 57 % faster to train, exhibits early training instability and lower overall accuracy (F1 = 0.739, mAP50-95 = 0.395). Based on these findings, YOLOv8m is recommended as the core detection engine for the SmartFlow system, deployed via a Streamlit web application that allows users to upload parcel images and view annotated detections in real time. The system can be integrated at multiple stages of the logistics pipeline to detect mishandling and shipping defects, ensuring product quality from warehouse to customer delivery.

**Keywords:** Object Detection, YOLOv8, Damaged Parcel Detection, F1-score, mAP, Training Stability, Logistics Quality Control, Industry 4.0.

---

## TABLE OF CONTENTS

| Chapter No. | Title | Page No. |
|---|---|---|
|  | ABSTRACT | iii |
|  | TABLE OF CONTENTS | iv |
|  | LIST OF FIGURES | v |
|  | LIST OF TABLES | vi |
|  | ABBREVIATIONS | vii |
| **1** | **INTRODUCTION** | **1** |
|  | 1.1 Introduction to Project | 2 |
|  | 1.2 Motivation | 3 |
|  | 1.3 Problem Statement and Description | 4 |
|  | 1.4 Sustainable Development Goal of the Project | 5 |
|  | 1.5 Product Vision Statement | 5 |
|  | 1.6 Product Goal | 6 |
|  | 1.7 Product Backlog (Key User Stories with Desired Outcomes) | 7 |
|  | 1.8 Product Release Plan | 8 |
| **2** | **SPRINT PLANNING AND EXECUTION** | **9** |
|  | 2.1 Sprint 1 – Dataset Curation & YOLOv8m Baseline | 10 |
|  | 2.1.1 Sprint Goal with User Stories of Sprint 1 | 11 |
|  | 2.1.2 Functional Document | 12 |
|  | 2.1.3 Architecture Document | 13 |
|  | 2.1.4 UI Design | 14 |
|  | 2.1.5 Functional Test Cases | 15 |
|  | 2.1.6 Daily Call Progress | 16 |
|  | 2.1.7 Committed vs Completed User Stories | 17 |
|  | 2.1.8 Sprint Retrospective | 18 |
|  | 2.2 Sprint 2 – Comparative Study & Streamlit Deployment | 19 |
|  | 2.2.1 Sprint Goal with User Stories of Sprint 2 | 20 |
|  | 2.2.2 Functional Document | 21 |
|  | 2.2.3 Architecture Document | 22 |
|  | 2.2.4 UI Design | 23 |
|  | 2.2.5 Functional Test Cases | 24 |
|  | 2.2.6 Daily Call Progress | 25 |
|  | 2.2.7 Committed vs Completed User Stories | 26 |
|  | 2.2.8 Sprint Retrospective | 27 |
| **3** | **RESULTS AND DISCUSSIONS** | **28** |
|  | 3.1 Project Outcomes | 29 |
|  | 3.2 Total Committed vs Completed User Stories | 30 |
| **4** | **CONCLUSIONS & FUTURE ENHANCEMENT** | 31 |
|  | REFERENCES | 32 |
|  | APPENDIX | 33 |
|  | A. Patent Disclosure Form / Publication Details | 34 |
|  | B. Sample Coding with Screenshots | 35 |
|  | C. Plagiarism Report | 36 |

---

## LIST OF FIGURES

| Fig. No. | Title | Page |
|---|---|---|
| 1.1 | High-level logistics inspection pipeline targeted by SmartFlow | 2 |
| 1.2 | Product release timeline across two sprints | 8 |
| 2.1 | Sprint 1 architecture – data ingestion to YOLOv8m baseline | 13 |
| 2.2 | Sprint 1 UI wireframe – upload + confidence slider | 14 |
| 2.3 | Sprint 2 architecture – model comparison and Streamlit serving | 22 |
| 2.4 | Sprint 2 UI – annotated detection view & metrics table | 23 |
| 3.1 | F1-score evolution across 150 epochs (YOLOv8m / v11m / v12s) | 29 |
| 3.2 | mAP50-95 evolution across epochs | 29 |
| 3.3 | Training loss curves (box, cls, dfl) | 30 |
| 3.4 | Validation loss curves | 30 |

## LIST OF TABLES

| Table No. | Title | Page |
|---|---|---|
| 1.1 | Product backlog – user stories and desired outcomes | 7 |
| 2.1 | Sprint 1 functional test cases | 15 |
| 2.2 | Sprint 1 committed vs completed user stories | 17 |
| 2.3 | Sprint 2 functional test cases | 24 |
| 2.4 | Sprint 2 committed vs completed user stories | 26 |
| 3.1 | Best performance metrics across models | 29 |
| 3.2 | Efficiency comparison (training time & GFLOPs) | 30 |
| 3.3 | Total committed vs completed stories | 30 |

## ABBREVIATIONS

| Abbreviation | Expansion |
|---|---|
| YOLO | You Only Look Once |
| CNN | Convolutional Neural Network |
| mAP | mean Average Precision |
| IoU | Intersection over Union |
| CIoU | Complete Intersection over Union |
| BCE | Binary Cross-Entropy |
| DFL | Distribution Focal Loss |
| SGD | Stochastic Gradient Descent |
| CV | Coefficient of Variation |
| GFLOPs | Giga Floating-Point Operations |
| GPU | Graphics Processing Unit |
| SDG | Sustainable Development Goal |
| UI / UX | User Interface / User Experience |
| API | Application Programming Interface |
| PANet | Path Aggregation Network |
| CSP | Cross Stage Partial |

---

# CHAPTER 1
# INTRODUCTION

## 1.1 Introduction to Project

In modern logistics and supply chain operations, ensuring product quality throughout the shipping process is paramount. Packages pass through multiple stages—warehouse dispatch, loading onto trucks, transit checkpoints, and final delivery—and at each stage they may suffer damage due to mishandling, improper stacking, or environmental factors such as moisture. Defects include scratches, dents, misalignments, water damage, and colour inconsistencies. Manual inspection of every parcel is labour-intensive, subjective, and prone to error, especially at scale.

The **SmartFlow** project is an automated defect detection system built around deep-learning based computer vision. It uses the YOLO (You Only Look Once) family of single-stage object detectors to identify damage in parcel images in real time. The system is trained on a curated dataset of 10,000 high-resolution parcel images (1920 × 1080) annotated by domain experts with axis-aligned bounding boxes around each defect.

The project delivers three artefacts:
1. A trained YOLOv8m model fine-tuned for package defect detection.
2. A comparative study of YOLOv8m, YOLOv11m, and YOLOv12s evaluating detection accuracy, training stability, convergence, and efficiency.
3. A Streamlit web application (`streamlit_app.py`) that lets a logistics operator upload a parcel image, adjust the confidence threshold, and view annotated detections alongside a class/confidence table.

## 1.2 Motivation

Three observations drive this work:

1. **Economic impact of missed defects.** In logistics, a single defective package reaching a customer causes returns, compensation, brand damage, and churn. The cost of a false negative therefore far exceeds that of a false positive, and recall must be treated as a first-class metric, not an after-thought.
2. **Limits of manual inspection.** Human inspectors tire, disagree, and simply cannot keep up with the throughput of modern fulfilment centres. Automated, 24×7 visual inspection is the only realistic path to consistent quality at scale.
3. **Ambiguity in YOLO version selection.** New YOLO versions appear every few months (v8, v11, v12) with improvements benchmarked on COCO. COCO performance does not translate directly to specialised industrial tasks, where defects are small, varied, and subtle. A principled comparative study on a logistics-specific dataset is therefore needed before committing to a production model.

## 1.3 Problem Statement and Description

> **Problem Statement:** *Given an image of a parcel captured at any stage of the logistics pipeline, automatically detect and localise all visible defects (scratches, dents, misalignments, wet / water-damaged regions, holes) with sufficient precision and recall to be used as the basis for operational decisions (re-pack, replace, flag handling point) without routine human review.*

**Formal formulation.** Let an image *I* contain a set of defects **D = {d₁, d₂, …, dₙ}**, each with a bounding box *bᵢ = (xᵢ, yᵢ, wᵢ, hᵢ)* and class label *cᵢ ∈ {hole, wet, scratch, dent, misalignment}*. A detector *f* predicts a set **D̂ = {(b̂ⱼ, ĉⱼ, p̂ⱼ)}*, where *p̂ⱼ* is a confidence score. *f* is trained to minimise the composite loss:

$$L = \lambda_{box}L_{box} + \lambda_{cls}L_{cls} + \lambda_{dfl}L_{dfl}$$

where *L_box* is CIoU loss for bounding-box regression, *L_cls* is binary cross-entropy for classification, and *L_dfl* is distribution focal loss.

**Sub-problems addressed:**

1. Curate and annotate a domain-specific dataset that reflects real packaging, lighting, and damage patterns.
2. Select an architecture that balances accuracy and speed for edge-side deployment.
3. Quantify the precision / recall trade-off, not just mean average precision, since logistics cares about recall.
4. Measure training *stability*, because industrial deployment cannot tolerate a model that behaves differently after every re-training.
5. Package the trained model into a usable interface that a non-ML operator can run.

## 1.4 Sustainable Development Goal of the Project

SmartFlow directly supports the United Nations Sustainable Development Goals:

- **SDG 9 – Industry, Innovation, and Infrastructure:** Automates quality control in industrial supply chains, a canonical Industry 4.0 use-case.
- **SDG 12 – Responsible Consumption and Production:** By catching damaged parcels early, fewer products reach landfills as returns or damaged write-offs, reducing material waste.
- **SDG 8 – Decent Work and Economic Growth:** Relieves workers of repetitive, eye-straining manual inspection while improving logistics productivity.

## 1.5 Product Vision Statement

> *For* logistics operators and e-commerce fulfilment centres *who* need to guarantee parcel quality at every handoff, *SmartFlow* is *a deep-learning based parcel inspection system* that *detects damage and mishandling in real time at warehouse dispatch, loading, transit checkpoints, and final delivery.* Unlike *manual inspection or generic COCO-trained detectors*, our product *is tuned to real logistics defects, reports balanced precision / recall, and runs through a no-code Streamlit interface.*

## 1.6 Product Goal

Deliver, in two sprints, a deployable damaged-parcel detection product that:

- Achieves **F1 ≥ 0.75** and **mAP50-95 ≥ 0.40** on the held-out test set.
- Exposes an upload-and-detect web UI with confidence control, completing a single prediction in under two seconds on commodity GPU hardware.
- Is backed by a reproducible, fully-logged comparative study of at least three modern YOLO variants, so that the choice of detector is evidence-based rather than driven by hype.

## 1.7 Product Backlog (Key User Stories with Desired Outcomes)

**Table 1.1 – Product Backlog**

| ID | User Story | Desired Outcome | Priority |
|---|---|---|---|
| US-01 | As a logistics ML engineer, I want a clean, split parcel-defect dataset so that training is reproducible. | Dataset split 70/20/10 (train / val / test), no image overlap. | High |
| US-02 | As an ML engineer, I want a YOLOv8m baseline fine-tuned on the dataset so that I have a reference point. | Trained `best.pt`, per-epoch metric logs. | High |
| US-03 | As a researcher, I want to train YOLOv11m and YOLOv12s under identical hyperparameters. | Three comparable runs, same optimiser / LR / batch / resolution. | High |
| US-04 | As a researcher, I want F1, mAP50, mAP50-95, and CV-stability reported per model. | Comparative metric table and curves. | High |
| US-05 | As a warehouse operator, I want to upload a parcel image and see annotated defects. | Streamlit web app with bounding-box overlay. | High |
| US-06 | As an operator, I want to tune the confidence threshold interactively. | Slider in UI; live re-rendering. | Medium |
| US-07 | As an operator, I want a tabular breakdown of detected classes and confidences. | Detection table under the image. | Medium |
| US-08 | As a reviewer, I want training loss / validation curves saved to disk. | Figures in `research_output/`. | Medium |
| US-09 | As a deployment engineer, I want `requirements.txt` pinned so the app installs cleanly. | Working `pip install -r requirements.txt`. | Medium |
| US-10 | As a researcher, I want an efficiency comparison (training time, GFLOPs). | Table in report and paper. | Low |

## 1.8 Product Release Plan

| Release | Scope | Target Date |
|---|---|---|
| R1 (end of Sprint 1) | Dataset prepared; YOLOv8m baseline trained; internal CLI-based prediction demo. | End of Sprint 1 |
| R2 (end of Sprint 2) | YOLOv11m and YOLOv12s trained; full metric comparison; Streamlit app (`streamlit_app.py`) deployed locally; final report & research paper. | End of Sprint 2 |

---

# CHAPTER 2
# SPRINT PLANNING AND EXECUTION

## 2.1 Sprint 1 — Dataset Curation and YOLOv8m Baseline

**Duration:** Weeks 1 – 5
**Sprint Theme:** Establish a reproducible data pipeline and train a strong YOLOv8m baseline.

### 2.1.1 Sprint Goal with User Stories of Sprint 1

**Sprint 1 Goal.** By the end of Sprint 1, we will have a cleanly-split, expert-annotated parcel-defect dataset and a fully-trained YOLOv8m model whose per-epoch metrics are logged to disk, enabling comparative analysis in Sprint 2.

Stories pulled into Sprint 1: **US-01, US-02, US-08, US-09**.

### 2.1.2 Functional Document

- **FR-1.1 Dataset ingestion.** Load 10,000 parcel images (1920×1080) with YOLO-format annotations.
- **FR-1.2 Split.** Produce train (70 %, 7 000), val (20 %, 2 000), test (10 %, 1 000) with no image overlap.
- **FR-1.3 Augmentation.** Random horizontal flip (0.5), rotation (±10°), scale (0.5–1.5×), colour jitter (±0.2 brightness / contrast / saturation), mosaic augmentation; resize to 640×640.
- **FR-1.4 Training.** Fine-tune YOLOv8m from COCO-pretrained weights on NVIDIA A100 40 GB, SGD (m = 0.937, wd = 5e-4), lr 0.01 → 1e-5 cosine, batch 16, 150 epochs, CIoU + BCE + DFL losses.
- **FR-1.5 Logging.** Write per-epoch box/cls/dfl losses, val losses, Precision, Recall, mAP50, mAP50-95 to CSV and produce evolution plots.

### 2.1.3 Architecture Document

```
                       ┌───────────────────────────┐
 Raw parcel images ──▶ │ 01_prepare_dataset.py     │──▶ dataset/{train,val,test}
                       └───────────────────────────┘
                                    │
                                    ▼
                       ┌───────────────────────────┐
                       │ 02_train_yolov8m.py       │──▶ results/.../best.pt
                       │  (Ultralytics YOLO API)   │      + results.csv
                       └───────────────────────────┘
                                    │
                                    ▼
                       ┌───────────────────────────┐
                       │ 06_research_metrics.py    │──▶ research_output/*.png,*.csv
                       └───────────────────────────┘
```

The YOLOv8m backbone (CSPDarknet) feeds a PANet neck and a decoupled detection head with anchor-free prediction. 25 M parameters, 78.7 GFLOPs at 640×640.

### 2.1.4 UI Design (CLI demo)

Sprint 1 ships a minimal CLI demo only: `python scripts/predict.py --weights results/.../best.pt --source sample.jpg`. A browser-based UI is deferred to Sprint 2.

### 2.1.5 Functional Test Cases

**Table 2.1 – Sprint 1 Functional Test Cases**

| TC | Input | Expected | Status |
|---|---|---|---|
| TC-1.1 | Run `prepare_dataset.py` on raw folder. | 10 000 images split 70/20/10, no overlap. | Pass |
| TC-1.2 | Sanity-check annotation format. | All labels YOLO-normalised in [0, 1]. | Pass |
| TC-1.3 | Launch training for 1 epoch. | `best.pt` / `last.pt` written; no crash. | Pass |
| TC-1.4 | Train full 150 epochs. | Converges; mAP50-95 ≥ 0.38. | Pass (0.403) |
| TC-1.5 | Per-epoch CSV. | 150 rows, all columns populated. | Pass |

### 2.1.6 Daily Call Progress

Daily 15-minute stand-ups (3-question format: *done / doing / blockers*). Representative log:

- **Day 1 – 3:** Raw dataset inventory; duplicate-image scan; class distribution.
- **Day 4 – 6:** Split script; augmentation pipeline verification on 100-image subset.
- **Day 7:** Small smoke-test run (1 epoch) completed.
- **Day 8 – 19:** Full 150-epoch YOLOv8m training; monitor mAP; investigate a minor spike at epoch 42.
- **Day 20:** Save `best.pt`; generate evolution plots; demo to guide.

### 2.1.7 Committed vs Completed User Stories

**Table 2.2 – Sprint 1 Committed vs Completed**

| Story | Committed | Completed |
|---|---|---|
| US-01 Dataset split | ✓ | ✓ |
| US-02 YOLOv8m baseline | ✓ | ✓ |
| US-08 Save training curves | ✓ | ✓ |
| US-09 Pin requirements | ✓ | ✓ |
| **Total** | **4** | **4 (100 %)** |

### 2.1.8 Sprint Retrospective

- **What went well.** Tight scope; early smoke-test caught a mislabelled class; A100 access secured on day one.
- **What went wrong.** Initial augmentation config caused class imbalance (mosaic dropping small-defect crops); fixed by lowering mosaic probability.
- **Actions for Sprint 2.** Add per-class metric dashboard; standardise training command so v11m and v12s runs are byte-for-byte comparable.

## 2.2 Sprint 2 — Comparative Study and Streamlit Deployment

**Duration:** Weeks 6 – 10
**Sprint Theme:** Train competitor models, quantify the precision / recall / stability trade-off, and ship a usable UI.

### 2.2.1 Sprint Goal with User Stories of Sprint 2

**Sprint 2 Goal.** Produce a rigorous three-way comparison of YOLOv8m, YOLOv11m, and YOLOv12s, select the best model on evidence, and deliver a Streamlit web application that serves the chosen model to non-technical users.

Stories pulled into Sprint 2: **US-03, US-04, US-05, US-06, US-07, US-10**.

### 2.2.2 Functional Document

- **FR-2.1** Train YOLOv11m (26 M params, 79.1 GFLOPs) and YOLOv12s (11 M params, 45.2 GFLOPs) under identical hyper-parameters to the YOLOv8m run (v12s uses 100 epochs per original authors' guidance).
- **FR-2.2** Compute best-F1 epoch, best-mAP50-95 epoch, Precision / Recall at those epochs.
- **FR-2.3** Compute coefficient of variation (CV) of validation mAP50-95 over last 50 epochs as a stability metric.
- **FR-2.4** Compute average seconds-per-epoch and total training time.
- **FR-2.5** `streamlit_app.py`: upload image → inference → overlay boxes → show class / confidence table; confidence slider (0.1 – 0.9, default 0.25).
- **FR-2.6** Package `best.pt` at `results/yolov8m_optimized_20260224_1855/weights/best.pt` and load at app start-up.

### 2.2.3 Architecture Document

```
 ┌─────────────┐   image   ┌──────────────────────┐   tensor   ┌──────────────┐
 │ Browser UI  │──────────▶│ streamlit_app.py     │───────────▶│ YOLOv8m best │
 │ (Streamlit) │◀──────────│  - PIL decode        │            │   .pt (CUDA) │
 └─────────────┘  annotated│  - conf slider       │◀──── boxes │              │
                  image +  │  - draw + table      │            └──────────────┘
                  table    └──────────────────────┘
```

Offline, `scripts/06_research_metrics.py` consumes the three `results.csv` files and emits comparison figures to `research_output/`.

### 2.2.4 UI Design

Two-column Streamlit layout:

- **Left:** file uploader (.jpg/.jpeg/.png), confidence slider, model info card.
- **Right:** annotated image with bounding boxes; below it a table with columns *Class, Confidence, x1, y1, x2, y2*.
- **Header:** "SmartFlow – Damaged Parcel Detection (YOLOv8m)".

### 2.2.5 Functional Test Cases

**Table 2.3 – Sprint 2 Functional Test Cases**

| TC | Input | Expected | Status |
|---|---|---|---|
| TC-2.1 | Train YOLOv11m 150 epochs. | Best F1 ≈ 0.733. | Pass (0.733) |
| TC-2.2 | Train YOLOv12s 100 epochs. | Best F1 ≈ 0.739. | Pass (0.739) |
| TC-2.3 | Upload valid JPG to Streamlit. | Annotated image + non-empty table. | Pass |
| TC-2.4 | Upload non-image file. | Friendly error, no crash. | Pass |
| TC-2.5 | Slider 0.25 → 0.75. | Fewer boxes at higher threshold. | Pass |
| TC-2.6 | No defects present. | Image shown; empty table with "No detections". | Pass |
| TC-2.7 | CV(mAP50-95) over last 50 epochs. | YOLOv8m ≤ 0.025. | Pass (0.020) |

### 2.2.6 Daily Call Progress

- **Day 21 – 25:** Standardise training harness; kick off YOLOv11m run.
- **Day 26 – 30:** Begin YOLOv12s run (in parallel on 2nd GPU slice); observed early loss spikes for v12s, confirmed convergence after epoch 60.
- **Day 31 – 34:** Metric aggregation, figure generation (F1, mAP50-95, loss, val-loss curves).
- **Day 35 – 38:** Streamlit prototype; confidence slider; annotated-image rendering via Ultralytics plot API.
- **Day 39:** End-to-end demo on held-out test images to guide.

### 2.2.7 Committed vs Completed User Stories

**Table 2.4 – Sprint 2 Committed vs Completed**

| Story | Committed | Completed |
|---|---|---|
| US-03 v11m + v12s training | ✓ | ✓ |
| US-04 Metric comparison & CV | ✓ | ✓ |
| US-05 Streamlit upload + detect | ✓ | ✓ |
| US-06 Confidence slider | ✓ | ✓ |
| US-07 Detection table | ✓ | ✓ |
| US-10 Efficiency comparison | ✓ | ✓ |
| **Total** | **6** | **6 (100 %)** |

### 2.2.8 Sprint Retrospective

- **What went well.** Identical hyper-parameters across three runs made the comparison genuinely apples-to-apples; Streamlit was the right choice for time-to-demo.
- **What went wrong.** YOLOv12s early-epoch instability cost ~½ day of debugging before we accepted it as an architectural property; documentation for v12s was sparse.
- **Carry-forward to post-release.** Edge deployment on NVIDIA Jetson; per-class recall breakdown; active-learning loop for hard negatives.

---

# CHAPTER 3
# RESULTS AND DISCUSSIONS

## 3.1 Project Outcomes

### 3.1.1 Overall Detection Performance

**Table 3.1 – Best Performance Metrics Across Models**

| Model | Best F1 | Epoch (F1) | Best mAP50-95 | Epoch (mAP) |
|---|---|---|---|---|
| **YOLOv8m**  | **0.759** | 125 | **0.403** | 137 |
| YOLOv11m | 0.733 | 139 | 0.396 | 139 |
| YOLOv12s | 0.739 |  98 | 0.395 |  98 |

At the epoch of best F1:

- **YOLOv8m**: Precision = 0.748, Recall = 0.769 (balanced).
- **YOLOv11m**: Precision = 0.799, Recall = 0.677 (high-precision, low-recall).
- **YOLOv12s**: Precision = 0.766, Recall = 0.714.

At the epoch of best mAP50-95:

- **YOLOv8m**: Precision = 0.798, Recall = 0.720.
- **YOLOv11m**: Precision = 0.799, Recall = 0.677.
- **YOLOv12s**: Precision = 0.766, Recall = 0.714.

### 3.1.2 F1-score Evolution (Fig. 3.1)

YOLOv8m rises quickly, surpassing 0.74 by epoch 50 and maintaining a plateau above 0.75 with minimal fluctuation. YOLOv11m peaks later but never exceeds 0.733 and shows greater oscillation. YOLOv12s climbs rapidly but exhibits moderate fluctuation after epoch 60.

### 3.1.3 mAP50-95 Evolution (Fig. 3.2)

YOLOv8m converges smoothly to the highest value (0.403) with low variance (**CV = 0.020**). YOLOv11m is more variable (CV = 0.039) and peaks slightly later. YOLOv12s converges fastest but stabilises at a slightly lower value with moderate variance.

### 3.1.4 Training and Validation Loss Curves (Figs. 3.3, 3.4)

YOLOv8m losses decrease smoothly and plateau (box 1.78, cls 1.12, dfl 1.98). YOLOv11m losses decrease but with visible oscillation in classification loss. YOLOv12s shows extreme loss spikes in the early epochs, stabilising only after epoch 60. Validation losses mirror these patterns: YOLOv8m is consistently low, YOLOv11m fluctuates moderately, YOLOv12s settles later and slightly higher.

### 3.1.5 Efficiency

**Table 3.2 – Efficiency Comparison**

| Model | Epochs | Avg. Time / Epoch (s) | Total Time (s) | GFLOPs |
|---|---|---|---|---|
| YOLOv8m  | 150 | 255 | 38 250 | 78.7 |
| YOLOv11m | 150 | 255 | 38 250 | 79.1 |
| YOLOv12s | 100 | 163 | 16 300 | 45.2 |

YOLOv12s trains **57 % faster** than the other two, but the speed benefit does not compensate for its lower accuracy and training instability in a high-stakes quality-control setting.

### 3.1.6 Interpretation / Justification of Outcomes vs Goals

| Goal (from §1.6) | Target | Achieved | Verdict |
|---|---|---|---|
| F1-score | ≥ 0.75 | 0.759 (YOLOv8m) | **Met** |
| mAP50-95 | ≥ 0.40 | 0.403 (YOLOv8m) | **Met** |
| Stability (CV of mAP50-95) | Low | 0.020 | **Met** |
| Working Streamlit UI | End-to-end upload → detect | `streamlit_app.py` deployed | **Met** |
| Evidence-based model selection | 3-way comparison | Section 3.1.1 – 3.1.5 | **Met** |

**Why YOLOv8m wins.** Its decoupled head, task-aligned assigner, and anchor-free design simplify learning and improve generalisation. The balanced F1 is exactly what logistics needs: it minimises both missed defects (which reach customers) and false alarms (which waste re-inspection effort). The low CV makes re-training predictable—critical for a production system.

**Why YOLOv11m falls short here.** High precision but compromised recall means many defective parcels would slip through. Low recall is the worst failure mode in this domain.

**Why YOLOv12s is not recommended yet.** Its speed is attractive for edge devices, but the early-epoch training instability is a reliability risk for a high-stakes pipeline. It is a candidate for future edge deployment once stabilising tricks (warm-up, gradient clipping) are tuned.

## 3.2 Total Committed vs Completed User Stories

**Table 3.3 – Total Committed vs Completed User Stories**

| Sprint | Committed | Completed | Completion Rate |
|---|---|---|---|
| Sprint 1 | 4 | 4 | 100 % |
| Sprint 2 | 6 | 6 | 100 % |
| **Total** | **10** | **10** | **100 %** |

*Justification for any incomplete stories:* None — all committed user stories were completed on time. Stretch items identified during retrospectives (per-class recall dashboard, Jetson edge deployment, active-learning loop for hard negatives) were intentionally deferred to post-release as they were **not** in the committed backlog. This deferral is documented in Chapter 4 as future enhancement.

---

# CHAPTER 4
# CONCLUSIONS AND FUTURE ENHANCEMENT

## 4.1 Conclusions

This project presented **SmartFlow**, an end-to-end damaged-parcel detection system for logistics quality control, and a comprehensive comparative study of three modern YOLO variants on a custom 10 000-image package-defect dataset.

Key conclusions:

1. **YOLOv8m is the most reliable choice for package defect detection**, delivering the highest F1-score (0.759), the highest mAP50-95 (0.403), and the lowest coefficient of variation in validation mAP50-95 (0.020).
2. **F1-score, not just mAP, must guide model selection** in logistics quality control. YOLOv11m achieved near-identical mAP50-95 to YOLOv8m but with precision-heavy, recall-poor behaviour that would let defective parcels through.
3. **Training stability matters as much as peak accuracy.** YOLOv12s was 57 % faster to train but the early instability and lower final accuracy make it an unreliable production choice without additional stabilisation work.
4. **The Streamlit deployment** turns the research result into a usable product: a non-technical operator can upload a parcel photograph and receive annotated defect boxes with confidences in seconds.
5. **SmartFlow is deployable at every handoff** in the logistics pipeline—warehouse dispatch, loading, transit checkpoints, and final delivery—providing a consistent, 24×7 quality gate.

## 4.2 Future Enhancement

1. **Dataset generalisation.** Validate on additional defect types, packaging materials (cardboard, plastic, padded envelopes) and real-world lighting to confirm that the conclusions transfer beyond the current proprietary dataset.
2. **Per-model hyper-parameter tuning.** The present comparison used identical hyper-parameters for fairness; each model may improve further with dedicated tuning.
3. **Ensemble detection.** Combining YOLOv8m's balanced detections with YOLOv11m's high-precision outputs via weighted-box fusion could push both precision and recall higher.
4. **Edge deployment.** Port the detector to NVIDIA Jetson Orin / Xavier with TensorRT INT8 quantisation for deployment directly on conveyor-belt cameras.
5. **Broader SmartFlow platform.** Integrate defect detection with demand forecasting and route optimisation—recasting it as one module in a holistic smart-logistics platform that links quality events back to supply-chain decisions.
6. **Active learning loop.** Use low-confidence predictions in production as candidates for re-annotation, continuously improving the model on the long tail of hard cases.
7. **Explainability.** Add Grad-CAM / EigenCAM overlays so operators can see *why* a defect was flagged, building trust in the system.

---

# REFERENCES

[1] J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 779–788.

[2] G. Jocher, A. Chaurasia, and J. Qiu, "YOLOv8 by Ultralytics," 2023. [Online]. Available: https://github.com/ultralytics/ultralytics

[3] Ultralytics, "YOLOv11," 2024. [Online]. Available: https://docs.ultralytics.com/models/yolo11/

[4] Y. Li *et al.*, "YOLOv12: Attention-Centric Real-Time Object Detectors," 2025. [Online]. Available: https://arxiv.org/abs/2502.12524

[5] J. Redmon and A. Farhadi, "YOLO9000: Better, Faster, Stronger," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2017.

[6] J. Redmon and A. Farhadi, "YOLOv3: An Incremental Improvement," *arXiv preprint* arXiv:1804.02767, 2018.

[7] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, "YOLOv4: Optimal Speed and Accuracy of Object Detection," *arXiv preprint* arXiv:2004.10934, 2020.

[8] G. Jocher *et al.*, "YOLOv5," 2020. [Online]. Available: https://github.com/ultralytics/yolov5

[9] Y. He, K. Song, Q. Meng, and Y. Yan, "An End-to-end Steel Surface Defect Detection Approach via Fusing Multiple Hierarchical Features," *IEEE Trans. Instrum. Meas.*, vol. 69, no. 4, pp. 1493–1504, 2020.

[10] J. Li, X. Liang, and Y. Wei, "Fabric Defect Detection Based on Improved YOLOv3," in *Proc. IEEE Int. Conf. Signal Process. (ICSP)*, 2020, pp. 1–5.

[11] Z. Chen, D. Yang, and T. Zhang, "Deep Learning Based Defect Detection for Electronic Components," *IEEE Access*, vol. 8, pp. 124567–124576, 2020.

[12] Ultralytics, "YOLO Performance on COCO," 2024. [Online]. Available: https://docs.ultralytics.com/models/benchmarks

---

# APPENDIX

## A. Patent Disclosure Form / Publication Details

**Publication (Under Review / Submitted):**
I. Singh, N. K. Mohanarajan, K. Priyadharshini, and B. Sowmiya, *"SmartFlow: Automated Defect Detection System using YOLOv8"*, Department of Computing Technologies, SRM Institute of Science and Technology, Kattankulathur, 2026.

*(Attach: copy of manuscript `minor_paper_2.pdf`, acknowledgement / acceptance e-mail, and patent disclosure form if filed.)*

## B. Sample Coding with Screenshots

### B.1 Streamlit App (`streamlit_app.py`, abridged)

```python
import streamlit as st
from PIL import Image
from ultralytics import YOLO

WEIGHTS = "results/yolov8m_optimized_20260224_1855/weights/best.pt"

@st.cache_resource
def load_model():
    return YOLO(WEIGHTS)

def main():
    st.title("SmartFlow – Damaged Parcel Detection (YOLOv8m)")
    model = load_model()

    uploaded = st.file_uploader("Upload parcel image", type=["jpg", "jpeg", "png"])
    conf = st.slider("Confidence threshold", 0.1, 0.9, 0.25, 0.05)

    if uploaded is not None:
        image = Image.open(uploaded).convert("RGB")
        results = model.predict(image, conf=conf, verbose=False)
        annotated = results[0].plot()
        st.image(annotated, caption="Detections", use_column_width=True)

        rows = []
        for b in results[0].boxes:
            cls = int(b.cls[0]); conf_v = float(b.conf[0])
            x1, y1, x2, y2 = map(float, b.xyxy[0])
            rows.append({"class": model.names[cls], "confidence": conf_v,
                         "x1": x1, "y1": y1, "x2": x2, "y2": y2})
        if rows:
            st.dataframe(rows)
        else:
            st.info("No detections above threshold.")

if __name__ == "__main__":
    main()
```

### B.2 Training Command (YOLOv8m baseline)

```bash
yolo detect train \
     model=yolov8m.pt \
     data=dataset/data.yaml \
     epochs=150 imgsz=640 batch=16 \
     optimizer=SGD lr0=0.01 lrf=0.0001 \
     momentum=0.937 weight_decay=0.0005 \
     project=results name=yolov8m_optimized_20260224_1855
```

### B.3 Research Metrics Aggregation (`scripts/06_research_metrics.py`, abridged)

```python
import pandas as pd, matplotlib.pyplot as plt

runs = {
    "YOLOv8m":  "results/yolov8m_optimized_20260224_1855/results.csv",
    "YOLOv11m": "results/yolov11m_optimized/results.csv",
    "YOLOv12s": "results/yolov12s_optimized/results.csv",
}

for metric in ["metrics/mAP50-95(B)", "metrics/precision(B)",
               "metrics/recall(B)"]:
    plt.figure()
    for name, csv in runs.items():
        df = pd.read_csv(csv)
        plt.plot(df["epoch"], df[metric], label=name)
    plt.xlabel("Epoch"); plt.ylabel(metric); plt.legend()
    plt.savefig(f"research_output/{metric.replace('/', '_')}.png", dpi=200)
```

**Screenshots to attach:**
- Figure B.1 – Streamlit home page (empty state).
- Figure B.2 – Upload + annotated parcel with bounding boxes.
- Figure B.3 – Confidence slider effect (0.25 vs 0.75).
- Figure B.4 – Training curve screenshot from Ultralytics `results.png`.

## C. Plagiarism Report

*(Attach the Turnitin / Drillbit plagiarism-check PDF summary here.)*
Similarity Index: ___ %
Internet Sources: ___ %
Publications: ___ %
Student Papers: ___ %

---

*End of Report.*
