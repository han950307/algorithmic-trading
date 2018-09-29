from abc import ABC
from abc import abstractmethod
import datetime
import os
import re


class Stock(ABC):
	@abstractmethod
	def get_ticker(self):
		pass

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


class Brokerage(ABC):
	"""
	Base class for all stock brokerages.
	This could be a simulated stock brokerage or a real one.
	Brokerages should also be swappable.
	"""
	def __init__(self):
		"""
		"""
		# Please initialize these attributes in the child classes.
		self.stock_flyweight = None
	pass


class SimulatedBrokerage(Brokerage):
	"""
	Use this brokerage to run tests on historical models, etc.
	"""
	class SimulatedStock(Stock):
		def get_ticker(self):
			ticker = os.path.basename(self.stock_file)
			while True:
				res = re.search(r'(.*)\.', ticker)
				if not res:
					break
				ticker = res.group(1)

			return ticker

		def __init__(self, stock_file):
			self.stock_file = stock_file
			self.timestamp = None
			self.history = None
			with open(stock_file) as f:
				pass

	def __init__(self):
		data_folder = '/home/hansung/algorithmic-trading/data/historical/Stocks'
		self.stock_flyweight = StockFlyweight()

		# Want to load all stocks into memory and be able to shuffle later.
		for f in os.listdir(data_folder):
			stock_path = os.path.join(data_folder, f)
			stock = SimulatedBrokerage.SimulatedStock(stock_path)
			self.stock_flyweight.add(stock)


class StockFlyweight(ABC):
	"""
	A holder for all the stocks.
	"""
	def __init__(self):
		self.stock_dict = {}

	def add(self, stock):
		"""
		Given the stock object, adds it to the flyweight.
		"""
		if stock in self.stock_set:
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
			if stock not in self.stock_set:
				raise AttributeError('Ticker "{}" is not in this flyweight!'.format(stock.get_ticker()))

		del self.stock_dict[stock]

	def get(self, ticker):
		"""
		given the ticker, returns the stock object.
		"""
		if ticker not in self.stock_dict:
			raise AttributeError('Ticker "{}" is not in this flyweight!'.format(ticker))
		return self.stock_dict[ticker]
