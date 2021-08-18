from ally import *
from xml.etree.ElementTree import tostring

## These values are from Ally Invest API Applications page.
CONSUMER_KEY = "CONSUMER KEY"
CONSUMER_SECRET = "CONSUMER SECRET"
OAUTH_TOKEN = "OAUTH TOKEN"
OAUTH_SECRET = "OAUTH TOKEN SECRET"

if __name__ == "__main__":
     ally = AllyAPI(OAUTH_SECRET, OAUTH_TOKEN, CONSUMER_KEY, response_format="json")

     print(ally.get_member_profile())
     print(ally.get_status())
     print(ally.get_quote("AAPL"))
     print(ally.get_quote(["AAPL", "MSFT", "XLNX", "NXPI"]))
     print(ally.news_search("AAPL"))
     print(ally.news_search(["AAPL", "MSFT", "XLNX", "NXPI"]))

     ##NOTE: this is the preferred way to get quotes! The response classes are a little
     ##      easier to work with than the JSON.
     quote_request = QuotesRequest(symbols=['SND', 'PRU', 'HMC'])
     response = quote_request.execute(ally)
     print(response.get_raw_data())

     quote_request = QuotesRequest(symbols=ticker_list)
     response = quote_request.execute(ally)
     for quote in response.get_quotes():
          # process quote data
          print(quote)
          pass

     accounts_balances_request = AccountsBalancesRequest()
     accounts_balances_response = accounts_balances_request.execute(ally)
     print(accounts_balances_response.get_raw_data())

     # Placing orders -- note that these must use XML as FIXML is passed o the calls
     account = 00000000
     # buy one share of intel at $50 for account number 00000000, print the results
     print(tostring(ally.order_common_stock("INTC", 1, ORDER_TYPE.LIMIT, account,
            SIDE.BUY, TIME_IN_FORCE.DAY, 50), 'utf-8', method="xml"))
    # sell one share of Apple at market price for account number 00000000, print the results
    print(tostring(ally.order_common_stock("AAPL", 1, ORDER_TYPE.MARKET, account, SIDE.SELL),
        'utf-8', method="xml"))
