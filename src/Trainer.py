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

def train():
  initMaxLoss = util.INIT_MAX_LOSS
  initDesiredProfit = util.INIT_DESIRED_PROFIT
  initBuyThreshold = util.INIT_BUY_THRESHOLD
  
  population = loadPopulation(AI.AI(initMaxLoss, initDesiredProfit, initBuyThreshold), 0,util.GENERATION_SIZE)
  trainStocks = util.loadTrainingStocks()

  for generation in range(util.MAX_GENERATIONS):
    for sample in population:
      sample.train(trainStocks)


    population.sort(key=operator.attrgetter('score'), reverse=True)
    population = population[0:2]
    population[0].printPerformance()
    population[1].printPerformance()
    print("---------- Generation " + str(generation) + " ----------")
    
    size = util.GENERATION_SIZE - len(population)
    population += loadPopulation(population[0],generation,size/2)
    population += loadPopulation(population[0],generation,size/2)
       
    for sample in population:
      sample.reset()


train()
