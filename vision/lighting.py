"""
RecycloVision - Lighting & Frame Quality Module
Handles brightness and blur detection.
"""

import cv2
import numpy as np


def get_lighting_metric(frame):
    """
    Calculate brightness of frame.
    Returns normalized brightness between 0 and 1.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray) / 255.0
    return round(brightness, 3)


def get_blur_metric(frame):
    """
    Calculate blur score using Laplacian variance.
    Lower value = blurry image.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return round(blur_score, 2)


def get_frame_quality(frame):
    """
    Return combined lighting + blur info.
    """
    return {
        "lighting": get_lighting_metric(frame),
        "blur": get_blur_metric(frame)
    }