import random

import AI
import util
import operator
import numpy
import copy
import cProfile


def load_population(baseline, generation, size):
    samples = []
    for i in range(size):
        samples.append(baseline.mutate(generation))
    return samples


def load_default_ai():
    init_max_loss = util.INIT_MAX_LOSS
    init_desired_profit = util.INIT_DESIRED_PROFIT
    init_buy_threshold = util.INIT_BUY_THRESHOLD

    return AI.AI(init_max_loss, init_desired_profit, init_buy_threshold, 0)


def print_progress(population, count):
    print(util.center_text("Generation " + str(count)))
    population[0].print_performance()
    population[1].print_performance()

    # Uncomment to see the worst in each batch, ensure someone is losing money
    # population[util.GENERATION_SIZE-1].printPerformance()


def update_population(population, generation):
    size = util.GENERATION_SIZE - len(population)
    population += load_population(population[0], generation, size / 3)
    population += load_population(population[1], generation, size / 3)
    population += load_population(load_default_ai(), generation, size / 3)

    population[0].generation = generation
    population[1].generation = generation

    return population


def print_training_times(start_sample_time, end_sample_time):
    print(
        "Training time period used: " + util.pretty_date(start_sample_time) + " to " + util.pretty_date(
            end_sample_time))




def train():
    debug = False;
    util.print_greeting()
    population = load_population(load_default_ai(), 0, util.GENERATION_SIZE)

    train_start, train_end = util.get_test_training_times()

    training_stocks = util.query_stocks(random.sample(util.load_tickers(), 20), train_start, train_end)

    best = []

    for generation in range(util.MAX_GENERATIONS):
        for sample in population:
            sample.reset()

        for sample in population:
            sample.train(training_stocks, debug)

        population.sort(key=operator.attrgetter('score'), reverse=True)
        #        util.printScoreboard(population)
        print_progress(population, generation)

        top = [ai for ai in population if ai.score == population[0].score]
        if len(top) == 1:
            top.append(population[1])

        population = update_population(random.sample(top, 2), generation)

        best.append(copy.deepcopy(population[0]))

    best_list = [stock.max_profit() for stock in training_stocks]
    optimal = numpy.sum(best_list)

    util.write_output_result(best, optimal)

    util.print_stock_info(training_stocks)

    print_training_times(train_start, train_end)
    print("Gen 1 score: %s, Last gen score: %s" % (best[0].score, best[-1].score))

    return best[-1].report(training_stocks)


info = []
for i in range(1):
    info.append(train())

for line in info:
    print(line)
