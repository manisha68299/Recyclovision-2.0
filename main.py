import cv2
import traceback
from ultralytics import YOLO

# === Project Imports ===
from ai.detector import WasteDetector
from vision.camera import start_camera, read_frame, release_camera
from vision.hud import draw_hud
from vision.lighting import get_frame_quality
from vision.performance import performance_monitor

from logic.tracker import waste_tracker
from logic.carbon import add_carbon_saving, get_total_carbon_saved
from logic.rules import waste_system   # ✅ UPDATED

from database.db_manager import waste_db


def main():

    print("🚀 Starting RecycloVision...")

    try:
        # =============================
        # 1️⃣ Load YOLO Model
        # =============================
        model = YOLO("runs/detect/train/weights/best.pt")
        allowed_classes = None

        # =============================
        # 2️⃣ Initialize AI Detector
        # =============================
        brain = WasteDetector(model, allowed_classes)

        # =============================
        # 3️⃣ Start Camera
        # =============================
        cap = start_camera()

        print("✅ System Initialized Successfully.")

        # =============================
        # 4️⃣ Main Loop
        # =============================
        while True:

            ret, frame = read_frame(cap)
            if not ret:
                print("❌ Failed to capture frame")
                break

            # ---------------------------------
            # Lighting & Quality Check
            # ---------------------------------
            frame_quality = get_frame_quality(frame)

            # ---------------------------------
            # AI Detection
            # ---------------------------------
            detections, low_conf = brain.detect_objects(frame)

            # ---------------------------------
            # Process Detections
            # ---------------------------------
            for det in detections:

                label = det["label"]
                confidence = det["confidence"]

                # ✅ Intelligent validation using label
                if waste_system.validate(label):
                    is_correct = True
                    status = "CORRECT"
                else:
                    is_correct = False
                    status = "CONTAMINATION_PREVENTED"

                # Update Tracker
                waste_tracker.log_detection(
                    item_label=label,
                    is_correct=is_correct,
                    confidence_score=confidence
                )

                purity = waste_tracker.compute_purity_score()

                # Carbon update
                if is_correct:
                    add_carbon_saving(label)

                # Log to database
                waste_db.log_detection_result(
                    item_label=label,
                    is_correct=is_correct,
                    confidence=confidence,
                    purity_score=purity
                )

            # ---------------------------------
            # FPS + Latency Calculation
            # ---------------------------------
            fps, latency_ms = performance_monitor.calculate()

            # ---------------------------------
            # Draw HUD
            # ---------------------------------
            frame = draw_hud(
                frame,
                detections,
                purity_score=waste_tracker.compute_purity_score(),
                carbon_saved=get_total_carbon_saved(),
                fps=fps,
                latency=latency_ms,
                current_bin=waste_system.current_bin  # ✅ UPDATED
            )

            # Show frame
            cv2.imshow("♻️ RecycloVision - Live AI Detection", frame)

            # ---------------------------------
            # Key Handling
            # ---------------------------------
            key = cv2.waitKey(1) & 0xFF

            # ✅ Switch bin using new intelligent system
            waste_system.switch_bin(key)

            # Exit
            if key == ord("q"):
                break

    except Exception:
        print("⚠️ System Error Occurred:")
        traceback.print_exc()

    finally:
        try:
            release_camera(cap)
        except:
            pass

        print("🛑 RecycloVision stopped safely.")


if __name__ == "__main__":
    main()