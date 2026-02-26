"""
Performance Monitoring Module
Handles FPS and latency calculation
"""

import time


class PerformanceMonitor:

    def __init__(self):
        self.prev_time = 0

    def calculate(self):

        current_time = time.time()

        if self.prev_time == 0:
            self.prev_time = current_time
            return 0, 0

        fps = 1 / (current_time - self.prev_time)
        latency_ms = int((1 / fps) * 1000)

        self.prev_time = current_time

        return round(fps, 1), latency_ms


# Global instance
performance_monitor = PerformanceMonitor()