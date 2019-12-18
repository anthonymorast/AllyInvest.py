from .response import *
from .quote import *

class QuotesResponse(Response):
    def __init__(self, response_format, data):
        super().__init__(response_format, data)
        self.quotes = []
        if response_format.lower() == 'xml':
            self.__parse_xml(data)
        elif response_format.lower() == 'json':
            self.__parse_json(data)

    def __parse_xml(self, data):
        pass

    def __parse_json(self, data):
        super().parse_json(data)
        for quote_json in self.json['quotes']['quote']:
            quote = Quote()
            quote.from_json(quote_json)
            self.quotes.append(quote)

    def get_quotes(self):
        return self.quotes
