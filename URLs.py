class URLs:
    def __init__(self, response_format="json"):
        self.format = response_format

        self.base_url = "https://api.tradeking.com/v1/"
        # self.request_token = "https://developers.tradeking.com/oauth/request_token"
        # self.user_auth = "https://developers.tradeking.com/oauth/authorize"
        # self.resource_owner_key = "https://developers.tradeking.com/oauth/resource_owner_key"

        # account
        self.accounts = "accounts.{format}".format(format=self.format)
        self.accounts_balances = "accounts/balances.{format}".format(format=self.format)
        self.account = "accounts/{id}.{format}".format(format=self.format, id="{id}")
        self.account_balances = "accounts/{id}/balances.{format}".format(format=self.format, id="{id}")
        self.account_history = "accounts/{id}/history.{format}".format(format=self.format, id="{id}")
        self.account_holdings = "accounts/{id}/holdings.{format}".format(format=self.format, id="{id}")

        # market
        self.clock = "market/clock.{format}".format(format=self.format)
        self.quote = "market/ext/quotes.{format}".format(format=self.format)
        self.news_search = "/market/news/search.{format}".format(format=self.format)
        self.news_article = "market/news/{article_id}.{format}".format(format=self.format, article_id="{article_id}")
        self.toplists = "market/toplists/topgainers.{format}".format(format=self.format)

        # member
        self.member_profile = "member/profile.{format}".format(format=self.format)

        # Utilities
        self.status = "utility/status.{format}".format(format=self.format)
        self.version = "utility/version.{format}".format(format=self.format)

    def base_url(self):
        return self.base_url

    def request_token(self):
        return self.request_token

    def user_auth(self):
        return self.user_auth

    def resource_owner_key(self):
        return self.resource_owner_key

    """
        Accounts
    """
    def accounts_url(self):
        return self.base_url + self.accounts

    def accounts_balances_url(self):
        return self.base_url + self.accounts_balances

    def account_url(self):
        return self.base_url + self.account

    def account_balances_url(self):
        return self.base_url + self.account_balances

    def account_history_url(self):
        return self.base_url + self.account_history

    def account_holdings_url(self):
        return self.base_url + self.account_holdings

    """
        ORDER/TRADE
        TODO:
            GET accounts/:id/orders
            POST accounts/:id/orders
            POST accounts/:id/orders/preview
    """

    """
        Market
        TODO:
            GET market/options/search
            GET market/options/strikes
            GET market/options/expirations
            GET market/timesales
    """
    def clock_url(self):
        return self.base_url + self.clock

    def quote_url(self):
        return self.base_url + self.quote

    def news_search_url(self):
        return self.base_url + self.news_search

    def news_article_url(self):
        return self.base_url + self.news_article

    def toplists_url(self):
        return self.base_url + self.toplists

    """
        Member
    """
    def member_profile_url(self):
        return self.base_url + self.member_profile

    """
        Utilities
    """
    def status_url(self):
        return self.base_url + self.status

    def version_url(self):
        return self.base_url + self.version

    """
        WATCHLIST
        TODO:
            GET watchlists
            POST watchlists
            GET watchlists/:id
            DELETE watchlists/:id
            POST watchlists/:id/symbols
            DELETE watchlists/:id/symbols
    """
    """
        STREAMING OPERATIONS
            MARKET
            TODO:
                GET market/quotes
    """
