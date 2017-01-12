from pandas_datareader import data, wb


def lookup(ticker, start, end):
    return data.DataReader(ticker, 'yahoo', start, end)
