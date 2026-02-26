"""
RecycloVision - Intelligent Waste Segregation System
Combines category mapping + bin switching + validation
Fully scalable & model-independent
"""


class WasteSegregationSystem:

    # =============================
    # CATEGORY MAPPING (Label Based)
    # =============================
    CATEGORY_MAP = {

        # RECYCLABLE
        "BOTTLE": "RECYCLABLE",
        "PLASTIC_BOTTLE": "RECYCLABLE",
        "GLASS_BOTTLE": "RECYCLABLE",
        "ALUMINUM_CAN": "RECYCLABLE",
        "METAL_CAN": "RECYCLABLE",
        "PAPER": "RECYCLABLE",
        "CARDBOARD": "RECYCLABLE",

        # E-WASTE
        "CELL_PHONE": "E-WASTE",
        "SMARTPHONE": "E-WASTE",
        "LAPTOP": "E-WASTE",
        "COMPUTER": "E-WASTE",

        # GENERAL
        "PLASTIC_BAG": "GENERAL",
        "TEXTILE": "GENERAL",
        "RUBBER": "GENERAL"
    }

    CATEGORY_COLOR = {
        "RECYCLABLE": (0, 255, 0),
        "E-WASTE": (0, 0, 255),
        "GENERAL": (255, 165, 0)
    }

    # =============================
    # BIN SWITCHING SYSTEM
    # =============================

    def __init__(self):
        self.current_bin = "RECYCLABLE"

    def switch_bin(self, key):

        if key == ord("1"):
            self.current_bin = "RECYCLABLE"

        elif key == ord("2"):
            self.current_bin = "GENERAL"

        elif key == ord("3"):
            self.current_bin = "E-WASTE"

    # =============================
    # INTELLIGENT VALIDATION
    # =============================

    @classmethod
    def get_category(cls, item_label):
        return cls.CATEGORY_MAP.get(item_label.upper(), "GENERAL")

    @classmethod
    def get_color(cls, item_label):
        category = cls.get_category(item_label)
        return cls.CATEGORY_COLOR.get(category, (255, 255, 255))

    def validate(self, item_label):
        actual_category = self.get_category(item_label)
        return actual_category == self.current_bin


# Global instance
waste_system = WasteSegregationSystem()
