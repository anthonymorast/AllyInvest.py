"""@package AllyAPI
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

from requests_oauthlib import OAuth1
from xml.etree import ElementTree
import datetime
import requests
import json

from .URLs import URLs

class AllyAPI:
    """The AllyAPI class providing blackbox use of the Ally Invest API.

    This is the main class of the API module. This should be the only class used in
    applictions built around the API. The AllyAPI class allows access to the GET and
    POST requests supported by Ally Invest.

    Missing Functionality:
        ORDER/TRADE
            GET accounts/:id/orders
            POST accounts/:id/orders
            POST accounts/:id/orders/preview
        MARKET
            GET market/options/search
            GET market/options/strikes
            GET market/options/expirations
            GET market/timesales
        WATCHLIST
            GET watchlists/:id
            DELETE watchlists/:id
            POST watchlists/:id/symbols
            DELETE watchlists/:id/symbols
        STREAMING OPERATIONS
            MARKET
                GET market/quotes
    """
    def __init__(self, oauth_secret, oauth_token, client_key,
                response_format="json"):
        """AllyAPI constructor. Sets the response format on all of the URLs and
            the oauth/client keys required to access the API.

            Parameters
                @param self - the object pointer
                @param oauth_secret - secret oauth key from Ally
                @param oauth_token - oauth token from Ally
                @param client_key - client key from Ally
                @param response_format - format of the response. Valid values are 'xml' and 'json'.
                    Specifying 'xml' will return an ElementTree containing the response XML while
                    'json' will return the response in the JSON format.
        """
        self.format = response_format
        self.url = URLs(response_format=response_format)

        self.oauth_secret = oauth_secret
        self.oauth_token = oauth_token
        self.client_key = client_key
        self.client_secret = client_key

        self.auth_time = None
        self.auth = None
        self.valid_auth_dt = datetime.timedelta(seconds=10)

    def __create_auth(self):
        """A private method to create the OAuth1 object, if necessary."""
        now = datetime.datetime.now()

        if self.auth == None or self.auth_time + self.valid_auth_dt < now:
            self.auth_time = now
            self.auth = OAuth1(self.client_key, self.client_secret, self.oauth_token,
                          self.oauth_secret, signature_type='auth_header')

    def __get_symbol_string(self, symbols):
        """Returns a string that is either a single quote or a comma-separated
            list of quotes depending on the type of quotes.
            @param self - the object pointer
            @param symbols - single ticker or list of ticker to get quotes for
        """
        if not isinstance(symbols, str): # list
            symbols = ",".join(symbols)
        return symbols

    def __to_format(self, response):
        """A private method to return the API response in the desired format
            @param self - the object pointer
            @param response - response from the Ally Invest API
        """
        if self.format == "json":
            return response.json()
        else:
            return ElementTree.fromstring(response.content)

    def __get_data(self, url):
        """A private method to return the requested data in the requested format
            for a given URL.
            @param self - the object pointer
            @param url - API URL to access
        """
        self.__create_auth()
        return self.__to_format(requests.get(url, auth=self.auth))

    def __submit_post(self, url, data):
        """A private method to submit a post request to the Ally Invest server
            @param self - the object pointer
            @param url - API URL to access
            @param data - payload for the HTTP request
        """
        self.__create_auth()
        return self.__to_format(requests.post(url, data=data, auth=self.auth))

    def get_accounts(self):
        """Returns all of the user's accounts."""
        return self.__get_data(self.url.accounts_url())

    def get_accounts_balances(self):
        """Returns the balances of all of the user's accounts."""
        return self.__get_data(self.url.accounts_balances_url())

    def get_account(self, id):
        """Returns a specific account provided the account ID (account number)
            @param self - the object pointer
            @param id - account number
        """
        return self.__get_data(self.url.account_url().format(id=str(id)))

    def get_account_balances(self, id):
        """Returns the balances of a specific account (ID = account number)
            @param self - the object pointer
            @param id - account number
        """
        return self.__get_data(self.url.account_balances_url().format(id=str(id)))

    def get_account_history(self, id):
        """Returns the history of a specific account (ID = account number)
            @param self - the object pointer
            @param id - account number
        """
        return self.__get_data(self.url.account_history_url().format(id=str(id)))

    def get_account_holdings(self, id):
        """Returns the holdings of a specific account (ID = account number)
            @param self - the object pointer
            @param id - account number
        """
        return self.__get_data(self.url.account_holdings_url().format(id=str(id)))

    def get_market_clock(self):
        """Returns the state of the market, the time until next state change,
            and current server timestamp.
            @param self - the object pointer
        """
        return self.__get_data(self.url.clock_url())

    def get_quote(self, symbols):
        """Returns quote information for a single ticker or list of tickers.
            Note: this function does not implement selecting customer FIDs as
            described in the API documentation. These can be filtered from the return
            if need be.
            @param self - the object pointer
            @param symbols - single ticker or list of ticker to get quotes for
        """
        url = self.url.quote_url()+"?symbols={symbols}"
        symbols = self.__get_symbol_string(symbols)
        return self.__get_data(url.format(symbols=symbols))

    def news_search(self, symbols, startdate=None, enddate=None, maxhits=10):
        """Retrieves a listing of news headlines based on symbols.
            @param self - the object pointer
            @param symbols - single ticker or list of ticker to get quotes for
            @param startdate - search for articles between this date and enddate
            @param enddate - search for articles between this date and startdate
            @param maxhits - number of articles to return
        """
        if startdate is None or enddate is None:
            print("news_search: either enddate or startdate is not specified, ignoring both.")

        if (startdate is not None and enddate is not None) and (enddate < startdate):
            print("news_search: start date is after end date.")
            raise Exception("Start date is after end date in news search.")

        url = self.url.news_search_url() + "?symbols={syms}&maxhits={mxhits}".format(mxhits=maxhits, syms="{syms}")
        if startdate is not None and enddate is not None:
            url += "&startdate={sdate}&enddate={edate}" \
                .format(sdate=startdate.strftime("%m/%d/%Y"), edate=enddate.strftime("%m/%d/%Y"))

        symbols = self.__get_symbol_string(symbols)
        return self.__get_data(url.format(syms=symbols))

    def get_news_article(self, article_id):
        """Gets a single news article based on the article ID. This ID can be retrieved
            from the news_search()  function.
            @param self - the object pointer
            @param article_id - ID of the article to retrieve
        """
        return self.__get_data(self.url.news_article_url().format(article_id=article_id))

    def get_toplists(self, listtype="topgainers", exchange="N"):
        """Returns a ranked list depending on listtype and exchange.
            @param listtype - type of list to be queried, accepted values are:
                'toplosers': top losers by dollar amount
                'toppctlosers': top percentage losers
                'topvolume': top volume
                'topactive': top active
                'topgainers': top gainers by dollar amount (default)
                'toppctgainers': top percentage gainers
            @param exchange - exchange to be queried, accepted values are:
                'A': American Stock Exchange
                'N': New York Stock Exchange (default)
                'Q': NASDAQ
                'U': NASDAQ Bulletin Board
                'V': NASDAQ OTC Other
        """
        url = self.url.toplists_url().format(listtype=listtype)
        url += "?exchange={ex}".format(ex=exchange)
        return self.__get_data(url)

    def get_member_profile(self):
        """Returns general information associated with the user including account
            numbers and account information.
            @param self - the object pointer
        """
        return self.__get_data(self.url.member_profile_url())

    def get_status(self):
        """Returns an error if the API endpoint/server is unavailable. Otherwise
            returns the current server timestamp.
            @param self - the object pointer
        """
        return self.__get_data(self.url.status_url())

    def get_version(self):
        """Gets the current version of the API of the endpoint called.
            @param self - the object pointer
        """
        return self.__get_data(self.url.version_url())

    def get_watchlists(self):
        """Retrieves all watchlists belonging to the member.
            @param self - the object pointer
        """
        return self.__get_data(self.url.get_watchlists_url())


    def create_watchlist(self, watchlist_name, symbols=""):
        """Creates a watchlist and adds a symbol or list of symbols to a watchlist.
            WARNING: There appears to be an issue when adding a list of symbols.
                It is recommended that one ticker symbol is added at a time.
            @param self - the object pointer
            @param watchist_id - name of the watchlist
            @param symbols - single ticker or list of tickers to add to the watchlist
        """
        print("WARNING create_watchlist(): There appears to be an issue when adding a list of symbols. It is recommended that one ticker symbol is added at a time.")
        payload = {"id": watchlist_name}
        if not symbols == "":
            payload["symbols"] = symbols
        return self.__submit_post(self.url.post_watchlist_url(), payload)
