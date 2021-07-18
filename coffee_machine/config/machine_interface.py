# machine configuration details and application config
import os
from coffee_machine.config import START_CONFIG


MACHINE_CONFIG = START_CONFIG.get("machine").get("outlets")
INVENTORY_CONFIG = START_CONFIG.get("machine").get("total_items_quantity")
DRINK_CONFIG = START_CONFIG.get("machine").get("beverages")

INGREDIENT_LOW_THRESHOLD = float(os.getenv("INGREDIENT_LOW_THRESHOLD", 0.5))
TIME_TO_PREPARE_BREVERAGE = float(os.getenv("TIME_TO_PREPARE_BREVERAGE", 0))
