import AI
import Scraper
import random
import util
import operator



def mutateVal(baseVal, delta):
  sign = random.choice([-1,1])
  return sign*random.random() * delta + baseVal
    
def mutateAi(starter):
  newMaxLoss = -mutateVal(maxLoss, deltaMaxLoss)
  newDesiredProfit = mutateVal(desiredProfit, deltaDesiredProfit)
  newBuyThreshold = mutateVal(buyThreshold, deltaBuyThreshold)

def loadPopulation(baseline, generation, size):
  samples = []
  factor = 1 - generation/util.MAX_GENERATIONS
  deltaMaxLoss = factor * util.DELTA_MAX_LOSS
  deltaDesiredProfit = factor * util.DELTA_DESIRED_PROFIT
  deltaBuyThreshold = factor * util.DELTA_BUY_THRESHOLD

  for i in range(size):
    newMaxLoss = mutateVal(baseline.maxLoss, deltaMaxLoss)
    newDesiredProfit = mutateVal(baseline.desiredProfit, deltaDesiredProfit)
    newBuyThreshold = mutateVal(baseline.buyThreshold, deltaBuyThreshold)
    samples.append(AI.AI(newMaxLoss, newDesiredProfit, newBuyThreshold))

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
  population += loadPopulation(population[0],generation,size/2)
  population += loadPopulation(population[1],generation,size/2)

  return population

def printTrainingTimes(startSampleTime, endSampleTime,startTrainTime, endTrainTime):
  print("Training time period used: " + util.prettyDate(startSampleTime) + " to " + util.prettyDate(endSampleTime))
  print("Testing time period used: " + util.prettyDate(startTrainTime) + " to " + util.prettyDate(endTrainTime))



def train():
  util.printGreeting()
  population = loadPopulation(loadDefaultAi(), 0,util.GENERATION_SIZE)
  a,b,c,d = util.getTrainingTimes()
  printTrainingTimes(a,b,c,d)
  trainingStocks = util.loadTrainingStocks(a,b,c,d)
  util.printStockInfo(trainingStocks)


  for generation in range(util.MAX_GENERATIONS):

    for sample in population:
      sample.train(trainingStocks)

    population.sort(key=operator.attrgetter('score'), reverse=True)
    printProgress(population,generation)
    population = updatePopulation(population[0:2], generation)    
       
    for sample in population:
      sample.reset()

train()
