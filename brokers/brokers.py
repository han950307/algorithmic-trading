from abc import ABC
from abc import abstractmethod
import datetime
import os
import re

from brokers.stock import (
    Stock,
    StockFlyweight
) 


class Broker(ABC):
    """
    Base class for all stock Brokers.
    This could be a simulated stock Broker or a real one.
    Brokers should also be swappable.
    """
    def __init__(self):
        """
        """
        # Please initialize these attributes in the child classes.
        self.stock_flyweight = None

    @abstractmethod
    def buy(self, *args, **kwargs):
        """
        Given a ticker or a stock object, buys the stock for you.
        """
        pass

    @abstractmethod
    def sell(self, *args, **kwargs):
        """
        Given a ticker or a stock object with quantity, sells the stocks for you.
        """
        pass

    def get_current_price(self, ticker):
        """
        Given a ticker, returns the current market price.
        """
        stock = self.stock_flyweight.get(ticker)
        return stock.get_current_price()

    def get_historical_price(self, ticker, timestamp):
        """
        Given a ticker, returns the historical price at the timestamp.
        """
        stock = self.stock_flyweight.get(ticker)
        return stock.get_historical_price(timestamp)

    def get_random_stock(self):
        return self.stock_flyweight.get_random_stocks()[0]


class SimulatedBroker(Broker):
    """
    Use this Broker to run tests on historical models, etc.
    """
    class SimulatedStock(Stock):
        def __init__(self, stock_file):
            super().__init__()
            self.stock_file = stock_file
            self.timestamp = None
            self.history = {}
            with open(stock_file) as f:
                beg = True
                for l in f:
                    if beg is True:
                        beg = False
                        continue
                    sp = l.split(",")
                    dt_str = sp[0]
                    open_price = float(sp[1])
                    high = float(sp[2])
                    low = float(sp[3])
                    close_price = float(sp[4])
                    volume = int(sp[5])
                    dt_open = datetime.datetime.strptime('{} 9:30AM'.format(dt_str), '%Y-%m-%d %I:%M%p')
                    dt_close = datetime.datetime.strptime('{} 4:00PM'.format(dt_str), '%Y-%m-%d %I:%M%p')
                    self.history[dt_open] = open_price
                    self.history[dt_close] = close_price

        def get_ticker(self):
            """
            Returns the ticker string of this stock.
            """
            ticker = os.path.basename(self.stock_file)
            while True:
                res = re.search(r'(.*)\.', ticker)
                if not res:
                    break
                ticker = res.group(1)

            return ticker

        def get_historical_price(self, timestamp):
            """
            Given the timestamp, returns the historical price.
            If it does not exist, return None
            """
            # Normalize because we do it in minute chunks in the simulation.
            timestamp -= datetime.timedelta(seconds=timestamp.second)
            timestamp -= datetime.timedelta(microseconds=timestamp.microsecond)

            if timestamp in self.history:
                return self.history[timestamp]
            else:
                ct = 0
                while timestamp not in self.history and ct < 14400:
                    # Get the last timestamp on record
                    timestamp = timestamp + datetime.timedelta(minutes=-1)
                    ct += 1
                if timestamp in self.history:
                    return self.history[timestamp]
                else:
                    return None

        def revert_price_to(self, timestamp):
            """
            Given a datetime object, reverts the stock's state to this time.
            """
            price = self.get_historical_price(timestamp)
            if price:
                self.timestamp = timestamp
                self.current_price = price
            else:
                self.timestamp = None
                self.current_price = None

    def __init__(self):
        super().__init__()
        data_folder = '/home/hansung/algorithmic-trading/data/historical/Stocks'
        self.stock_flyweight = StockFlyweight()

        # Want to load all stocks into memory and be able to shuffle later.
        ct = 0
        for f in os.listdir(data_folder):
            stock_path = os.path.join(data_folder, f)
            stock = SimulatedBroker.SimulatedStock(stock_path)
            self.stock_flyweight.add(stock)
            ct += 1
            if ct % 50 == 0:
                print(ct)
                break

    def set_day(self, timestamp):
        for stock in self.stock_flyweight:
            stock.revert_price_to(timestamp)

    def buy(self, ticker, quantity):
        # Haha, simulated buying
        stock = self.stock_flyweight.get(ticker)
        return {
            'money': stock.get_current_price() * quantity,
            'status': True
        }

    def sell(self, ticker, quantity):
        # also, haha simulated selling
        stock = self.stock_flyweight.get(ticker)
        return {
            'money': stock.get_current_price() * quantity,
            'status': 'sold'
        }
