import pytest

from scrappers.classes import MarketCSGOHelper


class MarketCSGOTestData:
    weapon_types = [
        'AK-47',
        'AWP',
        'M4A4',
        'M4A1-S'
    ]

    ak_47_names = [
        'Head Shot',
        'Point Disarray',
        'Frontside Misty',
        'Ice Coaled',
        'Legion of Anubis'
    ]

    awp_names = [
        'Neo-Noir',
        'Hyper Beast',
        'Worm Gog',
        'Asiimov',
        'Atheris'
    ]

    m4a4_names = [
        'Temukau',
        'The Emperor',
        'Desolate Space',
        'Neo-Noir',
        'Asiimov'
    ]

    m4a1_s_names = [
        'Decimator',
        'Black Lotus',
        "Chantico's Fire",
        'Cyrex',
        'Control Panel'
    ]

    types = [
        'Factory New',
        'Minimal Wear',
        'Field-Tested',
        'Well-Worn',
        'Battle-Scarred'
    ]


class TestMarketCSGOHelper:
    marketCSGO = MarketCSGOHelper()

    def test_is_request_not_empty(self, type='AK-47', name='Head Shot', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request is not None and request != []

    def test_is_currency_equal_usd(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['currency'] == 'USD'

    def test_is_stattrak_false(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['stattrak'] == False

    def test_is_stattrak_true(self, name='Head Shot', type='AK-47', is_stattrak=True, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['stattrak'] == True

    def test_is_price_is_float(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert isinstance(request[0]['price'], float)

    def test_is_price_is_not_empty(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['price'] != ''

    @pytest.mark.parametrize('type', MarketCSGOTestData.weapon_types)
    def test_is_request_type_equal_types(self, type, name='', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['seo']['type'] == type

    @pytest.mark.parametrize('name', MarketCSGOTestData.ak_47_names)
    def test_is_market_name_has_right_type_and_name_for_ak_47(self, name, type='AK-47', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['market_hash_name'] and request[0]['market_name']

    @pytest.mark.parametrize('name', MarketCSGOTestData.awp_names)
    def test_is_market_name_has_right_type_and_name_for_awp(self, name, type='AWP', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['market_hash_name'] and request[0]['market_name']

    @pytest.mark.parametrize('name', MarketCSGOTestData.m4a1_s_names)
    def test_is_market_name_has_right_type_and_name_for_awp(self, name, type='M4A1-S', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['market_hash_name'] and request[0]['market_name']

    @pytest.mark.parametrize('name', MarketCSGOTestData.m4a4_names)
    def test_is_market_name_has_right_type_and_name_for_awp(self, name, type='M4A4', is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['market_hash_name'] and request[0]['market_name']
