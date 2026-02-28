"""
RecycloVision - HUD Module
Draws overlay information on live video feed.
"""

import cv2
from logic.rules import waste_system


def draw_hud(frame, detections, purity_score, carbon_saved,
             fps=0, latency=0, current_bin="RECYCLABLE"):

    height, width, _ = frame.shape

    # =============================
    # Draw Detection Boxes
    # =============================
    for det in detections:

        label = det["label"]
        confidence = det["confidence"]
        coords = det["coords"]

        x1, y1, x2, y2 = map(int, coords)

        # Get color from intelligent waste system
        color = waste_system.get_color(label)

        # Draw bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Draw label text
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

    # =============================
    # Draw Top Info Panel
    # =============================
    cv2.rectangle(frame, (0, 0), (width, 120), (0, 0, 0), -1)

    cv2.putText(
        frame,
        f"Active Bin: {current_bin}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Purity: {purity_score:.2f}%",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"CO2 Saved: {carbon_saved:.2f} kg",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # =============================
    # Performance Info (Right Side)
    # =============================
    cv2.putText(
        frame,
        f"FPS: {fps}",
        (width - 150, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Latency: {latency} ms",
        (width - 200, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    return frame