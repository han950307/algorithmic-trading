from algorithms.algorithms import SimpleAlgorithm


class User(object):
	"""
	So this class holds a collection of stocks
	and can perform various actions, like buy stock etc.
	"""
	def __init__(self):
		# Init these in child classees
		self.buying_power = None
		pass


class SimulatedUser(User):
	"""
	This user can give itself money and fast foward time etc! :o
	"""
	def __init__(self):
		super().__init__()
		pass

	def set_buying_power(self, amount):
		self.buying_power = amount

	
