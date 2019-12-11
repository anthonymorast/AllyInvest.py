from .response import *
from .holding import *

class AccountHoldingsResponse(Response):
    def __init__(self, account_id, response_format, data):
        super().__init__(response_format, data)
        self.raw_data = data
        self.response_format = response_format
        self.account_id = account_id
        self.holdings = []
        if response_format.lower() == 'xml':
            self.__parse_xml(data)
        elif response_format.lower() == 'json':
            self.__parse_json(data)

    def __parse_xml(self, data):
        super().parse_json(data)
        for holding_json in data['accountholdings']:
            holding = Holding()
            self.holdings.append(holding.from_xml(holding_json))

    def __parse_json(self, data):
        super().parse_json(data)
        for holding_json in self.json['accountholdings']['holding']:
            holding = Holding()
            holding.from_json(holding_json)
            self.holdings.append(holding)

    def get_holdings(self):
        return self.holdings

    def get_raw_data(self):
        return self.raw_data
