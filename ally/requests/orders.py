from .request import *
from ..responses.orders import *

class OrdersRequest(Request):
    def __init__(self, account_id, response_format='json'):
        super().__init__(response_format)
        self.account_id = account_id

    def execute(self, ally_api):
        return OrdersResponse(self.account_id, self.response_format, ally_api.get_orders(self.account_id))
