import math
import numpy


class TrainingStock:
    def __init__(self, ticker, training_data, validation_data):
        self.ticker = ticker
        self.trainingData = training_data
        self.validationData = validation_data

    def set_bought_at(self, bought_at):
        self.boughtAt = bought_at

    def setSoldAt(self, soldAt):
        self.soldAt = soldAt

    def computeReturnPercent(self):
        return (self.soldAt - self.boughtAt) / self.boughtAt

    def printStats(self):
        mean = numpy.mean(self.trainingData)
        last = self.trainingData[-1]
        print("[{:5s}] Mean: {:6.2f}, Current: {:6.2f}".format(self.ticker, mean, last))

    def max_profit(self):
        start = end = self.trainingData[-1]

        for val in self.validationData:
            end = max(end, val)


        val = 0

        if (start-end) == 0:
            val = 0
        else:
            val = (end - start) / start

        if math.isnan(val):
            print("nan found")


        return val

    def print_deriv(self):
        mean = numpy.mean(self.trainingData)
        last = self.trainingData[-1]
        return (last - mean) / mean

