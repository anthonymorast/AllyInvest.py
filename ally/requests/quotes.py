from .request import *
from ..responses.quotes import *

class QuotesRequest(Request):
    def __init__(self, symbols=[], fids=[], response_format='json'):
        super().__init__(response_format)
        self.symbols = symbols
        self.fids = fids

    def set_fids(self, fids):
        self.fids = fids

    def set_symbols(self, symbols):
        self.symbols = symbols

    def get_symbols(self):
        return self.symbols

    def get_fids(self):
        return self.fids

    def execute(self, allyApi):
        return QuotesResponse(self.response_format, allyApi.get_quote(self.symbols))
