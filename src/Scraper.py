from pandas_datareader import data, wb
from datetime import datetime
import numpy

def lookup(ticker, start, end):
    # Can use open, close, high, low, volumn, adj close
    return data.DataReader(ticker,  'yahoo', start, end)
