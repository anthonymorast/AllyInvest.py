from .response import *

class QuotesResponse(Response):
    def __init__(self, response_format, data):
        super().__init__(response_format, data)

    def __parse_xml(self, data):
        pass

    def __parse_json(self, data):
        pass
