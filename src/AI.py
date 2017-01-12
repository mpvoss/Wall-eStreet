import Scraper
import numpy
import BuyModel
import util


class AI:
    def __init__(self, max_loss, desired_profit, buy_threshold):
        self.maxLoss = max_loss
        self.desiredProfit = desired_profit
        self.buyThreshold = buy_threshold
        self.results = []
        self.score = 0

    @staticmethod
    def buy_stocks():
        data = {}

        start = util.getStartTime()
        end = util.getCurrentTime()
        tickers = util.load_tickers()

        for ticker in tickers:
            data[ticker] = Scraper.lookup(ticker, start, end)

        for ticker in tickers:
            if BuyModel.should_buy(ticker, data[ticker]):
                print("Buy " + ticker)
            else:
                print("Don't buy " + ticker)

    def reset(self):
        self.results = []
        self.score = 0

    def compute_return(self, debug, ticker, bought_at, train_data):
        ret_val = 0
        for price in train_data:
            return_val = util.compute_return(bought_at, price)
            if return_val > self.desiredProfit or return_val < self.maxLoss:
                ret_val = return_val
                break
        # Didn't sell it due to large gain/loss. Force sale at end of simulation
        if ret_val == 0:
            ret_val = train_data[-1]

        diff = util.compute_return(bought_at, train_data[-1])
        if debug:
            print("Bought {} at ${} and sold at ${} for {} return ".format(ticker, bought_at, ret_val,
                                                                           util.pretty_percent(100 * diff)))
        return diff

    def analyze(self, stock, debug):
        if BuyModel.should_buy(self, stock.trainingData):
            stock.set_bought_at(stock.trainingData[-1])
            return_val = self.compute_return(debug, stock.ticker, stock.trainingData[-1], stock.validationData)
            self.results.append(return_val)

    def train(self, stocks, debug):
        for stock in stocks:
            self.analyze(stock, debug)
        if not self.results:
            self.score = 0
        else:
            self.score = numpy.sum(self.results)

    def print_parameters(self):
        return "AI parameters: maxLoss[{}] desiredProfit[{}] buyThreshold[{}]".format(util.pretty_percent(self.maxLoss),
                                                                                      util.pretty_percent(
                                                                                          self.desiredProfit),
                                                                                      util.pretty_percent(
                                                                                          self.buyThreshold))

    def print_performance(self):
        print(self.print_parameters())
        if len(self.results) > 0:
            score = self.score * 100
            print("   %d stocks purchased, average return: %.3f%%" % (len(self.results), numpy.mean(self.results) * 100))
        else:
            print("   No stocks purchased. Score: {}".format(self.score))

    def mutate(self):
        # Linear mutation fall off towards end of simulation. Disabled for now
        factor = 1  # - generation / util.MAX_GENERATIONS
        delta_max_loss = util.DELTA_MAX_LOSS * factor
        delta_desired_profit = util.DELTA_DESIRED_PROFIT * factor
        delta_buy_threshold = util.DELTA_BUY_THRESHOLD * factor

        new_max_loss = util.mutate_val(self.maxLoss, delta_max_loss)
        new_desired_profit = util.mutate_val(self.desiredProfit, delta_desired_profit)
        new_buy_threshold = util.mutate_val(self.buyThreshold, delta_buy_threshold)

        return AI(new_max_loss, new_desired_profit, new_buy_threshold)
