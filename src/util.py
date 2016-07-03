from datetime import datetime, timedelta
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import Scraper
import random
import TrainingStock
import csv
import os

''' Constants '''
DATA_TIMEFRAME_DAYS = 90
MAX_NUM_TICKERS = 20
MAX_HOLD_TIME_DAYS = 30*12
MAX_GENERATIONS = 50
GENERATION_SIZE = 100
NUM_STOCKS = 500
MAX_HISTORY_DAYS = 365 * 5
TRAIN_TIME_DAYS = 6 * 30

# All percents
DELTA_MAX_LOSS = 10
DELTA_DESIRED_PROFIT = 10
DELTA_BUY_THRESHOLD = 10

INIT_MAX_LOSS = -2
INIT_DESIRED_PROFIT = 2
INIT_BUY_THRESHOLD = 1.1

MUTATE_PROBABILITY = 0.8

''' Utility methods '''
def prettyPercent(val):
    return '{:.3f}%'.format(val)

def getDataFile():
    val = os.path.join(os.path.dirname(__file__), '..', 'data', 'constituents.csv')
    return val

def prettyDate(date):
    return date.strftime("%B %Y")

def getTrainingTimes():
    startTimeframe = random.randrange(MAX_HISTORY_DAYS)
    startSampleTime = datetime.now() - timedelta(startTimeframe)
    endSampleTime = startSampleTime + timedelta(TRAIN_TIME_DAYS)
    startTrainTime = endSampleTime
    endTrainTime = startTrainTime + timedelta(MAX_HOLD_TIME_DAYS)

    return (startSampleTime, endSampleTime, startTrainTime, endTrainTime)

def getTestTrainingTimes():
    trainStart = datetime(2014,1,10)
    trainEnd = trainStart + timedelta(TRAIN_TIME_DAYS)
    validationStart = trainEnd
    validationEnd = validationStart + timedelta(MAX_HOLD_TIME_DAYS)
    return trainStart, trainEnd, validationStart, validationEnd


def loadTrainingStocks(startSampleTime, endSampleTime, startTrainTime, endTrainTime):
    stocks = []
    with open(getDataFile()) as csvfile:
        reader = csv.DictReader(csvfile)
        tickers = [row['Symbol'] for row in reader]
#        tickers = random.sample(tickers, MAX_NUM_TICKERS)
        tickers = tickers[0:MAX_NUM_TICKERS]

        # Cols are Symbol, Name, Sector
        try:
            trainingData = Scraper.lookup(tickers, startSampleTime, endSampleTime)['Close']
            validationData = Scraper.lookup(tickers, startTrainTime, endTrainTime)['Close']
            stocks = [TrainingStock.TrainingStock(company, trainingData[company],validationData[company]) for company in tickers]

        except RemoteDataError:
            print("Error reading stock data, skipping")
    return stocks

def printGreeting():
    print(centerText("-"))
    print(centerTextNoWrap("Wall-e Street Stock Market AI"))
    print(centerText("-"))

def centerText(text):
    return '{:-^80}'.format(text)

def centerTextNoWrap(text):
    return '{:^80}'.format(text)

def printStockInfo(stocks):
    print("\n")
    print(centerTextNoWrap("Stock data used in this experiment"))
    for stock in stocks:
        stock.printStats()

def computeReturn(boughtAt, soldAt):
    return (soldAt - boughtAt) / boughtAt

def loadTickers():
    tickers = []
    with open(getDataFile()) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Cols are Symbol, Name, Sector
            if len(tickers) < MAX_NUM_TICKERS:
                tickers.append(row['Symbol'])
    return tickers

def mutateVal(baseVal, delta):
    if random.random() < MUTATE_PROBABILITY:
        sign = random.choice([-1, 1])
        return sign * random.random() * delta + baseVal
    else:
        return baseVal

def graphResults(results):
    results[:] = [x*100 for x in results]
    plt.plot(results)
    plt.ylabel('Return %')
    plt.xlabel('Generation #')
    plt.show()