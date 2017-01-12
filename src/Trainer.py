import AI
import util
import operator
import numpy


def load_population(baseline, generation, size):
    samples = []
    for i in range(size):
        samples.append(baseline.mutate())
    return samples


def load_default_ai():
    init_max_loss = util.INIT_MAX_LOSS
    init_desired_profit = util.INIT_DESIRED_PROFIT
    init_buy_threshold = util.INIT_BUY_THRESHOLD

    return AI.AI(init_max_loss, init_desired_profit, init_buy_threshold)


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

    return population


def print_training_times(start_sample_time, end_sample_time, start_train_time, end_train_time):
    print("Training time period used: " + util.pretty_date(start_sample_time) + " to " + util.pretty_date(end_sample_time))
    print("Validation time period used: " + util.pretty_date(start_train_time) + " to " + util.pretty_date(end_train_time))


def train():
    debug = False;
    util.print_greeting()
    population = load_population(load_default_ai(), 0, util.GENERATION_SIZE)

    #    a, b, c, d = util.getTrainingTimes()
    a, b, c, d = util.get_test_training_times()

    print_training_times(a, b, c, d)
    training_stocks = util.load_training_stocks(a, b, c, d)
    util.print_stock_info(training_stocks)

    best = []

    for generation in range(util.MAX_GENERATIONS):
        for sample in population:
            sample.reset()

        for sample in population:
            sample.train(training_stocks, debug)

        population.sort(key=operator.attrgetter('score'), reverse=True)
        #        util.printScoreboard(population)
        print_progress(population, generation)

        population = update_population(population[0:2], generation)

        best.append(numpy.sum(population[0].results))
        # population[0].train(training_stocks,True)

    util.print_stock_stats(training_stocks)

    bestList = [stock.max_profit() for stock in training_stocks]
    print("Best list: ")
    print(bestList)
    optimal = numpy.sum(bestList)
    # util.graph_results(best, optimal)
    util.write_output_result(best, optimal)


train()
