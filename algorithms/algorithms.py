from abc import ABC


class Algorithm(ABC):
	"""
	Base class for all stock trading algorithms.
	The idea is when we instantiate a stock trading service,
	we can pass in a trading algorithm as an argument and it would be
	swappable.
	"""
	pass


class SimpleAlgorithm(Algorithm):
	"""
	Very basic algorithm for trading stock.
	"""
