# test parallel execution with outlet limit
# check for same drink execution
# check max outlet response
# check expected output
# check ingredient low output
# check refil exeution

import pytest
import asyncio
from coffee_machine import ingredient_inventory_obj
from coffee_machine.config.machine_interface import INGREDIENT_LOW_THRESHOLD
from coffee_machine.services.inventory import IngredientsInventory
from app import place_parallel_request, get_inventory_running_low, refil_ingredient
from coffee_machine import machine_details, drink_details


@pytest.mark.integration
class TestBeverage:
    def setup_method(self):
        self.loop = asyncio.get_event_loop()

    def test_prepare_beverage(self):
        list_drink_to_request = ['hot_tea', 'hot_coffee', 'hot_coffee']
        result = self.loop.run_until_complete(
            place_parallel_request(loop=self.loop, list_drink_to_request=list_drink_to_request, console_print=False)
        )
        with open('result.txt', 'r') as f:
            result = f.readlines()
        assert set([log.strip() for log in result]) == set(
            ['hot_tea is prepared', 'hot_coffee is prepared', 'hot_coffee cannot be prepared because hot_milk is not sufficient']
        )

    def test_ingredient_unavailable(self):
        list_drink_to_request = ['green_tea']
        result = self.loop.run_until_complete(
            place_parallel_request(loop=self.loop, list_drink_to_request=list_drink_to_request, console_print=False)
        )
        with open('result.txt', 'r') as f:
            result = f.readlines()[-1].strip()
        assert result == "green_tea cannot be prepared because green_mixture is not available"

    def test_ingredient_in_sufficient(self):
        list_drink_to_request = ['hot_tea']
        result = self.loop.run_until_complete(
            place_parallel_request(loop=self.loop, list_drink_to_request=list_drink_to_request, console_print=False)
        )
        with open('result.txt', 'r') as f:
            result = f.readlines()[-1].strip()
        assert result == "hot_tea cannot be prepared because hot_milk is not sufficient"

    def test_ingredient_running_low(self):
        all_ingredients = ingredient_inventory_obj.get_ingredients
        ingredients_running_low = []
        for ingredient in all_ingredients:
            if ingredient_inventory_obj.get_inventory.get_stock_availability(
                ingredient=ingredient) <= machine_details.get_capacity(
                    ingredient=ingredient) * INGREDIENT_LOW_THRESHOLD:
                ingredients_running_low.append(ingredient)

        assert set(get_inventory_running_low()) == set(ingredients_running_low)

    def test_refil_ingredient(self):
        refil_ingredient(ingredient="hot_water")
        full_capacity = machine_details.get_capacity(ingredient="hot_water")
        assert ingredient_inventory_obj.get_inventory.get_stock_availability(ingredient="hot_water") == full_capacity
