from datetime import datetime, timedelta
import Scraper
import random
import TrainingStock
import csv
import os
from pandas_datareader._utils import RemoteDataError

''' Constants ''' 
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 20
MAX_HOLD_TIME_DAYS = 60
MAX_GENERATIONS = 1000
GENERATION_SIZE = 100
NUM_STOCKS = 500
MAX_HISTORY_DAYS = 365 * 5
ANALYSIS_TIME_DAYS = 30 * 6

# Buy thresh already percent
DELTA_MAX_LOSS = 5
DELTA_DESIRED_PROFIT = 2
DELTA_BUY_THRESHOLD = 2

INIT_MAX_LOSS = -2
INIT_DESIRED_PROFIT = 2
INIT_BUY_THRESHOLD = -5


''' Utility methods '''
def getStartTime():
  return datetime.now() - timedelta(days=DATA_TIMEFRAME_DAYS)

def getCurrentTime():
  return datetime.now()

def prettyPercent(val):
  return '{:.3f}%'.format(val)

def getDataFile():
  val = os.path.join(os.path.dirname(__file__), '..','data','constituents.csv')
  return val

def prettyDate(date):
  return date.strftime("%B %Y")

def loadTrainingStocks():
  stocks = []
  startTimeframe = random.randrange(MAX_HISTORY_DAYS)

  startSampleTime = datetime.now() - timedelta(startTimeframe)
  endSampleTime = startSampleTime + timedelta(ANALYSIS_TIME_DAYS)
  startTrainTime = endSampleTime
  endTrainTime = startTrainTime + timedelta(MAX_HOLD_TIME_DAYS)

  print("Training time period used: " + prettyDate(startSampleTime) + " to " + prettyDate(endSampleTime))
  print("Testing time period used: " + prettyDate(startTrainTime) + " to " + prettyDate(endTrainTime))


  with open(getDataFile()) as csvfile:
    reader = csv.DictReader(csvfile)
    rows = []
    for row in reader:
      rows.append(row)

    for i in range(MAX_NUM_TICKERS):
      # Cols are Symbol, Name, Sector
      row = rows[random.randrange(NUM_STOCKS)]
      ticker = row['Symbol']
      try:
        sampleData = Scraper.lookup(ticker, startSampleTime,endSampleTime)['Close']
        trainingData = Scraper.lookup(ticker, startTrainTime,endTrainTime)['Close']
        
        trainingStock = TrainingStock.TrainingStock(ticker, sampleData, trainingData)

        stocks.append(trainingStock)
        trainingStock.printStats()
      except RemoteDataError:
        print("Error reading " + ticker + ", skipping")
  return stocks
  

def computeReturn(boughtAt, soldAt):
  return (soldAt - boughtAt)/boughtAt

def loadTickers():
  tickers = []
  with open(getDataFile()) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # Cols are Symbol, Name, Sector
      if len(tickers) < MAX_NUM_TICKERS:
        tickers.append(row['Symbol'])
  return tickers

