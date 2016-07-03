import Scraper
import numpy
import BuyModel
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

    def computeReturn(self, debug, ticker, boughtAt, trainData):
        retVal = 0
        for price in trainData:
            returnVal = util.computeReturn(boughtAt, price)
            if returnVal > self.desiredProfit or returnVal < self.maxLoss:
                retVal = returnVal
                break
        if (retVal == 0):
            retVal = trainData[-1]

        diff = util.computeReturn(boughtAt, trainData[-1])
        if debug:
            print("Bought {} at ${} and sold at ${} for {} return ".format(ticker, boughtAt, retVal, util.prettyPercent(100*diff)))
        return diff

    def analyze(self, stock, debug):
        if BuyModel.shouldBuy(self,stock.trainingData):
            stock.setBoughtAt(stock.trainingData[-1])
            returnVal = self.computeReturn(debug, stock.ticker, stock.trainingData[-1],stock.validationData)
            self.results.append(returnVal)
 
    def train(self,stocks, debug):
        for stock in stocks:
            self.analyze(stock, debug)
        if not self.results:
            self.score = 0
        else:
            self.score = numpy.mean(self.results)

    def printPerformance(self):
        print("AI parameters: maxLoss[{}] desiredProfit[{}] buyThreshold[{}]".format(util.prettyPercent(self.maxLoss), util.prettyPercent(self.desiredProfit), util.prettyPercent(self.buyThreshold)))
        if len(self.results) > 0:
            score = self.score * 100
            print("   %d stocks purchased, average return: %.3f%%" % (len(self.results), score))
        else:
            print("   No stocks purchased. Score: {}".format(self.score))

    def mutate(self):
        # Linear mutation fall off towards end of simulation. Disabled for now
        factor = 1 #- generation / util.MAX_GENERATIONS
        deltaMaxLoss =  util.DELTA_MAX_LOSS * factor
        deltaDesiredProfit = util.DELTA_DESIRED_PROFIT * factor
        deltaBuyThreshold = util.DELTA_BUY_THRESHOLD * factor

        newMaxLoss = util.mutateVal(self.maxLoss, deltaMaxLoss)
        newDesiredProfit = util.mutateVal(self.desiredProfit, deltaDesiredProfit)
        newBuyThreshold = util.mutateVal(self.buyThreshold, deltaBuyThreshold)

        return AI(newMaxLoss, newDesiredProfit, newBuyThreshold)