"""
RecycloVision - Advanced Production Database Layer
Thread-safe SQLite telemetry database with optimized performance,
context management, structured analytics, and time-based querying.
"""

import sqlite3
from datetime import datetime, timedelta
import os
import logging
import threading


# Ensure folders exist
os.makedirs("data", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Logger setup
logger = logging.getLogger("database")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("logs/database.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class WasteDatabase:

    def __init__(self, db_path="data/waste_telemetry.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._initialize_database()

    # =============================
    # CONNECTION HANDLER
    # =============================

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    # =============================
    # DATABASE INITIALIZATION
    # =============================

    def _initialize_database(self):

        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detection_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    item_label TEXT,
                    is_correct BOOLEAN,
                    confidence REAL,
                    purity_score REAL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS low_confidence_detections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    frame_id INTEGER,
                    label TEXT,
                    confidence REAL,
                    lighting_metric REAL,
                    dynamic_threshold REAL,
                    timestamp DATETIME
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS carbon_savings_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_label TEXT,
                    carbon_value REAL,
                    cumulative_total REAL,
                    timestamp DATETIME
                )
            """)

            # Indexing for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_detection_time ON detection_results(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_carbon_time ON carbon_savings_log(timestamp)")

            conn.commit()

        logger.info("✅ Database initialized successfully")

    # =============================
    # INSERT OPERATIONS (Thread-Safe)
    # =============================

    def log_detection_result(self, item_label, is_correct, confidence, purity_score):

        with self.lock:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO detection_results
                    (timestamp, item_label, is_correct, confidence, purity_score)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now(),
                    item_label,
                    is_correct,
                    confidence,
                    purity_score
                ))

        logger.info(f"Detection logged | {item_label} | {confidence:.2f}")

    def log_low_confidence_detection(self, frame_id, label, confidence, lighting_metric, dynamic_threshold):

        with self.lock:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO low_confidence_detections
                    (frame_id, label, confidence, lighting_metric, dynamic_threshold, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    frame_id,
                    label,
                    confidence,
                    lighting_metric,
                    dynamic_threshold,
                    datetime.now()
                ))

        logger.warning(f"Low confidence | {label} | {confidence:.2f}")

    def log_carbon_savings(self, item_label, carbon_value, cumulative_total):

        with self.lock:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO carbon_savings_log
                    (item_label, carbon_value, cumulative_total, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (
                    item_label,
                    carbon_value,
                    cumulative_total,
                    datetime.now()
                ))

        logger.info(f"Carbon logged | {item_label} | Total: {cumulative_total}")

    # =============================
    # ADVANCED ANALYTICS
    # =============================

    def get_detection_stats(self):

        with self._get_connection() as conn:

            total = conn.execute("SELECT COUNT(*) FROM detection_results").fetchone()[0]

            avg_conf = conn.execute("SELECT AVG(confidence) FROM detection_results").fetchone()[0] or 0

            correct = conn.execute("""
                SELECT COUNT(*) FROM detection_results
                WHERE is_correct = 1
            """).fetchone()[0]

            purity = (correct / total * 100) if total > 0 else 0

        return {
            "total_detections": total,
            "average_confidence": round(avg_conf, 3),
            "purity_score": round(purity, 2)
        }

    def get_item_breakdown(self):

        with self._get_connection() as conn:

            rows = conn.execute("""
                SELECT item_label, COUNT(*) as count
                FROM detection_results
                GROUP BY item_label
                ORDER BY count DESC
            """).fetchall()

        return {row["item_label"]: row["count"] for row in rows}

    def get_recent_activity(self, hours=24):

        cutoff = datetime.now() - timedelta(hours=hours)

        with self._get_connection() as conn:

            rows = conn.execute("""
                SELECT * FROM detection_results
                WHERE timestamp >= ?
            """, (cutoff,)).fetchall()

        return [dict(row) for row in rows]

    def get_total_carbon_saved(self):

        with self._get_connection() as conn:
            result = conn.execute("""
                SELECT MAX(cumulative_total)
                FROM carbon_savings_log
            """).fetchone()[0]

        return round(result, 2) if result else 0


# Global instance
waste_db = WasteDatabase()