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
    # Lowered for better real-world detection
    if lighting < 0.4:
        return 0.55
    elif lighting < 0.7:
        return 0.50
    else:
        return 0.45
    
    def detect_objects(self, frame):

        self.frame_count += 1

        lighting = self.get_lighting_metric(frame)
        blur = self.get_blur_metric(frame)

        dynamic_conf = self.get_dynamic_confidence(lighting)

         # stricter if blurry
        if blur < 100:
          dynamic_conf += 0.02
    
        results = self.model(
    frame,
    conf=max(dynamic_conf, 0.40),  # never go below 0.40
    iou=0.5
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