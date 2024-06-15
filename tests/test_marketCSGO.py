import parametrize_from_file

from scrappers.classes import MarketCSGOHelper


class TestMarketCSGOHelper:
    marketCSGO = MarketCSGOHelper()
    path = 'test_data.yml'

    # def test_(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
    #     request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

    #     print(request[0])

    @parametrize_from_file(path)
    def test_is_request_not_empty(self, type, name, is_stattrak, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request is not None and request != []

    @parametrize_from_file(path)
    def test_is_currency_equal_usd(self, name, type, is_stattrak, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['currency'] == 'USD'

    @parametrize_from_file(path)
    def test_is_price_is_float(self, name, type, is_stattrak, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert isinstance(request[0]['price'], float)

    @parametrize_from_file(path)
    def test_is_stattrak_false(self, is_stattrak, name, type, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['stattrak'] == False

    @parametrize_from_file(path)
    def test_is_stattrak_true(self, is_stattrak, name, type, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['stattrak'] == True

    @parametrize_from_file(path)
    def test_is_price_is_not_empty(self, name, type, is_stattrak, max_price, page_number):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['price'] != ''

    @parametrize_from_file(path)
    def test_is_request_type_equal_types(self, type, name, is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['seo']['type'] == type

    @parametrize_from_file(path)
    def test_is_market_name_has_right_type_and_name(self, name, type, is_stattrak=False, max_price='', page_number=0):
        request = self.marketCSGO.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['market_hash_name'] and request[0]['market_name']
