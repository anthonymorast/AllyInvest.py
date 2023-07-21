from xml.etree import ElementTree

from .request import *
from ..responses.post_order import *
from ..responses.order import *

class PostOrderRequest(Request):
    def __init__(self, account_id, order, response_format='json'):
        super().__init__(response_format)
        self.account_id = account_id
        self.order = order

    def execute(self, ally_api, cancel=False):
        if isinstance(self.order, list):
            # This is a multi-leg option order.
            # Never trust order contents; always validate it.
            for order in self.order:
                order.validate()
            # Convert to string.
            fixml_string = ElementTree.tostring(get_multileg_fixml(self.order, cancel=cancel))
        else:
            # This is a single-leg option or common stock order.
            # Never trust order contents; always validate it.
            self.order.validate()
            # Convert to string.
            fixml_string = ElementTree.tostring(self.order.to_fixml(cancel=cancel))
        return PostOrderResponse(self.account_id, self.response_format, ally_api.post_order(self.account_id, fixml_string))
