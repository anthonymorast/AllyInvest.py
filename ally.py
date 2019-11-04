"""@package AllyAPI.py
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

from URLs import *

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
            GET watchlists
            POST watchlists
            GET watchlists/:id
            DELETE watchlists/:id
            POST watchlists/:id/symbols
            DELETE watchlists/:id/symbols
        STREAMING OPERATIONS
            MARKET
                GET market/quotes

    Parameters
        @param self - the object pointer
        @param oauth_secret - secret oauth key from Ally
        @param oauth_token - oauth token from Ally
        @param client_key - client key from Ally
        @param response_format - format of the response. Valid values are 'xml' and 'json'.
            Specifying 'xml' will return an ElementTree containing the response XML while
            'json' will return the response in the JSON format.
    """
    def __init__(self, oauth_secret, oauth_token, client_key,
                response_format="json"):
        """AllyAPI constructor. Sets the response format on all of the URLs and
            the oauth/client keys required to access the API.
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




        # market
        # self.clock = "market/clock.{format}".format(format=self.format)
        # self.quote = "market/ext/quotes.{format}".format(format=self.format)
        # self.news_search = "/market/news/search.{format}".format(format=self.format)
        # self.news_article = "market/news/{article_id}.{format}".format(format=self.format, article_id="{article_id}")
        # self.toplists = "market/toplists/topgainers.{format}".format(format=self.format)
        #
        # # member
        # self.member_profile = "member/profile.{format}".format(format=self.format)
        #
        # # Utilities
        # self.status = "utility/status.{format}".format(format=self.format)
        # self.version = "utility/version.{format}".format(format=self.format)
