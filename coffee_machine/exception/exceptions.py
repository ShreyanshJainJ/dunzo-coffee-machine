from coffee_machine.exception.error_codes import ErrorCode


class CMError(Exception):
    code: str = ErrorCode.DEFAULT_ERROR_CODE.value
    default_message: str = "An unkown error has occured"

    @property
    def int_code(self) -> int:
        return int(self.code[3:])

    def __init__(self, *args):
        if not args:
            self.args = (self.default_message, )


class InventoryUnavailable(CMError):
    """Stock unavailable to prepare the drink"""
    code: str = ErrorCode.GENERAIC_INVENTORY_UNAVAILABLE
    default_message = __doc__

    def __init__(self, inventory_type: str, drink_type: str):
        self.inventory_type = inventory_type
        self.drink_type = drink_type

    def __str__(self):
        return f"{self.drink_type} cannot be prepared because {self.inventory_type} is not available"


class InventoryInSufficient(CMError):
    """Inventory in sufficient to prepare selected drink"""
    code: str = ErrorCode.GENERAIC_INVENTORY_IN_SUFFICIENT
    default_message = __doc__

    def __init__(self, inventory_type: str, drink_type: str):
        self.inventory_type = inventory_type
        self.drink_type = drink_type

    def __str__(self):
        return f"{self.drink_type} cannot be prepared because {self.inventory_type} is not sufficient"
