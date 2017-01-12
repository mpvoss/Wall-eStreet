from datetime import datetime
import Scraper
import numpy
import BuyModel
import SellModel
import util


def drop_bad_stocks():
    # TODO implement
    pass


def sell_stocks():
    # TODO implement
    pass


def buy_stocks():
    data = {}

    start = util.getStartTime()
    end = util.getCurrentTime()
    tickers = util.load_tickers()

    for ticker in tickers:
        data[ticker] = Scraper.lookup(ticker, start, end)

    for ticker in tickers:
        if BuyModel.should_buy(ticker, data[ticker]):
            print("Buy " + ticker)
        else:
            print("Don't buy " + ticker);


def run():
    drop_bad_stocks()
    sell_stocks()
    buy_stocks()


run()
