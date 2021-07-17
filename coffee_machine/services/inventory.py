from dataclasses import dataclass
from typing import Dict, List

from coffee_machine.config.machine_interface import (INGREDIENT_LOW_THRESHOLD,
                                                     INVENTORY_CONFIG)
from coffee_machine.exception.exceptions import (InventoryInSufficient,
                                                 InventoryUnavailable)
from coffee_machine.services.drink import Beverages
from coffee_machine.services.machine import Machine
from coffee_machine.utils.singleton_meta import SingletonMeta


@dataclass
class Inventory:
    """Dataclass for inventory

    Returns:
        [type]: [description]
    """
    inventory_availability: Dict[str, int]

    def check_if_ingredient_exists(self, ingredient: str) -> bool:
        """This method checks if the ingredient exists

        Args:
            ingredient (str): [description]

        Returns:
            bool: [description]
        """
        return ingredient in self.inventory_availability

    def check_if_ingredient_sufficient(self, ingredient: str, quantity: int) -> bool:
        """This method checks if the ingredient is sufficient

        Args:
            ingredient (str): [description]
            quantity (int): [description]

        Returns:
            bool: [description]
        """
        return quantity <= self.inventory_availability.get(ingredient, 0)

    def get_stock_availability(self, ingredient: str) -> int:
        """This method returns the available stock for the given
        ingredient

        Args:
            ingredient (str): [description]

        Returns:
            int: [description]
        """
        return self.inventory_availability.get(ingredient, 0)

    def deduct_ingredient(self, ingredient: str, quantity: int) -> None:
        """This method removes the allocated ingredients

        Args:
            ingredient (str): [description]
            quantity (int): [description]
        """
        final_inventory_value = self.inventory_availability.get(
            ingredient) - quantity
        if final_inventory_value < 0:
            final_inventory_value = 0

        self.inventory_availability[ingredient] = final_inventory_value

    def fill_ingredient(self, ingredient: str, quantity: int) -> None:
        """This method refils the ingredient

        Args:
            ingredient (str): [description]
            quantity (int): [description]
        """
        self.inventory_availability[ingredient] = quantity

    def get_all_ingredients(self) -> List[str]:
        """This method gets all the available ingredients

        Returns:
            List[str]: [description]
        """
        return [ingredient for ingredient in self.inventory_availability]


class IngredientsInventory(metaclass=SingletonMeta):
    """This singleton class manages all the inventory related
    operation for handling the stock internally. This is threadsafe.

    Args:
        metaclass ([type], optional): [description]. Defaults to SingletonMeta.
    """

    def __init__(self, inital_inventory: Inventory):
        self._inventory = inital_inventory

    def ingredients_running_low(self, machine_details: Machine) -> List[str]:
        """Returns all the ingredients which are below a threshold

        Args:
            machine_details (Machine): [description]

        Returns:
            List[str]: [description]
        """
        all_ingredients = self._inventory.get_all_ingredients()
        ingredients_running_low = []
        for ingredient in all_ingredients:
            if self._inventory.get_stock_availability(
                ingredient=ingredient) <= machine_details.get_capacity(
                    ingredient=ingredient) * INGREDIENT_LOW_THRESHOLD:
                ingredients_running_low.append(ingredient)

        return ingredients_running_low

    def reserve_inventory(self, drink_type: str, drink_details: Beverages) -> None:
        """Allocates ingredients for making drinks

        Args:
            drink_type (str): [description]
            drink_details (Beverages): [description]
        """
        self._check_if_ingredients_exists(
            drink_type=drink_type, drink_details=drink_details)
        self._check_if_ingredients_sufficient(
            drink_type=drink_type, drink_details=drink_details)
        self._deduct_inventory(drink_type=drink_type,
                               drink_details=drink_details)

    def _check_if_ingredients_exists(self, drink_type: str, drink_details: Beverages) -> None:
        """THis method checks if the ingredient exists

        Args:
            drink_type (str): [description]
            drink_details (Beverages): [description]

        Raises:
            InventoryUnavailable: [description]
        """
        list_ingredient = drink_details.get_ingredients(drink_type=drink_type)
        for ingredient in list_ingredient:
            if not self._inventory.check_if_ingredient_exists(
                ingredient=ingredient
            ):
                raise InventoryUnavailable(
                    inventory_type=ingredient, drink_type=drink_type
                )

    def _check_if_ingredients_sufficient(self, drink_type: str, drink_details: Beverages) -> None:
        """This method checks if the ingredient is sufficient

        Args:
            drink_type (str): [description]
            drink_details (Beverages): [description]

        Raises:
            InventoryInSufficient: [description]
        """
        drink_composition = drink_details.get_receipe(drink_type=drink_type)
        for ingredient in drink_composition:
            if not self._inventory.check_if_ingredient_sufficient(
                ingredient=ingredient, quantity=drink_composition.get(
                    ingredient, 0)
            ):
                raise InventoryInSufficient(
                    inventory_type=ingredient, drink_type=drink_type
                )

    def _deduct_inventory(self, drink_type: str, drink_details: Beverages) -> None:
        """This method allocates/blocks ingredients

        Args:
            drink_type (str): [description]
            drink_details (Beverages): [description]
        """
        drink_composition = drink_details.get_receipe(drink_type=drink_type)
        for ingredient in drink_composition:
            self._inventory.deduct_ingredient(
                ingredient=ingredient,
                quantity=drink_composition.get(ingredient)
            )

    def refil_ingredient(self, ingredient: str, machine_details: Machine):
        """This method refils the ingredient

        Args:
            ingredient (str): [description]
            machine_details (Machine): [description]
        """
        full_capacity = machine_details.get_capacity(ingredient=ingredient)
        self._inventory.fill_ingredient(
            ingredient=ingredient, quantity=full_capacity
        )
