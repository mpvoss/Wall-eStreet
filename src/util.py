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
MAX_GENERATIONS = 10
GENERATION_SIZE = 100
NUM_STOCKS = 500
MAX_HISTORY_DAYS = 365 * 5
TRAIN_TIME_DAYS = 6 * 30

# All percents
#DELTA_MAX_LOSS = 1
#DELTA_DESIRED_PROFIT = 2
#DELTA_BUY_THRESHOLD = 2

#INIT_MAX_LOSS = 2
#INIT_DESIRED_PROFIT = 5
#INIT_BUY_THRESHOLD = 1.1


DELTA_MAX_LOSS = 5
DELTA_DESIRED_PROFIT = 5
DELTA_BUY_THRESHOLD = 5

INIT_MAX_LOSS = 5
INIT_DESIRED_PROFIT = 10
INIT_BUY_THRESHOLD = 0

MUTATE_PROBABILITY = 0.6

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

def printScoreboard(agents):
    print(centerText("Scoreboard start"))
    for agent in agents:
        print(agent.printParameters() + ": score " + str(agent.score))
    print(centerText("Scoreboard end"))


def graphResults(results,optimal):
    plt.plot(results, c='r', ls='-',label="Performance")
    plt.axhline(optimal,0,1, c='b', ls=':', label="Theoretical limit")

    plt.legend(loc='upper left');
    plt.ylabel('Return %')
    plt.xlabel('Generation #')
    print("Optimal: {}".format(optimal))
    plt.show()


def printStockStats(stocks):
    b = [(stock.ticker,  stock.maxProfit(), stock.printDeriv()) for stock in stocks]
    b.sort(key=lambda tup: tup[2])
    for a in b:
        print("{} max prof: {}, deriv: {}".format(a[0], a[1], a[2]))
#test = [1,2,3,4,5,6]
##op = [4 ]
#graphResults(test,op)