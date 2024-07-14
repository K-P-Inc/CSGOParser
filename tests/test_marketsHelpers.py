import pytest
import allure
import validators
import parametrize_from_file

from typing import Callable, List, Optional, Union
from scrappers.classes import (
    BaseHelper, CSMoneyHelper,
    SkinbidHelper, MarketCSGOHelper,
    CSFloatHelper, BitskinsHelper,
    HaloskinsHelper, DmarketHelper,
    SkinportHelper, SkinbaronHelper,
    WhiteMarketHelper, GamerPayHelper
)

MarketClass = Union[CSMoneyHelper, MarketCSGOHelper, SkinbidHelper, CSFloatHelper, BitskinsHelper, HaloskinsHelper, DmarketHelper, SkinportHelper]

class MarketData:
    def __init__(self,
        key_price: str, item_price: float, item_link: str, stickers_array: List[str],
        stickers_wears: List[float | None], item_float: float | None, item_in_game_link: str | None, pattern_template: float | None, is_buy_type_fixed: str
    ):
        self.key_price = key_price
        self.item_price = item_price
        self.item_link = item_link
        self.stickers_array = stickers_array
        self.stickers_wears = stickers_wears
        self.item_float = item_float
        self.item_in_game_link = item_in_game_link
        self.pattern_template = pattern_template
        self.is_buy_type_fixed = is_buy_type_fixed

    def __str__(self):
        return f"MarketData(key_price='{self.key_price}', item_price={self.item_price}, item_link='{self.item_link}', stickers_array={self.stickers_array})"

class TestData:
    __test__ = False  # Ignoring class for pytest

    def __init__(self, name: str, type: str, is_stattrak: bool, max_price: float, page_number: int, quality: Optional[str] = None):
        self.name = name
        self.type = type
        self.is_stattrak = is_stattrak
        self.max_price = max_price
        self.page_number = page_number
        self.quality = quality

    def __str__(self):
        quality_str = f", quality='{self.quality}'" if self.quality else ""
        return f"TestData(name='{self.name}', type='{self.type}', is_stattrak={self.is_stattrak}, max_price={self.max_price}, page_number={self.page_number}{quality_str})"


markets = [pytest.param(market_class, id=market_class.DB_ENUM_NAME) for market_class in [
    CSMoneyHelper(),
    MarketCSGOHelper(),
    # SkinbidHelper(),
    CSFloatHelper(),
    BitskinsHelper(),
    # HaloskinsHelper(),
    DmarketHelper(),
    # SkinportHelper(),
    # SkinbaronHelper(),
    # WhiteMarketHelper(),
    GamerPayHelper()
]]

validators_asserts = [pytest.param(func, id=id) for (func, id) in [
    (lambda market_data, test_data: f"{test_data.type} | {test_data.name}" in market_data.key_price, "is_name_valid"),
    (lambda market_data, test_data: test_data.is_stattrak == market_data.key_price.startswith("StatTrak"), "is_stattrak"),
    (lambda market_data, _: not market_data.key_price.startswith("Souvenir"), "is_not_sounvenir"),
    (lambda market_data, _: isinstance(market_data.item_price, float), "is_price_valid"),
    (lambda market_data, _: validators.url(market_data.item_link), "is_url_valid"),
    (lambda market_data, _: len(market_data.stickers_array) >= 0, "are_stickers_exists"),
]]

@allure.parent_suite("Integration Tests")
@allure.suite("Market Helpers Test Suite")
@allure.feature("Market Data Validation")
@allure.epic("Market Scraping and Validation")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("market", markets)
class TestMarketsHelpers:
    """Test suite for Market helper classes"""

    test_data_path = "test_data.yml"
    cache: dict[tuple, List[MarketData]] = {}  # Class-level cache to store parsed data

    @allure.step('Preparing item name with quality if needed')
    def _prepare_name(self, market: BaseHelper, name: str, quality: Optional[str] = None) -> str:
        """Prepares the item name based on market specific parsing rules"""
        if market.PARSE_WITH_QUALITY:
            return f"{name} ({quality})"
        return name

    @allure.step('Fetching item list from the market')
    def _get_item_list(self, market: BaseHelper, test_data: TestData) -> List:
        """Fetches item list from the market using provided data"""
        with allure.step('Cache item data [name, type, is_stattrak, max_price, page_number, quality]'):
            cache_key = (market.DB_ENUM_NAME, test_data.name, test_data.type, test_data.is_stattrak, test_data.max_price, test_data.page_number, test_data.quality)
            if cache_key in self.cache:
                return self.cache[cache_key]

        with allure.step('Setup item name'):
            name = self._prepare_name(market, test_data.name, test_data.quality)

        with allure.step('Get raw item list from market'):
            raw_item_list = market.do_request(test_data.type, name, test_data.is_stattrak, test_data.max_price, test_data.page_number)

        with allure.step('Make sure raw item list is not None'):
            assert raw_item_list is not None

        with allure.step('Parsing raw items into MarketData objects'):
            result_list = []
            for raw_item in raw_item_list:
                key_price, item_price, item_link, stickers_array, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed = market.parse_item(raw_item)
                result_list.append(MarketData(
                    key_price, item_price, item_link, stickers_array, stickers_wears, item_float, item_in_game_link, pattern_template, is_buy_type_fixed
                ))

        with allure.step('Caching fetched item list'):
            self.cache[cache_key] = result_list
            return self.cache[cache_key]

    @allure.sub_suite("Market Data Tests")
    @allure.story("Market Data Validators")
    @allure.description("Validates fetched market data against a set of validators")
    @pytest.mark.parametrize("validator", validators_asserts)
    @parametrize_from_file(path=test_data_path, preprocess=lambda data: [{ "id": item.pop("id"), "test_data": TestData(**item) } for item in data])
    def test_validate_market_response(self, market: MarketClass, test_data: TestData, validator):
        """Validates fetched market data against a set of validators"""

        allure.dynamic.title(f'Parse: {market} using data: {test_data} and valudator: {validator}')

        items_list = self._get_item_list(market, test_data)

        with allure.step('Validating each item in the list'):
            for item in items_list:
                with allure.step(f'Validate item: {item}'):
                    assert validator(item, test_data), f"{item} is not valid in {test_data}"
