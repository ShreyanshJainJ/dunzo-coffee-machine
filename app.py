import os
import asyncio
from typing import List
from asyncio import AbstractEventLoop
from coffee_machine.controllers.prepare_beverage import init_parallel_outlets, request_beverage
from coffee_machine import machine_details, drink_details
from coffee_machine.controllers.maintainance_operations import ingredients_below_threshold, refil_ingredients


async def place_parallel_request(loop: AbstractEventLoop, list_drink_to_request: List[str], console_print: bool=True):
    queue = asyncio.Queue(maxsize=machine_details.outlets)
    machine_outlets = [loop.create_task(init_parallel_outlets(queue=queue, console_print=console_print)) for _ in range(machine_details.outlets)]
    
    for drink_type in list_drink_to_request:
        await queue.put(drink_type)
    await queue.join()

    for outlets in machine_outlets:
        outlets.cancel()

def get_inventory_running_low() -> list:
    return ingredients_below_threshold()

def refil_ingredient(ingredient) -> None:
    refil_ingredients(ingredient=ingredient)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    console_print = os.getenv("CONSOLE_PRINT", 'True').lower() in ('true', '1', 't')
    list_drink_to_request = drink_details.get_types_of_drink()
    # print(
    #     "Request drinks {0} with parallel outlet {1}. Each drink takes {2} seconds to prepare\n".format(
    #     ', '.join(list_drink_to_request), machine_details.outlets, float(os.getenv("TIME_TO_PREPARE_BREVERAGE", 0))
    #     )
    # )
    result = loop.run_until_complete(
        place_parallel_request(loop=loop, list_drink_to_request=list_drink_to_request, console_print=console_print)
    )
    # print("\nNow getting list of ingredients below threshold")
    # print(get_inventory_running_low())
    # print("\nNow refilling hot_water, sugar_syrup and preparing black_tea\n")
    # refil_ingredient(ingredient="hot_water")
    # refil_ingredient(ingredient="sugar_syrup")
    # list_drink_to_request =["black_tea"]
    # result = loop.run_until_complete(
    #     place_parallel_request(loop=loop, list_drink_to_request=list_drink_to_request, console_print=console_print)
    # )
