from ally import *

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
          pass
          
     accounts_balances_request = AccountsBalancesRequest()
     accounts_balances_response = accounts_balances_request.execute(ally)
     print(accounts_balances_response.get_raw_data())
