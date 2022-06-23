from ally import *

## These values are from Ally Invest API Applications page.
CONSUMER_KEY = "CONSUMER KEY"
CONSUMER_SECRET = "CONSUMER SECRET"
OAUTH_TOKEN = "OAUTH TOKEN"
OAUTH_SECRET = "OAUTH TOKEN SECRET"
ACCOUNT_ID = "ACCOUNT ID"

if __name__ == "__main__":
     ally = AllyAPI(OAUTH_SECRET, OAUTH_TOKEN, CONSUMER_KEY, response_format="json")

     print(ally.get_member_profile())
     print(ally.get_status())
     print(ally.get_quote("AAPL"))
     print(ally.get_quote(["AAPL", "MSFT", "XLNX", "NXPI"]))
     print(ally.news_search("AAPL"))
     print(ally.news_search(["AAPL", "MSFT", "XLNX", "NXPI"]))

     quote_request = QuotesRequest(symbols=['SND', 'PRU', 'HMC'])
     response = quote_request.execute(ally)
     print(response.get_raw_data())

     accounts_balances_request = AccountsBalancesRequest()
     accounts_balances_response = accounts_balances_request.execute(ally)
     print(accounts_balances_response.get_raw_data())

     new_order = Order(acct=ACCOUNT_ID, sym="AAPL", qty=100, sec_typ="CS", side=1, typ=2, px=150.00, tm_in_force=1)
     post_preview_request = PostOrderPreviewRequest(ACCOUNT_ID, new_order)
     post_preview_response = post_preview_request.execute(ally)
     print(post_preview_response.get_raw_data())
