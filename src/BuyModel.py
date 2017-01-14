import numpy
import AI


def should_buy(ai, data):
    mean = numpy.mean(data)
    last = data[-1]
    return ((last - mean) / mean) > ai.buy_threshold
