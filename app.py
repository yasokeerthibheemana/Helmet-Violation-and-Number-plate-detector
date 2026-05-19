"""
app.py — Traffic Violation Detection · Helmet & Number Plate
Supports file upload, camera snapshot, and live webcam.
"""

import streamlit as st
import traceback
import tempfile
import os
import cv2
import numpy as np
from PIL import Image

from ui.theme import (
    inject_theme,
    section_card,
    violation_badge,
    plate_card,
    processing_indicator,
    empty_upload_state,
    no_plate_placeholder,
)

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Traffic Violation Detection",
    layout="centered",
    page_icon="🛵",
    initial_sidebar_state="collapsed",
)

inject_theme()

# ── Configuration ─────────────────────────────────────────────────────────────
YOLO_MODEL_PATH = r"C:\Users\Yaso keerthi\OneDrive\Desktop\helmet detection\runs\detect\train2\weights\best.pt"
CONF_THRESH = 0.35
CAMERA_INDEX = 0

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}


@st.cache_resource(show_spinner=False)
def load_model(path: str):
    from ultralytics import YOLO
    return YOLO(path)


try:
    model = load_model(YOLO_MODEL_PATH)
except Exception:
    st.error("⚠️ Could not load the YOLO model. Check the model path and dependencies.")
    with st.expander("Error details"):
        st.code(traceback.format_exc())
    st.stop()


def classify_upload(filename: str) -> str:
    ext = os.path.splitext(filename)[-1].lower()
    if ext in IMAGE_EXTS:
        return "image"
    if ext in VIDEO_EXTS:
        return "video"
    return "unsupported"


def run_image_inference(img_bgr: np.ndarray):
    results = model.predict(img_bgr, conf=CONF_THRESH, verbose=False)
    plotted = results[0].plot()
    violation = False
    plates = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            name = model.names[cls].lower()
            if "no" in name and "helmet" in name:
                violation = True
            if "plate" in name or "number" in name:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                crop = img_bgr[y1:y2, x1:x2]
                if crop.size > 0:
                    plates.append(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))

    return cv2.cvtColor(plotted, cv2.COLOR_BGR2RGB), violation, plates


def pil_to_bgr(pil_image: Image.Image) -> np.ndarray:
    rgb = np.array(pil_image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def show_image_results(plotted_rgb, violation, plate_crops, caption: str):
    col_plates, col_result = st.columns([1, 2], gap="large")

    with col_plates:
        section_card("Number Plate(s)", "🔢")
        if plate_crops:
            for i, crop in enumerate(plate_crops, 1):
                plate_card(crop, i)
        else:
            no_plate_placeholder()

    with col_result:
        section_card("Detection Output", "🔍")
        st.image(plotted_rgb, caption=caption, use_container_width=True)

    st.markdown("---")
    violation_badge(violation)


def process_and_show(img_bgr: np.ndarray, caption: str):
    with st.spinner("Running detection…"):
        plotted_rgb, violation, plate_crops = run_image_inference(img_bgr)
    show_image_results(plotted_rgb, violation, plate_crops, caption)


def open_webcam():
    if os.name == "nt":
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
        if cap.isOpened():
            return cap
    return cv2.VideoCapture(CAMERA_INDEX)


def run_video_file(uploaded_file):
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    tfile.flush()

    cap = cv2.VideoCapture(tfile.name)
    if not cap.isOpened():
        st.error("Unable to open the video file. Please try a different format.")
        os.remove(tfile.name)
        return

    section_card("Live Frame Analysis", "🎞️")
    processing_indicator()

    frame_placeholder = st.empty()
    progress_bar = st.progress(0)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
    frame_count = 0
    violation_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        plotted_rgb, violation, _ = run_image_inference(frame)
        if violation:
            violation_detected = True

        frame_placeholder.image(
            plotted_rgb,
            caption=f"Frame {frame_count} / {total_frames}",
            use_container_width=True,
        )
        progress_bar.progress(min(frame_count / total_frames, 1.0))

    cap.release()
    progress_bar.empty()
    st.markdown("---")
    violation_badge(violation_detected)

    try:
        os.remove(tfile.name)
    except OSError:
        pass


def run_upload_tab():
    uploaded_file = st.file_uploader(
        "Drop an image or video — JPG · PNG · MP4 · AVI · MOV",
        type=["jpg", "jpeg", "png", "bmp", "webp", "mp4", "avi", "mov", "mkv", "wmv"],
        label_visibility="collapsed",
        key="file_upload",
    )

    if not uploaded_file:
        empty_upload_state()
        return

    media_type = classify_upload(uploaded_file.name)
    if media_type == "unsupported":
        st.error(
            f"Unsupported file type: **{os.path.splitext(uploaded_file.name)[-1]}**. "
            "Please upload a JPG, PNG, MP4, AVI, or MOV file."
        )
        return

    if media_type == "image":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.read())
            img_path = tmp.name

        img_bgr = cv2.imread(img_path)
        try:
            os.remove(img_path)
        except OSError:
            pass

        if img_bgr is None:
            st.error("Unable to decode the image. Please try a different file.")
            return

        process_and_show(img_bgr, "YOLO · Annotated Frame")
    else:
        run_video_file(uploaded_file)


