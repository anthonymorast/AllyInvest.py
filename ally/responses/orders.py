from .response import *
from .order import *

class OrdersResponse(Response):
    def __init__(self, account_id, response_format, data):
        super().__init__(response_format, data)
        self.account_id = account_id
        self.orders = []
        if response_format.lower() == 'xml':
            self.__parse_xml(data)
        elif response_format.lower() == 'json':
            self.__parse_json(data)

    def __parse_xml(self, data):
        super().parse_xml(data)
        for order_xml in self.xml.find('orderstatus').findall('order'):
            order = Order()
            order.from_xml(order_xml)
            self.orders.append(order)

    def __parse_json(self, data):
        super().parse_json(data)
        for order_json in self.json['orderstatus']['order']:
            order = Order()
            order.from_json(order_json)
            self.orders.append(order)

    def get_orders(self):
        return self.orders

