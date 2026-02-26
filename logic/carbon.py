"""
RecycloVision - Carbon Impact Estimator
Tracks environmental impact from recycling.
"""

from datetime import datetime
from database.db_manager import waste_db


class CarbonImpactEstimator:

    # kg CO2 saved per item
    CARBON_SAVED = {
        "BOTTLE": 0.08,
        "PLASTIC_BOTTLE": 0.08,
        "GLASS_BOTTLE": 0.10,
        "ALUMINUM_CAN": 0.15,
        "CELL_PHONE": 70,
        "SMARTPHONE": 70,
        "LAPTOP": 200,
        "COMPUTER": 300,
        "PAPER": 0.01,
        "CARDBOARD": 0.05,
        "METAL_CAN": 0.12,
        "PLASTIC_BAG": 0.05,
        "E-WASTE": 50,
        "TEXTILE": 0.20,
        "RUBBER": 0.15
    }

    def __init__(self):
        self.total_carbon_saved = 0.0
        self.items_recycled = {}
        self.session_start = datetime.now()

    # =============================
    # Add Carbon Saving
    # =============================
    def add_carbon_saving(self, item_label):

        label = item_label.upper().strip()

        carbon_value = self.CARBON_SAVED.get(label, 0)

        self.total_carbon_saved += carbon_value

        # Track item frequency
        self.items_recycled[label] = self.items_recycled.get(label, 0) + 1

        # Log to database
        waste_db.log_carbon_savings(
            item_label=label,
            carbon_value=carbon_value,
            cumulative_total=self.total_carbon_saved
        )

        return self.total_carbon_saved

    # =============================
    # Get Metrics
    # =============================
    def get_total_carbon_saved(self):
        return round(self.total_carbon_saved, 2)

    def get_impact_metrics(self):

        total_items = sum(self.items_recycled.values())

        avg_per_item = (
            self.total_carbon_saved / total_items
            if total_items > 0 else 0
        )

        return {
            "total_carbon_saved": round(self.total_carbon_saved, 2),
            "total_items_recycled": total_items,
            "items_breakdown": self.items_recycled,
            "average_carbon_per_item": round(avg_per_item, 3),
            "session_duration_seconds": (
                datetime.now() - self.session_start
            ).total_seconds()
        }

    def reset_session(self):
        self.total_carbon_saved = 0.0
        self.items_recycled = {}
        self.session_start = datetime.now()


# Global instance
carbon_tracker = CarbonImpactEstimator()

# Convenience functions
def add_carbon_saving(item_label):
    return carbon_tracker.add_carbon_saving(item_label)

def get_total_carbon_saved():
    return carbon_tracker.get_total_carbon_saved()

def get_impact_metrics():
    return carbon_tracker.get_impact_metrics()