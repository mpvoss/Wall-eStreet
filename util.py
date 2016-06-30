from datetime import datetime, timedelta
import csv

''' Constants ''' 
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 2
MAX_HOLD_TIME_DAYS = 14
LOSS_THRESHOLD_PERCENT = 10
LOSS_THRESHOLD_DOLLARS = 1000


''' Utility methods '''
def getStartTime():
  return datetime.now() - timedelta(days=DATA_TIMEFRAME_DAYS)

def getCurrentTime():
  return datetime.now()

def loadTickers():
  tickers = []
  with open('constituents.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # Cols are Symbol, Name, Sector
      if len(tickers) < MAX_NUM_TICKERS:
        tickers.append(row['Symbol'])
  return tickers

