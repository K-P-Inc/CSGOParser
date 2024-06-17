import itertools as it
import allure
import re

@allure.step("Modifying item names for better grouping")
def grouper(item):
    return item.nodeid[:item.nodeid.rfind('[')]

@allure.feature("Test Collection Modification")
@allure.story("Grouping and Modifying Test Item Names")
def pytest_collection_modifyitems(items):
    """
    Modifies the collection of test items to improve the readability and structure of test reports.
    Groups tests by their base name and modifies their node IDs to include additional context.
    """
    for _, group in it.groupby(items, grouper):
        for i, item in enumerate(group):
            if item.name.startswith("test_validate_market_response"):
                with allure.step(f"Processing item: {item.name}"):
                    parts = item.name.split("[")
                    base = parts[0]

                    modifier, property, item_type = parts[1].split("]")[0].split("-", 2)

                    item._nodeid = f"{base}_{property.lower()}[{item_type.lower()}][test_case={modifier.lower()}]"