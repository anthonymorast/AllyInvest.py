from ally import * 

## These values are from Ally Invest API Applications page.
CONSUMER_KEY = "CONSUMER KEY"
CONSUMER_SECRET = "CONSUMER SECRET"
OAUTH_TOKEN = "OAUTH TOKEN"
OAUTH_SECRET = "OAUTH TOKEN SECRET"

if __name__ == "__main__":
#     ally = AllyAPI(OAUTH_SECRET, OAUTH_TOKEN, CONSUMER_KEY, response_format="json")
#     print(ally.get_accounts())
    acct_balances = AccountBalances()
