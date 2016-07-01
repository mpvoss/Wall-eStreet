import numpy
class TrainingStock:
  
  # buy data
  # hold data
  # boughtAt val
  # profit val

  def __init__(self, ticker, analysisData, trainData):
    self.ticker = ticker
    self.analysisData = analysisData
    self.trainData = trainData

  def setBoughtAt(self, boughtAt):
    self.boughtAt = boughtAt

  def setSoldAt(self, soldAt):
    self.soldAt = soldAt

  def computeReturnPercent(self):
    return (self.soldAt - self.boughtAt)/self.boughtAt

  def printStats(self):
    mean = numpy.mean(self.analysisData)
    last = self.analysisData[-1]
    print("[%s] Mean: %.2f, Current: %.2f" % (self.ticker,mean, last))

