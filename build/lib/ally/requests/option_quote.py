from .request import *
from ..responses.quotes import *

class OptionQuoteRequest(Request):
    def __init__(self, symbol, exp_date, strike, put_call, response_format='json'):
        super().__init__(response_format)
        self.symbol = symbol
        self.exp_date = exp_date
        self.strike = strike
        self.put_call = put_call

    def execute(self, allyApi):
        return QuotesResponse(self.response_format, allyApi.get_option_quote(self.symbol, self.exp_date, self.strike, self.put_call))
