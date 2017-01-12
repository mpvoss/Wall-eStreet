import numpy


def should_sell(ticker, data):
    mean = numpy.mean(data['Close'])
    last = data['Close'][-1]

    return last > mean
