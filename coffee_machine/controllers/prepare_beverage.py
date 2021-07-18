from coffee_machine.controllers import store_log
import asyncio
import time
from asyncio import Queue

from coffee_machine import (drink_details, ingredient_inventory_obj,
                            machine_details)
from coffee_machine.config.machine_interface import TIME_TO_PREPARE_BREVERAGE
from coffee_machine.exception.exceptions import CMError


async def request_beverage(drink_type: str) -> None:
    """This method requests for drinks.
    It acts as machine interface

    Args:
        drink_type (str): [description]
    """
    try:
        # checks first if ingredients can be reserved
        ingredient_inventory_obj.reserve_inventory(
            drink_type=drink_type, drink_details=drink_details
        )
        # assuming constant time for all drinks to be prepared
        return await _prepare_beverage(drink_type=drink_type)
    except CMError as error:
        return _provide_reject_feedback(exception=error)


def _provide_reject_feedback(exception: str) -> None:
    """Interface to provide feedback to users incase
    breverages cannot be created

    Args:
        exception (str): [description]
    """
    return str(exception)


async def _prepare_beverage(drink_type: str) -> None:
    """Interface to provide drink created feedback to the user

    Args:
        drink_type (str): [description]
    """
    await asyncio.sleep(TIME_TO_PREPARE_BREVERAGE)
    return f"{drink_type} is prepared"


async def init_parallel_outlets(queue: Queue, console_print: bool):
    """Parallel handling capacity based on the
    number of outlet defined in config.
    Works based on asyncio Queue and outlets defined
    in app

    Args:
        queue (Queue): [description]
    """
    while True:
        # wait until request posted
        drink_requested = await queue.get()
        # create drink
        result = await request_beverage(drink_requested)
        if console_print:
            print(result)
        store_log(result=result)
        # compelete the task
        queue.task_done()
