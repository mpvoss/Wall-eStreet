import numpy

class TrainingStock:
    def __init__(self, ticker, trainingData, validationData):
        self.ticker = ticker
        self.trainingData = trainingData
        self.validationData = validationData

    def setBoughtAt(self, boughtAt):
        self.boughtAt = boughtAt

    def setSoldAt(self, soldAt):
        self.soldAt = soldAt

    def computeReturnPercent(self):
        return (self.soldAt - self.boughtAt) / self.boughtAt

    def printStats(self):
        mean = numpy.mean(self.trainingData)
        last = self.trainingData[-1]
        print("[{:5s}] Mean: {:6.2f}, Current: {:6.2f}".format(self.ticker, mean, last))

    def maxProfit(self):
        start = end = self.trainingData[-1]

        for val in self.validationData:
            end = max(end, val)

        if start == 0:
            return 0
        else:
            return(end - start)/start

    def printDeriv(self):
        mean = numpy.mean(self.trainingData)
        last = self.trainingData[-1]
        return ((last - mean)/mean)

