import numpy
import AI
def shouldBuy(ai, data):
  mean = numpy.mean(data)
  last = data[-1]
  #print(last)
  #print(mean)
  #print(str((last - mean)/mean))
  return ((last - mean)/mean) > ai.buyThreshold     
