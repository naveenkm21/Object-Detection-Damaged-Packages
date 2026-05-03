"""
SCM Parcel Damage Inspection Dashboard
Powered by YOLOv8m (fine-tuned for hole / wet damage detection).
Built for supply chain quality-control demos.
"""
from __future__ import annotations

import io
import os
import time
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st
import torch
from PIL import Image, ImageOps
from ultralytics import YOLO

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
MODEL_PATH = ROOT / "results/yolov8m_optimized_20260224_1855/weights/best.pt"
MODEL_URL = os.environ.get(
    "MODEL_URL",
    "https://github.com/naveenkm21/Object-Detection-Damaged-Packages/releases/download/v1.0-weights/best.pt",
)
RESEARCH_DIR = ROOT / "research_output"
SAMPLE_DIR = ROOT / "dataset/test/images"
MAX_IMAGE_EDGE = int(os.environ.get("MAX_IMAGE_EDGE", "1600"))

CLASS_COLORS = {"hole": "#E64A4A", "wet": "#3E8AE6"}
CLASS_ICONS = {"hole": "🕳️", "wet": "💧"}

st.set_page_config(
    page_title="SCM Parcel Damage Inspection",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
:root {
    --brand: #0F4C81;
    --brand-2: #1F8FFF;
    --accent: #FFB020;
    --bg-soft: #F4F7FB;
    --danger: #E64A4A;
    --ok: #2BAE66;
}
.main .block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1400px; }
.app-header {
    background: linear-gradient(120deg, #0F4C81 0%, #1F8FFF 100%);
    padding: 1.4rem 1.8rem; border-radius: 14px; color: white; margin-bottom: 1.2rem;
    box-shadow: 0 6px 20px rgba(15, 76, 129, 0.18);
}
.app-header h1 { color: white; margin: 0; font-size: 1.7rem; letter-spacing: 0.3px; }
.app-header p  { color: #E6F0FF; margin: 0.25rem 0 0 0; font-size: 0.95rem; }
.kpi-card {
    background: white; padding: 1rem 1.1rem; border-radius: 12px;
    border: 1px solid #E6ECF3; box-shadow: 0 2px 8px rgba(15,76,129,0.05);
    height: 100%;
}
.kpi-label { color: #6B7A8F; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.7px; }
.kpi-value { color: #0F4C81; font-size: 1.7rem; font-weight: 700; margin: 0.25rem 0 0 0; }
.kpi-sub   { color: #8A98AC; font-size: 0.78rem; }
.status-pill {
    display: inline-block; padding: 0.3rem 0.8rem; border-radius: 999px;
    font-size: 0.82rem; font-weight: 600;
}
.status-ok    { background: #E4F7EC; color: #1F7A47; }
.status-warn  { background: #FFF3D6; color: #9A6B00; }
.status-bad   { background: #FCE4E4; color: #B02828; }
.section-title {
    font-size: 1.05rem; font-weight: 700; color: #0F4C81;
    margin: 0.4rem 0 0.6rem 0; border-left: 4px solid #1F8FFF; padding-left: 0.6rem;
}
.footer-note { color:#8A98AC; font-size:0.8rem; text-align:center; margin-top:2rem; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #F4F7FB; border-radius: 8px 8px 0 0; padding: 0.4rem 1rem;
}
.stTabs [aria-selected="true"] { background: #0F4C81 !important; color: white !important; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------
def ensure_model(model_path: Path, url: str) -> Path:
    if model_path.exists():
        return model_path
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with st.spinner(f"Downloading model weights ({url.rsplit('/', 1)[-1]})..."):
        tmp_path = model_path.with_suffix(model_path.suffix + ".part")
        urllib.request.urlretrieve(url, tmp_path)
        tmp_path.replace(model_path)
    return model_path


@st.cache_resource(show_spinner="Loading YOLOv8m model...")
def load_model(model_path: Path) -> YOLO:
    return YOLO(str(model_path))


@st.cache_data(show_spinner=False)
def load_research_metrics():
    metrics_csv = sorted(RESEARCH_DIR.glob("per_class_metrics_*.csv"))
    threshold_csv = sorted(RESEARCH_DIR.glob("threshold_results_*.csv"))
    confusion_png = sorted(RESEARCH_DIR.glob("confusion_matrix_*.png"))
    threshold_png = sorted(RESEARCH_DIR.glob("threshold_analysis_*.png"))
    per_class_png = sorted(RESEARCH_DIR.glob("per_class_metrics_*.png"))
    out = {}
    if metrics_csv:
        out["per_class"] = pd.read_csv(metrics_csv[-1])
    if threshold_csv:
        out["threshold"] = pd.read_csv(threshold_csv[-1])
    out["confusion_png"] = confusion_png[-1] if confusion_png else None
    out["threshold_png"] = threshold_png[-1] if threshold_png else None
    out["per_class_png"] = per_class_png[-1] if per_class_png else None
    return out


# ---------------------------------------------------------------------------
# Inference helpers
# ---------------------------------------------------------------------------
def prepare_image_for_inference(image: Image.Image) -> np.ndarray:
    image_rgb = ImageOps.exif_transpose(image).convert("RGB")
    if MAX_IMAGE_EDGE > 0 and max(image_rgb.size) > MAX_IMAGE_EDGE:
        # Resize overly large inputs to prevent memory errors during conversion.
        image_rgb.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE), Image.LANCZOS)
    try:
        return np.array(image_rgb)
    except MemoryError:
        fallback_edge = 1024 if MAX_IMAGE_EDGE <= 0 else min(1024, max(320, MAX_IMAGE_EDGE // 2))
        if max(image_rgb.size) > fallback_edge:
            image_rgb.thumbnail((fallback_edge, fallback_edge), Image.LANCZOS)
            return np.array(image_rgb)
        raise


def run_inference(model: YOLO, image: Image.Image, conf: float, iou: float):
    try:
        image_np = prepare_image_for_inference(image)
    except MemoryError:
        st.error("Image too large to process. Please upload a smaller resolution image.")
        st.stop()

    t0 = time.perf_counter()
    use_cpu = st.session_state.get("force_cpu", False)
    predict_kwargs = {"source": image_np, "conf": conf, "iou": iou, "verbose": False}
    if use_cpu:
        predict_kwargs["device"] = "cpu"
    try:
        results = model.predict(**predict_kwargs)
    except RuntimeError as exc:
        if "cuda" in str(exc).lower():
            st.session_state["force_cpu"] = True
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            predict_kwargs["device"] = "cpu"
            results = model.predict(**predict_kwargs)
            if not st.session_state.get("warned_cpu_fallback", False):
                st.warning("CUDA error detected. Falling back to CPU inference for this session.")
                st.session_state["warned_cpu_fallback"] = True
        else:
            raise
    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    result = results[0]
    annotated_bgr = result.plot()
    annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

    rows = []
    if result.boxes is not None and len(result.boxes) > 0:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            xyxy = box.xyxy[0].tolist()
            rows.append(
                {
                    "class": model.names.get(cls_id, str(cls_id)),
                    "confidence": float(box.conf[0]),
                    "x1": int(xyxy[0]),
                    "y1": int(xyxy[1]),
                    "x2": int(xyxy[2]),
                    "y2": int(xyxy[3]),
                    "area_px": int((xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])),
                }
            )
    return annotated_rgb, pd.DataFrame(rows), elapsed_ms, image_np


def compute_severity(detections: pd.DataFrame, image_shape) -> dict:
    """Translate raw detections into an SCM-friendly verdict."""
    h, w = image_shape[:2]
    img_area = max(h * w, 1)
    if detections.empty:
        return {
            "verdict": "PASS",
            "level": "ok",
            "score": 0.0,
            "action": "Forward to next checkpoint. No visible damage.",
            "n_hole": 0, "n_wet": 0,
            "damage_pct": 0.0,
        }
    n_hole = int((detections["class"] == "hole").sum())
    n_wet = int((detections["class"] == "wet").sum())
    damage_pct = 100.0 * detections["area_px"].sum() / img_area
    avg_conf = float(detections["confidence"].mean())
    score = min(100.0, damage_pct * 4 + (n_hole * 12) + (n_wet * 8) + avg_conf * 25)

    if score >= 55 or n_hole >= 2 or damage_pct > 6:
        verdict, level = "REJECT", "bad"
        action = "Quarantine parcel. File carrier claim. Do not dispatch."
    elif score >= 25 or n_hole >= 1 or n_wet >= 1:
        verdict, level = "REVIEW", "warn"
        action = "Manual inspection required. Photograph & log before re-pack."
    else:
        verdict, level = "PASS", "ok"
        action = "Forward to next checkpoint."

    return {
        "verdict": verdict, "level": level, "score": round(score, 1),
        "action": action, "n_hole": n_hole, "n_wet": n_wet,
        "damage_pct": round(damage_pct, 2),
    }


def kpi_card(col, label: str, value: str, sub: str = ""):
    col.markdown(
        f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div></div>""",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def sidebar_controls():
    with st.sidebar:
        st.markdown("### 📦 SCM Inspection")
        st.caption("YOLOv8m · Damage detection")
        st.divider()
        page = st.radio(
            "Navigate",
            ["🏠 Live Inspection", "🗂️ Batch Processing", "📊 Model Performance", "ℹ️ About"],
            label_visibility="collapsed",
        )
        st.divider()
        st.markdown("**Detection settings**")
        conf = st.slider("Confidence threshold", 0.05, 0.95, 0.25, 0.05)
        iou = st.slider("IoU threshold (NMS)", 0.20, 0.90, 0.45, 0.05)
        st.divider()
        st.markdown("**Model**")
        if MODEL_PATH.exists():
            size_mb = MODEL_PATH.stat().st_size / (1024 * 1024)
            st.success(f"✅ best.pt loaded\n\n`{size_mb:.1f} MB`")
        else:
            st.error("❌ Model not found")
        st.caption(f"`{MODEL_PATH.relative_to(ROOT).as_posix()}`")
    return page, conf, iou


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_live(model: YOLO, conf: float, iou: float):
    st.markdown(
        """<div class="app-header">
            <h1>📦 Parcel Damage Inspection — Live</h1>
            <p>Real-time vision QA for inbound / outbound logistics checkpoints.</p>
        </div>""",
        unsafe_allow_html=True,
    )

    tab_upload, tab_sample = st.tabs(["📤 Upload image", "🖼️ Sample gallery"])

    image: Image.Image | None = None
    image_label = ""
    with tab_upload:
        uploaded = st.file_uploader(
            "Drop a parcel image (jpg / jpeg / png)",
            type=["jpg", "jpeg", "png"],
        )
        if uploaded is not None:
            image = Image.open(uploaded)
            image_label = uploaded.name

    with tab_sample:
        if SAMPLE_DIR.exists():
            samples = sorted(SAMPLE_DIR.glob("*.jpg"))[:12]
            if samples:
                cols = st.columns(6)
                for idx, path in enumerate(samples):
                    with cols[idx % 6]:
                        st.image(str(path), use_container_width=True)
                        if st.button("Use", key=f"sample_{idx}"):
                            image = Image.open(path)
                            image_label = path.name
            else:
                st.info("No sample images available.")
        else:
            st.info("Sample directory not found.")

    if image is None:
        st.info("📥 Upload an image or pick from the sample gallery to start inspection.")
        return

    annotated, dets, elapsed_ms, image_np = run_inference(model, image, conf, iou)
    severity = compute_severity(dets, image_np.shape)

    # KPI row
    cols = st.columns(5)
    pill_class = {"ok": "status-ok", "warn": "status-warn", "bad": "status-bad"}[severity["level"]]
    cols[0].markdown(
        f"""<div class="kpi-card">
            <div class="kpi-label">Verdict</div>
            <div style="margin-top:0.4rem"><span class="status-pill {pill_class}">{severity["verdict"]}</span></div>
            <div class="kpi-sub" style="margin-top:0.5rem">Damage score: {severity["score"]}/100</div>
        </div>""",
        unsafe_allow_html=True,
    )
    kpi_card(cols[1], "Detections", str(len(dets)), f"{severity['damage_pct']}% of frame")
    kpi_card(cols[2], "🕳️ Holes", str(severity["n_hole"]))
    kpi_card(cols[3], "💧 Wet spots", str(severity["n_wet"]))
    kpi_card(cols[4], "Inference", f"{elapsed_ms:.0f} ms", f"{1000/max(elapsed_ms,1):.1f} FPS")

    st.markdown(" ")
    st.markdown(f'<div class="section-title">Recommended action</div>', unsafe_allow_html=True)
    severity_box = {
        "ok": st.success, "warn": st.warning, "bad": st.error,
    }[severity["level"]]
    severity_box(f"**{severity['verdict']}** — {severity['action']}")

    st.markdown(f'<div class="section-title">Inspection view {("· " + image_label) if image_label else ""}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Original**")
        st.image(image_np, use_container_width=True)
    with c2:
        st.markdown("**Annotated detections**")
        st.image(annotated, use_container_width=True)

    st.markdown('<div class="section-title">Detection details</div>', unsafe_allow_html=True)
    if dets.empty:
        st.success("✅ No damage detected at this confidence threshold.")
    else:
        display = dets.copy()
        display["class"] = display["class"].apply(lambda c: f"{CLASS_ICONS.get(c,'')} {c}")
        st.dataframe(
            display.style.format({"confidence": "{:.3f}"}).background_gradient(
                subset=["confidence"], cmap="Blues"
            ),
            use_container_width=True, hide_index=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            counts = dets["class"].value_counts().rename_axis("class").reset_index(name="count")
            st.bar_chart(counts.set_index("class"))
        with c2:
            st.markdown("**Confidence distribution**")
            st.bar_chart(dets[["confidence"]].reset_index(drop=True))

        # Download report row
        buf = io.BytesIO()
        Image.fromarray(annotated).save(buf, format="PNG")
        st.download_button(
            "⬇️ Download annotated image",
            data=buf.getvalue(),
            file_name=f"inspection_{datetime.now():%Y%m%d_%H%M%S}.png",
            mime="image/png",
        )
        st.download_button(
            "⬇️ Download detections (CSV)",
            data=dets.to_csv(index=False).encode("utf-8"),
            file_name=f"detections_{datetime.now():%Y%m%d_%H%M%S}.csv",
            mime="text/csv",
        )


def page_batch(model: YOLO, conf: float, iou: float):
    st.markdown(
        """<div class="app-header">
            <h1>🗂️ Batch Inspection</h1>
            <p>Process a shipment of images at once — built for shift-end QA review.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    files = st.file_uploader(
        "Upload multiple parcel images",
        type=["jpg", "jpeg", "png"], accept_multiple_files=True,
    )
    if not files:
        st.info("Upload one or more images to run a batch inspection.")
        return

    progress = st.progress(0.0, text="Starting batch...")
    rows = []
    annotated_imgs: dict[str, np.ndarray] = {}
    for i, f in enumerate(files, start=1):
        img = Image.open(f)
        annotated, dets, elapsed_ms, image_np = run_inference(model, img, conf, iou)
        sev = compute_severity(dets, image_np.shape)
        annotated_imgs[f.name] = annotated
        rows.append({
            "file": f.name, "verdict": sev["verdict"], "score": sev["score"],
            "holes": sev["n_hole"], "wet": sev["n_wet"],
            "detections": len(dets), "damage_pct": sev["damage_pct"],
            "ms": round(elapsed_ms, 1),
        })
        progress.progress(i / len(files), text=f"Processed {i}/{len(files)} — {f.name}")
    progress.empty()

    df = pd.DataFrame(rows)

    # KPIs
    pass_n = (df["verdict"] == "PASS").sum()
    review_n = (df["verdict"] == "REVIEW").sum()
    reject_n = (df["verdict"] == "REJECT").sum()
    cols = st.columns(5)
    kpi_card(cols[0], "Total parcels", str(len(df)))
    kpi_card(cols[1], "✅ Pass", str(pass_n), f"{pass_n/len(df)*100:.0f}%")
    kpi_card(cols[2], "⚠️ Review", str(review_n), f"{review_n/len(df)*100:.0f}%")
    kpi_card(cols[3], "🚫 Reject", str(reject_n), f"{reject_n/len(df)*100:.0f}%")
    kpi_card(cols[4], "Avg latency", f"{df['ms'].mean():.0f} ms")

    st.markdown('<div class="section-title">Batch results</div>', unsafe_allow_html=True)
    def color_verdict(v):
        return {"PASS": "background-color:#E4F7EC;color:#1F7A47",
                "REVIEW": "background-color:#FFF3D6;color:#9A6B00",
                "REJECT": "background-color:#FCE4E4;color:#B02828"}.get(v, "")
    st.dataframe(
        df.style.applymap(color_verdict, subset=["verdict"])
                 .background_gradient(subset=["score"], cmap="Reds"),
        use_container_width=True, hide_index=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Verdict distribution**")
        st.bar_chart(df["verdict"].value_counts())
    with c2:
        st.markdown("**Damage score distribution**")
        st.bar_chart(df.set_index("file")["score"])

    # Build zip of annotated images
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, arr in annotated_imgs.items():
            img_buf = io.BytesIO()
            Image.fromarray(arr).save(img_buf, format="PNG")
            zf.writestr(f"annotated/{Path(name).stem}.png", img_buf.getvalue())
        zf.writestr("batch_report.csv", df.to_csv(index=False))

    st.download_button(
        "⬇️ Download batch report (.zip)",
        data=zip_buf.getvalue(),
        file_name=f"scm_batch_{datetime.now():%Y%m%d_%H%M%S}.zip",
        mime="application/zip",
    )


def page_performance():
    st.markdown(
        """<div class="app-header">
            <h1>📊 Model Performance</h1>
            <p>Validation metrics from the fine-tuned YOLOv8m run on the parcel-damage dataset.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    data = load_research_metrics()

    if "per_class" in data:
        pc = data["per_class"].copy()
        # Top KPIs
        cols = st.columns(4)
        kpi_card(cols[0], "Classes", str(int(pc["num_classes"].iloc[0])), "hole · wet")
        kpi_card(cols[1], "mAP@50 (mean)", f"{pc['ap50'].mean():.3f}")
        kpi_card(cols[2], "mAP@50-95 (mean)", f"{pc['map50-95'].mean():.3f}")
        kpi_card(cols[3], "F1 (mean)", f"{pc['f1'].mean():.3f}")

        st.markdown('<div class="section-title">Per-class metrics</div>', unsafe_allow_html=True)
        st.dataframe(
            pc.style.format({c: "{:.3f}" for c in ["precision","recall","f1","ap50","map50-95"]})
                    .background_gradient(subset=["f1","ap50","map50-95"], cmap="Blues"),
            use_container_width=True, hide_index=True,
        )
        chart_df = pc.set_index("class")[["precision","recall","f1","ap50","map50-95"]]
        st.bar_chart(chart_df)

    img_cols = st.columns(2)
    if data.get("confusion_png"):
        with img_cols[0]:
            st.markdown('<div class="section-title">Confusion matrix</div>', unsafe_allow_html=True)
            st.image(str(data["confusion_png"]), use_container_width=True)
    if data.get("per_class_png"):
        with img_cols[1]:
            st.markdown('<div class="section-title">Per-class chart</div>', unsafe_allow_html=True)
            st.image(str(data["per_class_png"]), use_container_width=True)
    if data.get("threshold_png"):
        st.markdown('<div class="section-title">Threshold sweep</div>', unsafe_allow_html=True)
        st.image(str(data["threshold_png"]), use_container_width=True)

    if "threshold" in data:
        st.markdown('<div class="section-title">Threshold table</div>', unsafe_allow_html=True)
        st.dataframe(data["threshold"], use_container_width=True, hide_index=True)


def page_about():
    st.markdown(
        """<div class="app-header">
            <h1>ℹ️ About this deployment</h1>
            <p>Damaged Parcel Detection for Supply Chain Management — final-year project demo.</p>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
### Why this matters in SCM
Damaged parcels cost logistics operators **1–3% of revenue annually** through claims,
re-shipments, and customer churn. Manual visual inspection at hubs is slow, inconsistent,
and rarely captured in a structured way. This system replaces it with an automated
computer-vision checkpoint that flags damage **in under a second per parcel**.

### How it fits the SCM pipeline
1. **Inbound dock** — verify carrier-handover condition before signing receipt.
2. **Sortation belt** — divert flagged parcels to a manual review lane.
3. **Outbound dispatch** — final QA gate before loading.
4. **Returns / claims** — auto-attach evidence images to the claim record.

### Stack
- **Model:** YOLOv8m fine-tuned on a 2-class dataset (`hole`, `wet`).
- **Training:** 150 epochs, AdamW, image size 640, batch 12, GPU.
- **Serving:** Ultralytics + Streamlit, single-file app, no external services.
- **Dataset:** Roboflow-formatted train / valid / test splits.

### Decision logic
The dashboard converts raw detections into an operations-friendly verdict:
- **PASS** — forward to next checkpoint.
- **REVIEW** — manual inspection lane.
- **REJECT** — quarantine + carrier claim.

Scoring blends detection count, class severity, and damaged frame area, so the
shopfloor team gets a single number — not a wall of bounding boxes.
        """
    )
    st.caption(f"Model file: `{MODEL_PATH.relative_to(ROOT).as_posix()}`  ·  "
               f"Built {datetime.now():%Y-%m-%d}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    page, conf, iou = sidebar_controls()

    try:
        ensure_model(MODEL_PATH, MODEL_URL)
    except Exception as exc:
        st.error(f"Could not download model weights from {MODEL_URL}\n\n{exc}")
        st.stop()
    if not MODEL_PATH.exists():
        st.error(f"Model not found at: {MODEL_PATH.as_posix()}")
        st.stop()

    model = load_model(MODEL_PATH)

    if page.startswith("🏠"):
        page_live(model, conf, iou)
    elif page.startswith("🗂️"):
        page_batch(model, conf, iou)
    elif page.startswith("📊"):
        page_performance()
    else:
        page_about()

    st.markdown(
        '<div class="footer-note">SCM Parcel Damage Inspection · YOLOv8m · '
        f'{datetime.now():%Y}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
