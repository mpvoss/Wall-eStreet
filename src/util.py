from datetime import datetime, timedelta
import Scraper
import TrainingStock
import csv
import os

''' Constants ''' 
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 20
MAX_HOLD_TIME_DAYS = 14
MAX_GENERATIONS = 10
GENERATION_SIZE = 10
DELTA_BUY_THRESHOLD = 0.01
DELTA_MAX_LOSS = 2
DELTA_DESIRED_PROFIT = 2
INIT_BUY_THRESHOLD = 0.05
INIT_DESIRED_PROFIT = 2
INIT_MAX_LOSS = -2

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
  startSampleTime = datetime.now() - timedelta(104)
  endSampleTime = datetime.now() - timedelta(14)
  startTrainTime = datetime.now() - timedelta(14)
  endTrainTime = datetime.now()

  with open(getDataFile()) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      # Cols are Symbol, Name, Sector
      if len(stocks) < MAX_NUM_TICKERS:
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

