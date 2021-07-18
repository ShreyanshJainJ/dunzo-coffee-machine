from typing import List
from coffee_machine import ingredient_inventory_obj, machine_details


def ingredients_below_threshold() -> List[str]:
    """This controller indicates all the
    ingredients below defined threshold

    Returns:
        List[str]: [description]
    """
    return ingredient_inventory_obj.ingredients_running_low(
        machine_details=machine_details
    )


def refil_ingredients(ingredient: str) -> None:
    """This function refils the highlighted ingredient
    with the initial maximum ammount (storage max capacity)

    Args:
        ingredient (str): [description]
    """
    ingredient_inventory_obj.refil_ingredient(
        ingredient=ingredient,
        machine_details=machine_details
    )
