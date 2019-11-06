"""@package URLs

    A Python3 class that allows access to all of the functionality in the
    Ally/TradeKing API.

    This package attempts to stay on top of changes to the API and allow an
    easy to user iterface with the Ally Invest API. The API does no formatting
    for the user. A response format of 'xml' or 'json' can be specified and
    the API responses will be returned as the raw XML or JSON, respectively.

    This API was built with the developer in mind and should allow a developer
    to build applications around the Ally Invest API without having to deal with
    accessing and managing the requests and responses.

    This project was inspired my PyAlly (https://github.com/alienbrett/PyAlly).
"""
class URLs:
    """ The URLs class will handle all of the URLs. The purpose of this class is
        to essentially store and serve all of the URL strings useful to the
        Ally Invest API.

        There is no processing of the URLs or the URL parameters done in this class
        all of that logic is handled in the AllyAPI class.
    """
    def __init__(self, response_format="json"):
        """The URLs class constructor which defines all of the URLs used by the API.

            When adding new API functionality the URL needs to be added here.
            Examples abound of the format used by this implementation of the API.

            @param self - the object pointer
            @param response_format - format of the response. Valid values are 'xml' and 'json'.
                Specifying 'xml' will return an ElementTree containing the response XML while
                'json' will return the response in the JSON format.
        """
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
        self.toplists = "market/toplists/{listtype}.{format}".format(format=self.format, listtype="{listtype}")

        # member
        self.member_profile = "member/profile.{format}".format(format=self.format)

        # Utilities
        self.status = "utility/status.{format}".format(format=self.format)
        self.version = "utility/version.{format}".format(format=self.format)

        # watchlists
        self.watchlists = "watchlists.{format}".format(format=self.format)

    def base_url(self):
        """Returns the API request endpoint.
            @param self - the object pointer
        """
        return self.base_url

    # def request_token(self):
    #     """
    #         @param self - the object pointer
    #     """
    #     return self.request_token
    #
    # def user_auth(self):
    #     """
    #         @param self - the object pointer
    #     """
    #     return self.user_auth
    #
    # def resource_owner_key(self):
    #     """
    #         @param self - the object pointer
    #     """
    #     return self.resource_owner_key

    """
        Accounts
    """
    def accounts_url(self):
        """Combines the request endpoint and accounts API URLs
            @param self - the object pointer
        """
        return self.base_url + self.accounts

    def accounts_balances_url(self):
        """Combines the request endpoint and accounts balances API URLs
            @param self - the object pointer
        """
        return self.base_url + self.accounts_balances

    def account_url(self):
        """Combines the request endpoint and account API URLs
            @param self - the object pointer
        """
        return self.base_url + self.account

    def account_balances_url(self):
        """Combines the request endpoint and account balances API URLs
            @param self - the object pointer
        """
        return self.base_url + self.account_balances

    def account_history_url(self):
        """Combines the request endpoint and account history API URLs
            @param self - the object pointer
        """
        return self.base_url + self.account_history

    def account_holdings_url(self):
        """Combines the request endpoint and account holding API URLs
            @param self - the object pointer
        """
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
        """Combines the request endpoint and market clock API URLs
            @param self - the object pointer
        """
        return self.base_url + self.clock

    def quote_url(self):
        """Combines the request endpoint and quote API URLs
            @param self - the object pointer
        """
        return self.base_url + self.quote

    def news_search_url(self):
        """Combines the request endpoint and news search API URLs
            @param self - the object pointer
        """
        return self.base_url + self.news_search

    def news_article_url(self):
        """Combines the request endpoint and news article API URLs
            @param self - the object pointer
        """
        return self.base_url + self.news_article

    def toplists_url(self):
        """Combines the request endpoint and toplists API URLs
            @param self - the object pointer
        """
        return self.base_url + self.toplists

    """
        Member
    """
    def member_profile_url(self):
        """Combines the request endpoint and member profile API URLs
            @param self - the object pointer
        """
        return self.base_url + self.member_profile

    """
        Utilities
    """
    def status_url(self):
        """Combines the request endpoint and server status API URLs
            @param self - the object pointer
        """
        return self.base_url + self.status

    def version_url(self):
        """Combines the request endpoint and API version API URLs
            @param self - the object pointer
        """
        return self.base_url + self.version

    """
        WATCHLIST
        TODO:
            GET watchlists/:id
            DELETE watchlists/:id
            POST watchlists/:id/symbols
            DELETE watchlists/:id/symbols
    """
    def get_watchlists_url(self):
        """Combines the request endpoint and watchlist get URLs. Note this is the
        same URL as the POST call (URLs.post_watchlist_url()).
        """
        return self.base_url + self.watchlists

    def post_watchlist_url(self):
        """Combines the request endpoint and watchlist post URLs"""
        return self.base_url + self.watchlists

    """
        STREAMING OPERATIONS
            MARKET
            TODO:
                GET market/quotes
    """
