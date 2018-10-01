from abc import ABC
from abc import abstractmethod

from algorithms.algorithms import SimpleAlgorithm
from brokers.brokers import SimulatedBroker


class Portfolio(ABC):
    """
    Holding stocks! This is just a wrapper to bookkeep the portfolio.
    Does not know how to check for price or anything.
    """
    def __init__(self, stock_flyweight):
        self.portfolio = {}
        self.stock_flyweight = stock_flyweight
    
    def add(self, ticker, quantity):
        """
        Given a ticker, adds it to the portfolio.
        """
        stock = self.stock_flyweight.get(ticker)
        if stock in self.portfolio:
            self.portfolio[stock] += quantity
        else:
            self.portfolio[stock] = quantity

    def get_num_stocks(self, stock):
        """
        Given a ticker or stock, gets the number of it owned.
        """
        if isinstance(stock, str):
            stock = self.stock_flyweight.get(stock)
        if stock not in self.portfolio:
            raise AttributeError('Ticker "{}" is not in this portfolio!'.format(stock.get_ticker()))
        else:
            return self.portfolio[stock]

    def remove(self, stock, quantity):
        """
        Given a ticker or stock, removes it from the portfolio.
        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be an int. Got {}, which is a {}'.format(
                quantity,
                type(quantity)
            ))
        if isinstance(stock, str):
            stock = self.stock_flyweight.get(stock)
        if stock not in self.portfolio:
            raise AttributeError('Ticker "{}" is not in this portfolio!'.format(stock.get_ticker()))
        if self.get_num_stocks(stock) < quantity:
            raise ValueError(
                'Cannot remove more than you have. ' + \
                'You have {} of {} but you are trying to remove {}.'.format(
                    self.get_num_stocks(stock),
                    stock.get_ticker(),
                    quantity
                )
            )
        else:
            self.portfolio[stock] -= quantity

    def get_current_total_value(self):
        value = 0
        for stock, ct in self.portfolio.items():
            value += stock.get_current_price() * ct

        return value


class User(ABC):
    """
    So this class holds a collection of stocks
    and can perform various actions, like buy stock etc.
    """
    def __init__(self, *args, **kwargs):
        # Init these in child classees
        self.buying_power = None
        self.broker = kwargs['broker']
        self.portfolio = Portfolio(self.broker.stock_flyweight)

    @abstractmethod
    def set_buying_power(self):
        """
        """

    @abstractmethod
    def place_buy_order(self, ticker, quantity):
        """
        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be an int. Got {}, which is a {}'.format(
                quantity,
                type(quantity)
            ))
        cur_price = self.broker.get_current_price(ticker)
        tot_price = cur_price * quantity
        if self.buying_power < tot_price:
            print('You do not have enough cash to buy {} orders of {}. You have {}'.format(
                quantity,
                ticker,
                self.buying_power
            ))
            return False

    @abstractmethod
    def place_sell_order(self, ticker, quantity):
        """
        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be an int. Got {}, which is a {}'.format(
                quantity,
                type(quantity)
            ))
        num_stocks = self.portfolio.get_num_stocks(ticker)
        if num_stocks < quantity:
            raise ValueError(
                'Cannot sell more than you have. ' + \
                'You have {} of {} but you are trying to remove {}.'.format(
                    num_stocks,
                    ticker,
                    quantity
                )
            )


class SimulatedUser(User):
    """
    """
    def __init__(self):
        super().__init__(broker=SimulatedBroker())
        self.set_buying_power()

    def set_buying_power(self, buying_power=10000000):
        self.buying_power = buying_power

    def place_buy_order(self, ticker, quantity):
        can_buy = super().place_buy_order(ticker, quantity)
        if can_buy is False:
            return False

        result = self.broker.buy(ticker, quantity)
        money = result['money']
        status = result['status']
        if status is True:
            self.portfolio.add(ticker, quantity)
            self.buying_power -= money

        return status

    def place_sell_order(self, ticker, quantity):
        super().place_sell_order(ticker, quantity)

        result = self.broker.sell(ticker, quantity)

        money = result['money']
        status = result['status']

        if status is 'sold':
            self.buying_power += money
            self.portfolio.remove(ticker, quantity)
            return True
        else:
            return False

class RobinhoodUser(object):
    """
    """
    def __init__(self, broker):
        super().__init__(broker=broker)
