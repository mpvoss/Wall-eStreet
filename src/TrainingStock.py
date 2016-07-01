import numpy
import sys
class TrainingStock:
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
    print("[{:5s}] Mean: {:6.2f}, Current: {:6.2f}".format(self.ticker,mean, last))
   

