import AI
import util
import operator
import numpy
import TrainingStock

def loadPopulation(baseline, generation, size):
    samples = []
    for i in range(size):
        samples.append(baseline.mutate())
    return samples

def loadDefaultAi():
    initMaxLoss = util.INIT_MAX_LOSS
    initDesiredProfit = util.INIT_DESIRED_PROFIT
    initBuyThreshold = util.INIT_BUY_THRESHOLD

    return AI.AI(initMaxLoss, initDesiredProfit, initBuyThreshold)

def printProgress(population, count):
    print(util.centerText("Generation " + str(count)))
    population[0].printPerformance()
    population[1].printPerformance()
    # Uncomment to see the worst in each batch, ensure someone is losing money
    # population[util.GENERATION_SIZE-1].printPerformance()

def updatePopulation(population, generation):
    size = util.GENERATION_SIZE - len(population)
    population += loadPopulation(population[0], generation, size / 3)
    population += loadPopulation(population[1], generation, size / 3)
    population += loadPopulation(loadDefaultAi(), generation, size / 3)

    return population

def printTrainingTimes(startSampleTime, endSampleTime, startTrainTime, endTrainTime):
    print("Training time period used: " + util.prettyDate(startSampleTime) + " to " + util.prettyDate(endSampleTime))
    print("Validation time period used: " + util.prettyDate(startTrainTime) + " to " + util.prettyDate(endTrainTime))

def train():
    util.printGreeting()
    population = loadPopulation(loadDefaultAi(), 0, util.GENERATION_SIZE)

#    a, b, c, d = util.getTrainingTimes()
    a, b, c, d = util.getTestTrainingTimes()

    printTrainingTimes(a, b, c, d)
    trainingStocks = util.loadTrainingStocks(a, b, c, d)
    util.printStockInfo(trainingStocks)

    best = []

    for generation in range(util.MAX_GENERATIONS):
        for sample in population:
            sample.reset()

        for sample in population:
            sample.train(trainingStocks, False)

        population.sort(key=operator.attrgetter('score'), reverse=True)
#        util.printScoreboard(population)
        printProgress(population, generation)

        population = updatePopulation(population[0:2], generation)

        best.append(numpy.sum(population[0].results))
        #population[0].train(trainingStocks,True)

    util.printStockStats(trainingStocks)

    util.graphResults(best, numpy.sum([stock.maxProfit() for stock in trainingStocks]))

train()
