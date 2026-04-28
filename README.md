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
2. **🗂️ Batch Processing** — drop an entire shipment of images, get a
   verdict table and a downloadable ZIP report (annotated PNGs + CSV).
3. **📊 Model Performance** — per-class metrics, confusion matrix, and
   threshold sweeps from the validation run.
4. **ℹ️ About** — SCM context, pipeline placement, and decision logic.

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
