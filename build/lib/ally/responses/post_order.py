from .response import *

class PostOrderResponse(Response):
    def __init__(self, account_id, response_format, data):
        super().__init__(response_format, data)
        self.account_id = account_id
        if response_format.lower() == 'xml':
            self.__parse_xml(data)
        elif response_format.lower() == 'json':
            self.__parse_json(data)

    def __parse_xml(self, data):
        super().parse_xml(data)

    def __parse_json(self, data):
        super().parse_json(data)
