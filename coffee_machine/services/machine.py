from dataclasses import dataclass
from typing import Dict


@dataclass
class Machine:
    """dataclass for machine related

    Returns:
        [type]: [description]
    """
    outlets: int
    item_capacity: Dict[str, int]

    def get_capacity(self, ingredient: str) -> int:
        """This method gets the maxium storage capacity available
        for a given ingredient

        Args:
            ingredient (str): [description]

        Returns:
            int: [description]
        """
        return self.item_capacity.get(ingredient, 0)
