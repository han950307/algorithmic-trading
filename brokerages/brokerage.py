from abc import ABC


class Brokerage(ABC):
	"""
	Base class for all stock brokerages.
	This could be a simulated stock brokerage or a real one.
	Brokerages should also be swappable.
	"""
