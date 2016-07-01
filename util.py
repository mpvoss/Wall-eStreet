from datetime import datetime, timedelta
import csv
import os

''' Constants ''' 
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 2
MAX_HOLD_TIME_DAYS = 14
MAX_GENERATIONS = 10
GENERATION_SIZE = 10
DELTA_BUY_THRESHOLD = 0.5
DELTA_MAX_LOSS = 2
DELTA_DESIRED_PROFIT = 2
INIT_BUY_THRESHOLD = 0.5
INIT_DESIRED_PROFIT = 2
INIT_MAX_LOSS = 2



''' Utility methods '''
def getStartTime():
  return datetime.now() - timedelta(days=DATA_TIMEFRAME_DAYS)

def getCurrentTime():
  return datetime.now()

def getDataFile():
  os.listdir()
  #val = os.path.join(os.path.dirname(__file__), '..','data','constituents.csv')
  #print val
  return None


def loadTickers():
  getDataFile()
  tickers = ['LLL']
  return tickers
  with open(getDataFile()) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # Cols are Symbol, Name, Sector
      if len(tickers) < MAX_NUM_TICKERS:
        tickers.append(row['Symbol'])
  return tickers

