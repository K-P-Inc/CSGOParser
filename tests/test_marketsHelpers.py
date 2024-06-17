import parametrize_from_file
import pytest
import validators

from scrappers.classes import CSMoneyHelper, MarketCSGOHelper, SkinbidHelper, CSFloatHelper, BitskinsHelper, HaloskinsHelper, DmarketHelper, SkinportHelper

markets = [pytest.param(market_class, id=market_class.DB_ENUM_NAME) for market_class in [
    CSMoneyHelper(),
    MarketCSGOHelper(),
    SkinbidHelper(),
    # CSFloatHelper(),
    BitskinsHelper(),
    HaloskinsHelper(),
    DmarketHelper(),
    # SkinportHelper() TODO: Needs cookies for tests
]]

@pytest.mark.parametrize('market', markets)
class TestMarketsHelpers:
    path = 'test_data.yml'

    def _prepare_name(self, market, name, quality):
        if market.PARSE_WITH_QUALITY:
            return f"{name} | ({quality})"
        return name

    @parametrize_from_file(path)
    def test_is_market_name_has_right_type_and_name(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert f'{type} | {name}' in key_price

    @parametrize_from_file(path)
    def test_is_stattrak_and_souvenir_false(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert not key_price.startswith('StatTrak') and not key_price.startswith('Souvenir')

    @parametrize_from_file(path)
    def test_is_stattrak_true(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert key_price.startswith('StatTrak')

    @parametrize_from_file(path)
    def test_is_price_is_float(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert isinstance(item_price, float)

    @parametrize_from_file(path)
    def test_is_url_valid(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert validators.url(link)

    @parametrize_from_file(path)
    def test_is_stickers_array_not_empty(self, market, name, type, is_stattrak, max_price, page_number, quality):
        name = self._prepare_name(market, name, quality)

        dirty_item_list = market.do_request(type, name, is_stattrak, max_price, page_number)

        assert dirty_item_list is not None

        for dirty_item in dirty_item_list:
            key_price, item_price, link, stickers_array = market.parse_item(dirty_item)

            assert len(stickers_array) > 0
