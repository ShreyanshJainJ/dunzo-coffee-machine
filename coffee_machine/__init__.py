from coffee_machine.config.machine_interface import (DRINK_CONFIG,
                                                     INVENTORY_CONFIG,
                                                     MACHINE_CONFIG)
from coffee_machine.services.drink import Beverages
from coffee_machine.services.inventory import IngredientsInventory, Inventory
from coffee_machine.services.machine import Machine


# init app details
# machine conf details
machine_details = Machine(
    outlets=MACHINE_CONFIG.get("count_n"),
    item_capacity=INVENTORY_CONFIG
)
# beverage details
drink_details = Beverages(DRINK_CONFIG)
# inventory manager
ingredient_inventory_obj = IngredientsInventory(
    inital_inventory=Inventory(INVENTORY_CONFIG))
