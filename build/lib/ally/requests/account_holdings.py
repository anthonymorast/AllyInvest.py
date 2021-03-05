from .request import *
from ..responses.account_holdings import *

class AccountHoldingsRequest(Request):
    def __init__(self, account_id, response_format='json'):
        super().__init__(response_format)
        self.account_id = account_id

    def execute(self, ally_api):
        return AccountHoldingsResponse(self.account_id, self.response_format, ally_api.get_account_holdings(self.account_id))
