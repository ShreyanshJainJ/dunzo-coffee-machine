# machine configuration details and application config
from coffee_machine.config import START_CONFIG


MACHINE_CONFIG = START_CONFIG.get("machine").get("outlets")
INVENTORY_CONFIG = START_CONFIG.get("machine").get("total_items_quantity")
DRINK_CONFIG = START_CONFIG.get("machine").get("beverages")

INGREDIENT_LOW_THRESHOLD = 0.2
TIME_TO_PREPARE_BREVERAGE = 5
