import cv2
import numpy as np
from datetime import datetime


class WasteDetector:

    def __init__(self, model, allowed_classes=None):
        self.model = model
        self.allowed_classes = allowed_classes
        self.frame_count = 0
        self.low_confidence_buffer = []

    def get_lighting_metric(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return np.mean(gray) / 255.0

    def get_blur_metric(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    def get_dynamic_confidence(self, lighting):
        if lighting < 0.4:
            return 0.80
        elif lighting < 0.7:
            return 0.70
        else:
            return 0.60

    def detect_objects(self, frame):

        self.frame_count += 1

        lighting = self.get_lighting_metric(frame)
        blur = self.get_blur_metric(frame)

        dynamic_conf = self.get_dynamic_confidence(lighting)

        if blur < 100:
            dynamic_conf += 0.05  # stricter if blurry

        results = self.model(
            frame,
            conf=dynamic_conf,
            iou=0.5,
            classes=self.allowed_classes
        )

        detections = []

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
                    "lighting": lighting,
                    "blur": blur
                }

                detections.append(detection_data)

                if confidence < 0.75:
                    self.low_confidence_buffer.append(detection_data)

        return detections, self.low_confidence_buffer