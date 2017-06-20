from datetime import datetime, timedelta
from pandas_datareader._utils import RemoteDataError
import matplotlib.pyplot as plt
import Scraper
import random
from Stock import Stock
import TrainingStock
import time
import csv
import os

import DatabaseService

''' Constants '''
DATA_TIME_FRAME_DAYS = 90
MAX_NUM_TICKERS = 500
MAX_HOLD_TIME_DAYS = 30 * 12
MAX_GENERATIONS = 100
GENERATION_SIZE = 40
NUM_STOCKS = 500
MAX_HISTORY_DAYS = 365 * 5
TRAIN_TIME_DAYS = 6 * 30
TRAIN_TIME_YEARS = 4

# All percents
DELTA_MAX_LOSS = 10
DELTA_DESIRED_PROFIT = 10
DELTA_BUY_THRESHOLD = 10

INIT_MAX_LOSS = 3
INIT_DESIRED_PROFIT = 8
INIT_BUY_THRESHOLD = -5

# DELTA_MAX_LOSS = 5
# DELTA_DESIRED_PROFIT = 5
# DELTA_BUY_THRESHOLD = 5
#
# INIT_MAX_LOSS = 5
# INIT_DESIRED_PROFIT = 10
# INIT_BUY_THRESHOLD = 0

MUTATE_PROBABILITY = 0.6

''' Utility methods '''


def pretty_percent(val):
    return '{:.3f}%'.format(val)


def get_data_file():
    val = os.path.join(os.path.dirname(__file__), '..', 'data', 'constituents.csv')
    return val


def pretty_date(date):
    return date.strftime("%B %Y")


def get_training_times():
    start_time_frame = random.randrange(MAX_HISTORY_DAYS)
    start_sample_time = datetime.now() - timedelta(start_time_frame)
    end_sample_time = start_sample_time + timedelta(TRAIN_TIME_DAYS)
    start_train_time = end_sample_time
    end_train_time = start_train_time + timedelta(MAX_HOLD_TIME_DAYS)

    return start_sample_time, end_sample_time, start_train_time, end_train_time


def get_test_training_times():
    train_start = datetime(2000, 1, 10)
    # Offset
    train_start = train_start + timedelta(random.random()*30*12*5)
    train_end = train_start + timedelta(30*12*4)
    return train_start, train_end


def load_training_stocks(start_sample_time, end_sample_time, start_train_time, end_train_time):
    stocks = []
    with open(get_data_file()) as csv_file:
        reader = csv.DictReader(csv_file)
        tickers = [row['Symbol'] for row in reader]
        #        tickers = random.sample(tickers, MAX_NUM_TICKERS)
        tickers = tickers[0:MAX_NUM_TICKERS]

        # Cols are Symbol, Name, Sector
        try:
            training_data = Scraper.lookup(tickers, start_sample_time, end_sample_time)
            validation_data = Scraper.lookup(tickers, start_train_time, end_train_time)['Close']
            stocks = [TrainingStock.TrainingStock(company, training_data[company], validation_data[company]) for company
                      in tickers]

        except RemoteDataError:
            print("Error reading stock data, skipping")
    return stocks


def print_greeting():
    print(center_text("-"))
    print(center_text_no_wrap("Wall-e Street Stock Market AI"))
    print(center_text("-"))


def center_text(text):
    return '{:-^80}'.format(text)


def center_text_no_wrap(text):
    return '{:^80}'.format(text)


def print_stock_info(stocks):
    print("\n")
    print(center_text_no_wrap("Stock data used in this experiment"))
    for stock in stocks:
        stock.printStats()


def compute_return(bought_at, sold_at):
    return (sold_at - bought_at) / bought_at


def load_tickers():
    tickers = []
    with open(get_data_file()) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Cols are Symbol, Name, Sector
            if len(tickers) < MAX_NUM_TICKERS:
                tickers.append(row['Symbol'])
    return tickers


def mutate_val(base_val, delta):
    if random.random() < MUTATE_PROBABILITY:
        sign = random.choice([-1, 1])
        return sign * random.random() * delta + base_val
    else:
        return base_val


def print_scoreboard(agents):
    print(center_text("Scoreboard start"))
    for agent in agents:
        print(agent.print_parameters() + ": score " + str(agent.score))
    print(center_text("Scoreboard end"))


def graph_results(results, optimal):
    plt.plot(results, c='r', ls='-', label="Performance")
    plt.axhline(optimal, 0, 1, c='b', ls=':', label="Theoretical limit")

    plt.legend(loc='upper left');
    plt.ylabel('Return %')
    plt.xlabel('Generation #')
    print("Optimal: {}".format(optimal))
    plt.show()


def print_stock_stats(stocks):
    b = [(stock.ticker, stock.max_profit(), stock.print_deriv()) for stock in stocks]
    b.sort(key=lambda tup: tup[2])
    for a in b:
        print("{} max prof: {}, deriv: {}".format(a[0], a[1], a[2]))
        # test = [1,2,3,4,5,6]
        ##op = [4 ]
        # graphResults(test,op)


def write_output_result(best, optimal):
    f = open("../data/top_strains.csv", 'w+')
    f.write("strain_id,generation,avg_profit\n")
    for strain in best:
        f.write(strain.build_thumbprint() + "\n")
    f.close()


def populate_db():
    session = DatabaseService.setup_db()

    session.add()
    session.commit()


def load_stocks(stocks, start, end):
    start_time = time.time()
    session = DatabaseService.setup_db()
    # in_db = session.query(Stock).filter(Stock.ticker.in_(stocks)).filter(Stock.timestamp >= start).filter(Stock.timestamp <= end).all()

    # removed = []
    # for row in in_db:
    #     if row.ticker not in removed:
    #         stocks.remove(row.ticker)
    #         removed.append(row.ticker)

    if len(stocks) > 0:
        panel = Scraper.lookup(stocks, start, end)
        for date in panel.major_axis:
            for company in panel.minor_axis:
                frame = panel.loc[:, date, company]

                high = frame["High"]
                low = frame["Low"]
                open = frame["Open"]
                close = frame["Close"]
                vol = frame["Volume"]
                adj_close = frame["Adj Close"]
                s = Stock(company, high, low, open, close, vol, adj_close, date)
                if not s.is_nan():
                    session.add(s)
                    # print("{}: high[{}] low[{}] date[{}]".format(stock, hi, low, date))

        session.commit()
    end_time = time.time()
    print("Time taken to load stocks: %s seconds" % (end_time - start_time))


def query_stocks(stocks, start, end):
    session = DatabaseService.setup_db()
    rows = session.query(Stock.ticker, Stock.close, Stock.timestamp).filter(Stock.ticker.in_(stocks)).filter(
        Stock.timestamp >= start).filter(
        Stock.timestamp <= end).order_by(Stock.ticker).order_by(Stock.timestamp.asc()).all()

    ticker = None
    prices = []
    training_stocks = []
    for row in rows:
        if ticker == None:
            ticker = row.ticker
        elif row.ticker != ticker:
            training_stocks.append(
                TrainingStock.TrainingStock(ticker, prices[:len(prices) / 2], prices[len(prices) / 2:]))
            ticker = row.ticker
            prices = []
        else:
            prices.append(row.close)
    training_stocks.append(TrainingStock.TrainingStock(ticker, prices[:len(prices) / 2], prices[len(prices) / 2:]))

    for s in training_stocks:
        s.printStats()

    return training_stocks

# query_stocks(load_tickers(), '2000-01-01', '2000-01-09')
# print("Done")
