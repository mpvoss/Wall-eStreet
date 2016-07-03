from datetime import datetime
import Scraper
import numpy
import BuyModel
import SellModel
import util


def dropBadStocks():
    # TODO implement
    pass


def sellStocks():
    # TODO implement
    pass


def buyStocks():
    data = {}

    start = util.getStartTime()
    end = util.getCurrentTime()
    tickers = util.loadTickers()

    for ticker in tickers:
        data[ticker] = Scraper.lookup(ticker, start, end)

    for ticker in tickers:
        if BuyModel.shouldBuy(ticker, data[ticker]):
            print("Buy " + ticker)
        else:
            print("Don't buy " + ticker);


def run():
    dropBadStocks()
    sellStocks()
    buyStocks()


run()
