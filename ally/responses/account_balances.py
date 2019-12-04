from .response import *

class AccountBalancesResponse(Response):
    def __init__(self, account_id, response_format, data):
        super().__init__(response_format, data)
        self.account_id = account_id

    def __parse_xml(self, data):
        pass

    def __parse_json(self, data):
        pass
