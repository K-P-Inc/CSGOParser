
import itertools as it
import re

def grouper(item):
    return item.nodeid[:item.nodeid.rfind('[')]

def pytest_collection_modifyitems(items):
    for _, group in it.groupby(items, grouper):
        for i, item in enumerate(group):
            if item.name.startswith("test_validate_market_response"):
                parts = item.name.split("[")
                base = parts[0]

                modifier, property, item_type = parts[1].split("]")[0].split("-", 2)

                item._nodeid = f"{base}_{property.lower()}[{item_type.lower()}][test_case={modifier.lower()}]"