def run_camera_snapshot_tab():
    st.caption("Allow camera access in your browser, then tap the shutter to capture a frame.")
    camera_photo = st.camera_input(
        "Take a photo",
        label_visibility="collapsed",
        key="camera_snapshot",
    )

    if camera_photo is None:
        st.info("📷 Waiting for a camera capture — use the button above to take a photo.")
        return

    image = Image.open(camera_photo)
    img_bgr = pil_to_bgr(image)
    process_and_show(img_bgr, "YOLO · Camera capture")


def _live_camera_frame():
    if not st.session_state.get("live_camera_on"):
        return

    cap = st.session_state.get("live_cap")
    if cap is None or not cap.isOpened():
        cap = open_webcam()
        st.session_state.live_cap = cap

    if not cap.isOpened():
        st.error("Could not open webcam. Close other apps using the camera and try again.")
        st.session_state.live_camera_on = False
        return

    ret, frame = cap.read()
    if not ret:
        st.warning("Failed to read from camera.")
        return

    plotted_rgb, violation, _ = run_image_inference(frame)
    if violation:
        st.session_state.live_violation = True

    st.image(plotted_rgb, caption="Live · Webcam", use_container_width=True)


def _stop_live_camera():
    cap = st.session_state.get("live_cap")
    if cap is not None:
        cap.release()
    st.session_state.live_cap = None
    st.session_state.live_camera_on = False


def run_live_camera_tab():
    if "live_camera_on" not in st.session_state:
        st.session_state.live_camera_on = False
    if "live_cap" not in st.session_state:
        st.session_state.live_cap = None
    if "live_violation" not in st.session_state:
        st.session_state.live_violation = False

    st.caption("Real-time detection from your default webcam (may use more CPU).")

    col_start, col_stop = st.columns(2)
    with col_start:
        if st.button("▶ Start live camera", use_container_width=True, type="primary"):
            st.session_state.live_camera_on = True
            st.session_state.live_violation = False
            st.rerun()
    with col_stop:
        if st.button("⏹ Stop", use_container_width=True):
            _stop_live_camera()
            st.rerun()

    if not st.session_state.live_camera_on:
        st.info("Press **Start live camera** to begin. Press **Stop** when finished.")
        return

    section_card("Live Webcam", "📹")
    processing_indicator()

    fragment = getattr(st, "fragment", None)
    if fragment is not None:
        @fragment(run_every=0.2)
        def _live_loop():
            _live_camera_frame()

        _live_loop()
    else:
        _live_camera_frame()
        st.caption("Upgrade Streamlit (`pip install -U streamlit`) for smoother live video.")

    if st.session_state.live_violation:
        st.markdown("---")
        violation_badge(True)


# ═════════════════════════════════════════════════════════════════════════════
#  Input mode tabs
# ═════════════════════════════════════════════════════════════════════════════
section_card("Input Source", "📥")
tab_upload, tab_camera, tab_live = st.tabs(["📁 Upload file", "📷 Camera photo", "🎥 Live webcam"])

with tab_upload:
    run_upload_tab()

with tab_camera:
    run_camera_snapshot_tab()

with tab_live:
    run_live_camera_tab()
