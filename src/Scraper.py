from pandas_datareader import data, wb
from datetime import datetime
import numpy

def lookup(ticker, start, end):
    return data.DataReader(ticker,  'yahoo', start, end)
