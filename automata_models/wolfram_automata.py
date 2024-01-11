import numpy as np
from math import log2

class WolframBinaryAutomata:
	def __init__(self, length, update_rule=None):
		self.cells = np.empty(length, dtype=int)
		self.length = length
		self.dtype = int
		self.rule = update_rule

	def get_maximum_initialization_int(self):
		return (2**self.length) - 1

	def populate_cells_from_int(self, seed):
		if not 0 < seed <= self.get_maximum_initialization_int():
			raise ValueError('Initialization seed for automata is out of bounds.')

		self.cells = np.zeros(self.length)

		if seed == 0:
			return self

		cur_index = 0
		while seed > 0:
			if seed % 2 == 1:
				self.cells[cur_index] = 1

			seed //= 2
			cur_index += 1

		return self

	def