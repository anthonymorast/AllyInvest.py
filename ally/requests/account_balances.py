from .request import *
from ..responses.account_balances import *

class AccountBalancesRequest(Request):
    def __init__(self, account_id, response_format='json'):
        super().__init__(response_format)
        self.account_id = account_id

    def execute(self, ally_api):
        return AccountBalancesResponse(self.account_id, self.response_format, ally_api.get_account_balances(self.account_id))
