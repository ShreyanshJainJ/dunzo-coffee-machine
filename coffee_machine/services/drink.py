from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Beverages:
    """Dataclass for different beverages

    Returns:
        [type]: [description]
    """
    drinks: Dict[str, Dict[str, int]]

    def get_receipe(self, drink_type: str) -> Dict[str, int]:
        """This method gets the ingredient composition
        for the provided drink type

        Args:
            drink_type (str): [description]

        Returns:
            Dict[str, int]: [description]
        """
        return self.drinks.get(drink_type, {})

    def get_ingredients(self, drink_type: str) -> List[str]:
        """This method gets the list of ingredients
        for the provided drink type

        Args:
            drink_type (str): [description]

        Returns:
            List[str]: [description]
        """
        return [ingredient for ingredient in self.get_receipe(drink_type)]

    def get_types_of_drink(self) -> List[str]:
        """This method returns all the available
        drinks in the machine

        Returns:
            [type]: [description]
        """
        return [drink_type for drink_type in self.drinks]
