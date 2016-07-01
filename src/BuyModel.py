import numpy
import AI

def shouldBuy(ai, data):
  mean = numpy.mean(data)
  last = data[-1]
  return ((last - mean)/mean) > ai.buyThreshold     
