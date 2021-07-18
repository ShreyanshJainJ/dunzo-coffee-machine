# dunzo-coffee-machine
Dunzo coffee machine assignment

1. Clean python code using design patters
2. Proper application exception handling with application error codes
3. Parallelism with asyncio
4. Integration tests
5. Results stored in local results.txt file (refreshed with every run) for operation logs / daily tally.
6. Added environment varaibles (details below)


## Assumptions
1. Refil operation fills the specific ingredient to full
2. Ingredient max storage capacity is as defined in initial coffee machine config
3. Only integration testing is added


## Application tested on
Python 3.8


## Getting Started
### Requirements
Install requirements from **`coffee_machine\requirements.txt`** & **`tests\requirements.txt`**

### Application configs
Initial input JSON in `coffee_machine\config\__init__.py`
Pytest addoption in `pytest.ini`

### To run application
Run **`python app.py`** from project root

### To run integration tests
Run **`pytest`** from project root

## Environment Variables
| Variable | Description | Default Values
| -------- | ---------- | ---------|
| INGREDIENT_LOW_THRESHOLD | Ingredient low threshold percentage indicator | 0.5 |
| TIME_TO_PREPARE_BREVERAGE | Time taken to prepare beverage in seconds | 0 |

## Pytest coverage details
```
Name                                                    Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------------------------------
coffee_machine\__init__.py                                  8      0      0      0   100%
coffee_machine\config\__init__.py                           1      0      0      0   100%
coffee_machine\config\machine_interface.py                  7      0      0      0   100%
coffee_machine\controllers\__init__.py                      6      0      0      0   100%
coffee_machine\controllers\maintainance_operations.py       6      0      0      0   100%
coffee_machine\controllers\prepare_beverage.py             25      1      2      1    93%
coffee_machine\exception\__init__.py                        0      0      0      0   100%
coffee_machine\exception\error_codes.py                     8      0      2      0   100%
coffee_machine\exception\exceptions.py                     26      3      2      0    82%
coffee_machine\services\__init__.py                         0      0      0      0   100%
coffee_machine\services\drink.py                           11      1      6      0    82%
coffee_machine\services\inventory.py                       62      1     20      1    98%
coffee_machine\services\machine.py                          8      0      2      0   100%
coffee_machine\utils\singleton_meta.py                     10      0      2      1    92%
-----------------------------------------------------------------------------------------
TOTAL                                                     178      6     36      3    94%
```

