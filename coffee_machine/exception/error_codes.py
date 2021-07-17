from enum import Enum, unique


@unique
class ErrorCode(Enum):
    """Defined application error codes

    Args:
        Enum ([type]): [description]
    """
    GENERIC_INPUT_ERROR = "CM-10000"
    SYSTEM_BUSY = "CM-10001"
    DEFAULT_ERROR_CODE = "CM-50000"

    # External dependencies
    GENERAIC_INVENTORY_UNAVAILABLE = "CM-30000"
    GENERAIC_INVENTORY_IN_SUFFICIENT = "CM-30001"
