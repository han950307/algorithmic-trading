from abc import ABC
from abc import abstractmethod
import random


class Stock(ABC):
    @abstractmethod
    def get_ticker(self):
        pass

    @abstractmethod
    def get_historical_price(self, timestamp):
        """
        Get the price at this time.
        """
        pass

    def get_current_price(self):
        return self.current_price

    def __init__(self):
        """
        """
        # Please initialize these attributes in the child classes.
        self.current_price = None
        self.timestamp = None
        self.history = None
        pass

    def __hash__(self):
        return hash(self.get_ticker())


class StockFlyweight(ABC):
    """
    A holder for all the stocks. This should soon be a singleton class.
    """
    def __init__(self):
        self.stock_dict = {}

    def __iter__(self):
        return iter(self.stock_dict.values())

    def add(self, stock):
        """
        Given the stock object, adds it to the flyweight.
        """
        if stock in self.stock_dict:
            print("INFO: {} is already in this flyweight".format(stock.get_ticker()))
        else:
            self.stock_dict[stock.get_ticker()] = stock

    def remove(self, stock):
        """
        Given the ticker or stock, remove from this flyweight.
        """
        if isinstance(stock, str):
            if stock not in self.stock_dict:
                raise AttributeError('Ticker "{}" is not in this flyweight!'.format(stock))
        else:
            if stock not in self.stock_dict:
                raise AttributeError('Ticker "{}" is not in this flyweight!'.format(stock.get_ticker()))

        del self.stock_dict[stock]

    def get(self, ticker):
        """
        given the ticker, returns the stock object.
        """
        if ticker not in self.stock_dict:
            raise AttributeError('Ticker "{}" is not in this flyweight!'.format(ticker))
        return self.stock_dict[ticker]

    def get_random_stocks(self, quantity=1):
        """
        Returns random stocks
        """
        keys = random.sample(self.stock_dict.keys(), quantity)
        return [self.get(key) for key in keys]
