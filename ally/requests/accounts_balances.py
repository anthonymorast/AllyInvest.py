from .request import *
from ..responses.accounts_balances import *

class AccountsBalancesRequest(Request):
    def __init__(self, response_format='json'):
        super().__init__(response_format)

    def execute(self, ally_api):
        return AccountsBalancesResponse(self.response_format, ally_api.get_accounts_balances())
