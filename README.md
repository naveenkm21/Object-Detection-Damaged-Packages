# Damaged Parcel Detection — SCM Inspection Dashboard

A YOLOv8m-powered computer-vision dashboard that automates parcel damage QA
for supply-chain checkpoints (inbound dock, sortation, outbound dispatch).

**Model:** `results/yolov8m_optimized_20260224_1855/weights/best.pt`
**Classes:** `hole`, `wet`

---

## Quick start (Windows)

Double-click `run_app.bat` — it activates the local `venv/`, starts Streamlit,
and opens at <http://localhost:8501>.

## Quick start (any OS)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Docker

```bash
docker build -t scm-parcel-inspection .
docker run -p 8501:8501 scm-parcel-inspection
```

---

## Dashboard pages

1. **🏠 Live Inspection** — upload or pick a sample image, get a verdict
   (PASS / REVIEW / REJECT), damage score, latency, and annotated view.

<img width="1087" height="670" alt="image" src="https://github.com/user-attachments/assets/4cd533fe-c00e-45f9-8b5a-64e1031bcedf" />

2. **🗂️ Batch Processing** — drop an entire shipment of images, get a
   verdict table and a downloadable ZIP report (annotated PNGs + CSV).

<img width="1098" height="672" alt="image" src="https://github.com/user-attachments/assets/6eed301b-eb5e-456c-9592-afe92bbbebcf" />
   
4. **📊 Model Performance** — per-class metrics, confusion matrix, and
   threshold sweeps from the validation run.

<img width="1131" height="674" alt="image" src="https://github.com/user-attachments/assets/2e86371b-7b9c-4290-8246-d217d2070726" />

6. **ℹ️ About** — SCM context, pipeline placement, and decision logic.

<img width="1129" height="614" alt="image" src="https://github.com/user-attachments/assets/0e031e37-613d-4783-ba69-74f82915e287" />


## SCM decision logic

Raw detections are converted into an operations-friendly verdict by combining
detection count, class severity (holes weight higher than wet), and damaged
frame area:

| Verdict   | Action                                                  |
| --------- | ------------------------------------------------------- |
| ✅ PASS    | Forward to next checkpoint                              |
| ⚠️ REVIEW | Manual inspection lane; photograph & log before re-pack |
| 🚫 REJECT | Quarantine; file carrier claim; do not dispatch         |

## Project layout

```
streamlit_app.py        # Multi-page Streamlit dashboard
.streamlit/config.toml  # Brand theme
run_app.bat             # Windows one-click launcher
Dockerfile              # Container deployment
requirements.txt        # Pinned dependencies
results/yolov8m_*/      # Training output + best.pt
research_output/        # Validation metrics consumed by the dashboard
dataset/                # Roboflow-format train / valid / test
```
