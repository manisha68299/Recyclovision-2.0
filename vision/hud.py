"""
RecycloVision - HUD Module
Draws overlay information on live video feed.
"""

import cv2
from logic.rules import WasteSegregationRules


def draw_hud(frame, detections, purity_score, carbon_saved):

    # Draw detection boxes
    for det in detections:

        label = det["label"]
        confidence = det["confidence"]
        coords = det["coords"]

        x1, y1, x2, y2 = map(int, coords)

        # Get category color
        color = WasteSegregationRules.get_category_color(label)

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Label text
        text = f"{label} ({confidence:.2f})"
        cv2.putText(
            frame,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    # Draw System Stats
    cv2.putText(
        frame,
        f"Purity: {purity_score:.2f}%",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        f"CO2 Saved: {carbon_saved:.2f} kg",
        (20, 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 255),
        2
    )

    return frame