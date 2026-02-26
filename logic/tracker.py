"""
RecycloVision - Waste Segregation Tracker
Handles behavioral tracking and purity score computation.
"""

from datetime import datetime


class WasteSegregationTracker:

    def __init__(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.session_start = datetime.now()
        self.detection_history = []

    # =============================
    # Log Detection Result
    # =============================
    def log_detection(self, item_label, is_correct, confidence_score=None):

        if is_correct:
            self.correct_count += 1
        else:
            self.wrong_count += 1

        record = {
            "timestamp": datetime.now(),
            "item_label": item_label,
            "is_correct": is_correct,
            "confidence": confidence_score,
            "purity_at_time": self.compute_purity_score()
        }

        self.detection_history.append(record)

    # =============================
    # Purity Score Calculation
    # =============================
    def compute_purity_score(self):

        total = self.correct_count + self.wrong_count

        if total == 0:
            return 0.0

        purity = (self.correct_count / total) * 100
        return round(purity, 2)

    # =============================
    # Get Summary Stats
    # =============================
    def get_stats(self):

        return {
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count,
            "total_detections": self.correct_count + self.wrong_count,
            "purity_score": self.compute_purity_score(),
            "session_duration_seconds": (
                datetime.now() - self.session_start
            ).total_seconds()
        }

    def reset_session(self):
        self.correct_count = 0
        self.wrong_count = 0
        self.session_start = datetime.now()
        self.detection_history = []


# Global instance
waste_tracker = WasteSegregationTracker()