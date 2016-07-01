from datetime import datetime
import Scraper
import numpy
import BuyModel
import SellModel
import util
 

class AI:
  def __init__(self, maxLoss, desiredProfit, buyThreshold):
    self.maxLoss = maxLoss
    self.desiredProfit = desiredProfit
    self.buyThreshold = buyThreshold
    self.results = []
    self.score = 0

  def buyStocks(self):
    data = {}

    start = util.getStartTime()
    end = util.getCurrentTime()
    tickers = util.loadTickers()

    for ticker in tickers:
      data[ticker] = Scraper.lookup(ticker, start, end)

    for ticker in tickers:
      if BuyModel.shouldBuy(ticker, data[ticker]):
        print("Buy " + ticker)
      else:
        print("Don't buy " + ticker);

  def reset(self):
    self.results = []
    self.score = 0

  def computeReturn(self, boughtAt, trainData):
    for price in trainData:
      returnVal = util.computeReturn(boughtAt, price)
      #print("return val: " + str(returnVal) + ", desProf " + str(self.desiredProfit) + ", maxLoss: " + str(self.maxLoss))
      if returnVal > self.desiredProfit or returnVal < self.maxLoss:
        #print("Sold at " + str(price))
        return returnVal
    #print("kept until the end")
    return util.computeReturn(boughtAt, trainData[-1])

  def analyze(self, stock):
    if BuyModel.shouldBuy(self,stock.analysisData):
      stock.setBoughtAt(stock.analysisData[-1])
      returnVal = self.computeReturn(stock.analysisData[-1],stock.trainData)
      self.results.append(returnVal)
 
  def train(self,stocks):
    for stock in stocks:
      self.analyze(stock)
    self.score = numpy.mean(self.results)

  def printPerformance(self):
    print("maxLoss: %.3f, desiredProfit: %.3f, buyThreshold: %.3f" % (self.maxLoss, self.desiredProfit, self.buyThreshold))
    if len(self.results) > 0:
      print("   %d stocks purchased, average return: %.3f" % (len(self.results), self.score))
    else:
      print("   No stocks purchased.")

  def dropBadStocks(self):
    #TODO implement
    pass

  def sellStocks(self):
    #TODO implement
    pass 


