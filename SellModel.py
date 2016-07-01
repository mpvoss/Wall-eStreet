import numpy
def shouldSell(ticker, data):
  mean = numpy.mean(data['Close'])
  last = data['Close'][-1]

  print(ticker + ": Mean: " + str(mean) + ", current: " + str(last)) 
  return last > mean      
