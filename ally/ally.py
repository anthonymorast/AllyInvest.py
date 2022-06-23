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
from collections import defaultdict
import re
import copy

from .URLs import URLs

class AllyAPI:
    """The AllyAPI class providing blackbox use of the Ally Invest API.

    This is the main class of the API module. This should be the only class used in
    applictions built around the API. The AllyAPI class allows access to the GET and
    POST requests supported by Ally Invest.

    Missing Functionality:
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

    def __convert_fixml_json(self, json_data):
        """Takes the order data and converts it to a consistent format.
           The FIXML message is also expanded, with the original intact.
            @param self - the object pointer
            @param json_data - original data to be converted.
        """
        # If there's no orders, there's nothing to do.
        if not json_data["response"]["orderstatus"]["order"]:
            return json_data

        # Copy the data to keep from overwriting the input.
        data = copy.deepcopy(json_data)

        # A single order will be a dict, and multiple a list.
        # Convert order to always be a list of dicts.
        if isinstance(data["response"]["orderstatus"]["order"], dict):
            data["response"]["orderstatus"]["order"] = \
                [data["response"]["orderstatus"]["order"]]

        # Convert the FIXML message in each order.
        # Add the keys to order itself, but preserve fixmlmessage.
        for order in data["response"]["orderstatus"]["order"]:
            order_xml = ElementTree.fromstring(order["fixmlmessage"])
            order.update(self.__fixml_to_dict(order_xml))

        # Return the converted data.
        return data

    def __convert_fixml_xml(self, xml_data):
        """Takes the order data and expands the FIXML message.
           The original message is left intact.
            @param self - the object pointer
            @param xml_data - original data to be converted.
        """
        # Register the FIXML namespace.
        ElementTree.register_namespace("", "http://www.fixprotocol.org/FIXML-5-0-SP2")

        # Copy the data to keep from overwriting the input.
        data = copy.deepcopy(xml_data)

        # Each order will have a "fixmlmessage" to convert.
        for order in data.find("orderstatus").findall("order"):
            fixml_text = order.find("fixmlmessage").text
            fixml = ElementTree.fromstring(fixml_text)
            order.append(fixml)

        # Return the converted data.
        return data

    def __fixml_to_dict(self, fixml):
        """Recursively convert FIXML to a dictionary.
            @param self - the object pointer
            @param fixml - FIXML Element to be converted.
        """
        # Remove the Namespace from the tag.
        tag = re.sub(r"\{[^}]*\} *", "", fixml.tag)

        # Establish the final dictionary to return.
        ret = {tag: {} if fixml.attrib else None}

        # Recursively convert each subelement.
        # Each subelement becomes a tag key with a dict value.
        children = list(fixml)
        if children:
            defdict = defaultdict(list)
            for childdict in map(self.__fixml_to_dict, children):
                for key, val in childdict.items():
                    defdict[key].append(val)
            ret = {tag: {k: v[0] if len(v) == 1 else v
                           for k, v in defdict.items()}}

        # Set each attribute as a tag key.
        if fixml.attrib:
            ret[tag].update(("@" + k, v)
                              for k, v in fixml.attrib.items())

        # Set the value of each attribute key to the text.
        if fixml.text:
            text = fixml.text.strip()
            if children or fixml.attrib:
                if text:
                  ret[tag]["#text"] = text
            else:
                ret[tag] = text

        # Return the final dictionary.
        return ret

    def __get_fixml(self, ticker, amount, type, account, side, tif, price, sectype):
        fixml = "<FIXML xmlns=\"http://www.fixprotocol.org/FIXML-5-0-SP2\">"
        fixml += "<Order"
        if type != ORDER_TYPE.MARKET and tif is not None:
            fixml += " TmInForce=\"{}\"".format(tif)
        if type != ORDER_TYPE.MARKET:
            fixml += " Px=\"{}\"".format(price)
        fixml += " Typ=\"{}\" Side=\"{}\" Acct=\"{}\">".format(type, side, account)
        fixml += "<Instrmt SecTyp=\"{}\" Sym=\"{}\"/>".format(sectype, ticker)
        fixml += "<OrdQty Qty=\"{}\"/></Order></FIXML>".format(amount)

        return fixml

    def __to_format(self, response, xml=False):
        """A private method to return the API response in the desired format
            @param self - the object pointer
            @param response - response from the Ally Invest API
        """
        if response.status_code != 200:
            if response.status_code == 429:
                print("Too many requests.")
                exit()
            elif response.status_code == 414:
                print("URI too long, please chunk ticker symbols.")
                exit()
        if self.format == "json" and not xml:
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

    def __submit_post(self, url, data, headers={}, usexml=False):
        """A private method to submit a post request to the Ally Invest server
            @param self - the object pointer
            @param url - API URL to access
            @param data - payload for the HTTP request
        """
        self.__create_auth()
        res = requests.post(url, headers=headers, data=data, auth=self.auth)
        return self.__to_format(res, usexml)

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

    def get_orders(self, id):
        """Returns the orders of a specific account (ID = account number)
            @param self - the object pointer
            @param id - account number
        """
        data = self.__get_data(self.url.get_orders().format(id=str(id)))
        if self.format == "json":
          return self.__convert_fixml_json(data)

        return self.__convert_fixml_xml(data)

    def post_order(self, id, fixml):
        """Posts an order and returns the response.
            @param self - the object pointer
            @param id - account number
            @param fixml - FIXML string to send.
        """
        headers = {
            'TKI_OVERRIDE': 'true',
            'Content-Type': 'application/xml',
        }
        # The GET and POST have the same URL.
        url = self.url.get_orders().format(id=str(id))
        return self.__submit_post(url, fixml, headers,
                                  self.format=='xml')

    def post_order_preview(self, id, fixml):
        """Posts an order for preview and returns the response.
            @param self - the object pointer
            @param id - account number
            @param fixml - FIXML string to send.
        """
        headers = {
            'TKI_OVERRIDE': 'true',
            'Content-Type': 'application/xml',
        }
        url = self.url.post_order_preview().format(id=str(id))
        return self.__submit_post(url, fixml, headers,
                                  self.format=='xml')

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

    def __get_option_quote_symbol(self, symbol, exp_date, strike, put_call):
        sym = "{sym}{year}{month:02d}{day:02d}{putcall}{strike}"
        strike = str(int(strike*1000)).zfill(8)
        return sym.format(sym=symbol.upper(), year=str(exp_date.year)[-2:], month=exp_date.month,
                        day=exp_date.day, putcall=put_call.upper(), strike=strike)

    def get_option_quote(self, symbol, expiration_date, strike_price, put_call):
        """Returns a quote for an option for the symbol, expiration date, strike price
            and put/call specifier.

            @param self - object pointer
            @param symbol - underlying stock's ticker symbol
            @param expiration_date - options expiration date
            @param strike_price - option's strike price
            @param put_call - c=call, p=put
        """
        url = self.url.quote_url() + "?symbols={sym}"

        if isinstance(symbol, str): # single ticker
            if not isinstance(expiration_date, datetime.datetime):
                print("In 'get_option_quote': datetime.datetime expected for expiration date.")
                return None
            sym = self.__get_option_quote_symbol(symbol, expiration_date, strike_price, put_call)
        elif isinstance(symbol, list) and isinstance(expiration_date, list) \
            and isinstance(strike_price, list) and isinstance(put_call, list):
            if not isinstance(expiration_date[0], datetime.datetime):
                print("In 'get_option_quote': datetime.datetime expected for expiration date.")
                return None
            request_sym = []
            for i in range(len(symbol)):
                request_sym.append(self.__get_option_quote_symbol(symbol[i], expiration_date[i],
                            strike_price[i], put_call[i]))
            sym = self.__get_symbol_string(request_sym)
        else:
            print("In 'get_option_quote': symbol, expiration_date, strike_price, and put_call \
                  must all be single values or lists.")
            return None

        return self.__get_data(url.format(sym=sym))

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

        return self.__get_data(url.format(syms=self.__get_symbol_string(symbols)))

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

    def get_options(self, symbol):
        url = self.url.options_search_url() + ("?symbol={}".format(symbol))
        return self.__get_data(url)

    def get_options_strikes(self, symbol):
        url = self.url.options_strikes_url() + ("?symbol={}".format(symbol))
        return self.__get_data(url)

    def get_options_expirations(self, symbol):
        url = self.url.options_exps_url() + ("?symbol={}".format(symbol))
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

    def order_common_stock(self, ticker, shares, type, account_nbr, side,
                            time_in_force=None, price=None):
        """Creates an order for common stock (as opposed to options).
            @param self - object pointer
            @param ticker - ticker symbol of the security to purchase
            @param shares - the number of shares to purchase
            @param type - the order type: Market, Limit, Stop, or Stop Limit
                - use the provided enum for these values
            @param account_nbr - the account number for which the shares are to be purchased
            @param side - the side of the trade: Buy or Sell
                - use the provided enum for these values
            @param time_in_force - not applicable for market orders: Day Order, Good til Cancelled, Market on Close
                - use the provided enum for these values
            @param price - the price to purchase the security (only for limit and stop limit orders)
        """
        if price == None and type != ORDER_TYPE.MARKET:
            raise("Price is required for non-market order types.")
        payload = self.__get_fixml(ticker, shares, type, account_nbr, side, time_in_force, price, "CS")
        headers = {
            'TKI_OVERRIDE': 'true',
            'Content-Type': 'application/xml',
        }
        url = self.url.get_post_order().format(id=account_nbr)
        return self.__submit_post(url, payload, headers, True)

class TIME_IN_FORCE:
    DAY = "0"
    GTC = "1"
    MARKET_ON_CLOSE = "7"

class ORDER_TYPE:
    MARKET = "1"
    LIMIT = "2"
    STOP = "3"
    STOP_LIMIT = "4"

class SIDE:
    BUY = "1"
    SELL = "2"
    SELL_SHORT = "5"
