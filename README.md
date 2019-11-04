# AllyInvest.py
A blackbox Ally Invest/TradeKing API interface for application developers.

AllyAPI.py
A Python3 class that allows access to all of the functionality in the
Ally/TradeKing API.

This package attempts to stay on top of changes to the API and allow an
easy to user interface with the Ally Invest API. The API does no formatting
for the user. A response format of 'xml' or 'json' can be specified and
the API responses will be returned as the raw XML or JSON, respectively.

This API was built with the developer in mind and should allow a developer
to build applications around the Ally Invest API without having to deal with
accessing and managing the requests and responses.

# Documentation

Doxygen was used to generate documentation for this interface. The generated
documentation can be found [here](http://www.anthonymorast.com/allyinvestapi/).

Perhaps the most useful documentation is of the [AllyAPI class](http://www.anthonymorast.com/allyinvestapi/classally_1_1_ally_a_p_i.html)
as this documentation shows which functionality is available and describes how to
use each function.

# Usage

Details coming soon. Some basic usage can be found in example.py until then.

# TODO
+ Documentation
  + URLs.py and examples.py
+ Implement missing functionality
  + Right now, the API implements many of the calls listed on [Ally's documentation page](https://www.ally.com/api/invest/documentation/)
    but there are many not yet implemented (due to time constraints). Below is a list.
  + Adding the functionality is pretty straight forward, some more details are below.
+ Test
  + Everything
  + Add unit tests

## Adding New API Functionality

To add a new API function the API URL has to be added to the URLs class in URLs.py.
Note that the request endpoint is already stored in the class e.g.

> https://api.tradeking.com/v1/

Therefore, only anything after */v1/* needs to be added as a URL. A method to
obtain the full URL must be implemented as well, examples abound in the URLs class.

After the URL is added, implementing the POST or GET is very simple. There are two
private methods in the *AllyAPI* class that allow easily retrieving data provided
only the URL. these are *__get_data(self, url)* and *__to_format(self, response)*.

To add the new functionality, just create a method call in the *AllyAPI* class that
uses your new URL and returns/calls the *__get_date(...)* method. This will return the
raw XML or JSON response from the user depending on the format set up when creating
the *AllyAPI* class instance.

## Missing Functionality
+ ORDER/TRADE
    + GET accounts/:id/orders
    + POST accounts/:id/orders
    + POST accounts/:id/orders/preview
+ MARKET
    + GET market/options/search
    + GET market/options/strikes
    + GET market/options/expirations
    + GET market/timesales
+ WATCHLIST
    + GET watchlists
    + POST watchlists
    + GET watchlists/:id
    + DELETE watchlists/:id
    + POST watchlists/:id/symbols
    + DELETE watchlists/:id/symbols
+ STREAMING OPERATIONS
    + MARKET
        + GET market/quotes
