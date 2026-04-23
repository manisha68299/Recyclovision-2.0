import streamlit as st
import av
import cv2
import numpy as np

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

from ultralytics import YOLO

# === YOUR MODULES ===
from logic.tracker import waste_tracker
from logic.carbon import add_carbon_saving, get_total_carbon_saved
from logic.rules import waste_system
from database.db_manager import waste_db


# ================================
# PAGE CONFIG
# ================================
st.set_page_config(page_title="♻️ RecycloVision", layout="wide")

st.title("♻️ RecycloVision")
st.caption("AI-Powered Smart Waste Segregation System")


# ================================
# LOAD MODEL (SAFE)
# ================================
@st.cache_resource
def load_model():
    # Use lightweight model for cloud
    return YOLO("yolov8n.pt")

model = load_model()


# ================================
# WEBRTC CONFIG
# ================================
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


# ================================
# VIDEO TRANSFORMER
# ================================
class WasteDetector(VideoTransformerBase):

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        try:
            results = model(img, verbose=False)[0]

            for box in results.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # =====================
                # VALIDATION LOGIC
                # =====================
                is_correct = waste_system.validate(label)

                # Tracker update
                waste_tracker.log_detection(label, is_correct, conf)
                purity = waste_tracker.compute_purity_score()

                # Carbon update
                if is_correct:
                    add_carbon_saving(label)

                # DB log
                try:
                    waste_db.log_detection_result(
                        item_label=label,
                        is_correct=is_correct,
                        confidence=conf,
                        purity_score=purity
                    )
                except:
                    pass  # avoid crash in cloud

                # =====================
                # DRAW
                # =====================
                color = (0, 255, 0) if is_correct else (0, 0, 255)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    img,
                    f"{label} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2
                )

        except Exception:
            pass  # prevent full crash

        return img


# ================================
# START CAMERA
# ================================
st.subheader("🎥 Live Waste Detection")

webrtc_streamer(
    key="recyclovision",
    video_transformer_factory=WasteDetector,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
)


# ================================
# METRICS DASHBOARD
# ================================
st.subheader("📊 Live Metrics")

col1, col2 = st.columns(2)

col1.metric(
    "Purity Score",
    f"{waste_tracker.compute_purity_score()}%"
)

col2.metric(
    "CO₂ Saved",
    f"{get_total_carbon_saved()} kg"
)


# ================================
# SYSTEM STATUS
# ================================
st.subheader("🟢 System Status")

st.success("Webcam: Active (Browser)")
st.success("AI Model: Running (YOLOv8 Nano)")
st.success("Tracking: Active")


# ================================
# AUTO REFRESH
# ================================
import time
time.sleep(2)
st.rerun()