"""
RecycloVision - Camera Module
Handles camera initialization and frame capture.
"""

import cv2


def start_camera(camera_index=0):
    """
    Initialize webcam.
    Default camera_index=0 (laptop camera)
    """
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise Exception("❌ Could not open camera.")

    print("📷 Camera started successfully.")
    return cap


def read_frame(cap):
    """
    Read a frame from camera.
    """
    ret, frame = cap.read()

    if not ret:
        return False, None

    return True, frame


def release_camera(cap):
    """
    Release camera and destroy windows.
    """
    cap.release()
    cv2.destroyAllWindows()
    print("🛑 Camera released.")