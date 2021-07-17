import asyncio
from typing import List
from asyncio import AbstractEventLoop
from coffee_machine.controllers.prepare_beverage import init_parallel_outlets, request_beverage
from coffee_machine import machine_details, drink_details


async def place_parallel_request(loop: AbstractEventLoop, list_drink_to_request: List[str]):
    queue = asyncio.Queue(maxsize=machine_details.outlets)
    machine_outlets = [loop.create_task(init_parallel_outlets(queue=queue)) for _ in range(machine_details.outlets)]
    
    for drink_type in list_drink_to_request:
        await queue.put(drink_type)
    await queue.join()
    for outlets in machine_outlets:
        outlets.cancel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    list_drink_to_request = drink_details.get_types_of_drink()
    loop.run_until_complete(
        place_parallel_request(loop=loop, list_drink_to_request=list_drink_to_request)
    )
