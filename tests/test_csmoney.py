import parametrize_from_file

from scrappers.classes import CSMoneyHelper


class TestCSMoneyHelper:
    csmoney = CSMoneyHelper()
    path = 'test_data.yml'

    # def test_(self, name='Head Shot', type='AK-47', is_stattrak=False, max_price='', page_number=0):
    #     request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)

    #     print(request[0])

    @parametrize_from_file(path)
    def test_is_request_not_empty(self, type, name, is_stattrak, max_price, page_number):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)

        assert request is not None and request != []

    @parametrize_from_file(path)
    def test_is_market_name_has_right_type_and_name(self, name, type, is_stattrak=False, max_price='', page_number=0):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)

        assert f'{type} | {name}' in request[0]['asset']['names']['short'] and request[0]['asset']['names']['full']

    @parametrize_from_file(path)
    def test_is_souvenir_false_by_default(self, name, type, is_stattrak, max_price, page_number):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)
        
        assert request[0]['asset']['isSouvenir'] == False

    @parametrize_from_file(path)
    def test_is_stattrak_false(self, name, type, is_stattrak, max_price, page_number):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number )

        assert request[0]['asset']['isStatTrak'] == False

    @parametrize_from_file(path)
    def test_is_stattrak_true(self, name, type, is_stattrak, max_price, page_number):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)

        assert request[0]['asset']['isStatTrak'] == True

    @parametrize_from_file(path)
    def test_is_price_is_float(self, name, type, is_stattrak, max_price, page_number):
        request = self.csmoney.do_request(type, name, is_stattrak, max_price, page_number)

        assert isinstance(request[0]['pricing']['default'], float)
