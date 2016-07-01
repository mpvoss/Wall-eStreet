from datetime import datetime, timedelta
import Scraper
import random
import TrainingStock
import csv
import os

''' Constants ''' 
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 20
MAX_HOLD_TIME_DAYS = 60
MAX_GENERATIONS = 100
GENERATION_SIZE = 100
DELTA_BUY_THRESHOLD = 0.05
DELTA_MAX_LOSS = 5
DELTA_DESIRED_PROFIT = 5
INIT_BUY_THRESHOLD = -0.03
INIT_DESIRED_PROFIT = 2
INIT_MAX_LOSS = -2
NUM_STOCKS = 500
MAX_HISTORY_DAYS = 365 * 5
ANALYSIS_TIME_DAYS = 30 * 6

''' Utility methods '''
def getStartTime():
  return datetime.now() - timedelta(days=DATA_TIMEFRAME_DAYS)

def getCurrentTime():
  return datetime.now()

def getDataFile():
  val = os.path.join(os.path.dirname(__file__), '..','data','constituents.csv')
  print val
  return val

def loadTrainingStocks():
  stocks = []
  startTimeframe = random.randrange(MAX_HISTORY_DAYS)

  startSampleTime = datetime.now() - timedelta(startTimeframe)
  endSampleTime = startSampleTime + timedelta(ANALYSIS_TIME_DAYS)
  startTrainTime = endSampleTime
  endTrainTime = startTrainTime + timedelta(MAX_HOLD_TIME_DAYS)


  with open(getDataFile()) as csvfile:
    reader = csv.DictReader(csvfile)
    rows = []
    for row in reader:
      rows.append(row)

    for i in range(MAX_NUM_TICKERS):
      # Cols are Symbol, Name, Sector
      row = rows[random.randrange(NUM_STOCKS)]
      ticker = row['Symbol']
      sampleData = Scraper.lookup(ticker, startSampleTime,endSampleTime)['Close']
      trainingData = Scraper.lookup(ticker, startTrainTime,endTrainTime)['Close']
        
      trainingStock = TrainingStock.TrainingStock(ticker, sampleData, trainingData)

      stocks.append(trainingStock)
      trainingStock.printStats()
    
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

