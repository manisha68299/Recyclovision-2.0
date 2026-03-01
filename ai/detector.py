import cv2
import numpy as np
from datetime import datetime


class WasteDetector:

    def __init__(self, model, allowed_classes=None):
        self.model = model
        self.allowed_classes = allowed_classes
        self.frame_count = 0
        self.low_confidence_buffer = []

    # --------------------------------------------------
    # Main Detection Function (Stable Version)
    # --------------------------------------------------
    def detect_objects(self, frame):

        self.frame_count += 1

        # Fixed confidence threshold (stable & reliable)
        results = self.model(
            frame,
            conf=0.25,   # Safe baseline threshold
            iou=0.5,
            classes=self.allowed_classes
        )

        detections = []
        self.low_confidence_buffer = []  # reset every frame

        for result in results:
            for box in result.boxes:

                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = self.model.names[class_id]

                coords = box.xyxy[0].cpu().numpy()

                detection_data = {
                    "label": label.upper(),
                    "confidence": round(confidence, 2),
                    "coords": coords,
                    "timestamp": datetime.now(),
                    "lighting": 0,   # kept for compatibility
                    "blur": 0        # kept for compatibility
                }

                detections.append(detection_data)

                # Log low confidence separately
                if confidence < 0.75:
                    self.low_confidence_buffer.append(detection_data)

        return detections, self.low_confidence_buffer