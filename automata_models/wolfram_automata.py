import numpy as np
from math import log2
from .binary_rule import BinaryLin3Rule, is_sequence, is_binary

def binary_array_to_string(array):
	if not is_sequence(array):
		raise ValueError('Array is not a sequence.')
	if not all(is_binary(x) for x in array):
		raise ValueError('Array contains non-binary values.')
	return ''.join(str(x) for x in array)

class WolframBinaryAutomata:
	def __init__(self, length, update_rule=None):
		self.cells = np.empty(length, dtype=int)
		self.length = length
		self.dtype = int
		self.rule = update_rule
		if self.rule is None:
			self.rule = BinaryLin3Rule(edge_case=[0, 0])
			self.rule.set_rule_from_int(30)
		self.generation = 0
		self.previous_states = np.array([])

	def get_maximum_initialization_int(self):
		return (2**self.length) - 1

	def clear_history(self):
		self.previous_states = np.array()
		self.generation = 0
		return self

	def set_new_rulerule(self, rule):
		self.rule = rule
		return self

	def log_old_cells_and_clear(self):
		self.previous_states = np.append(self.previous_states, Generation(self.cells, self.rule))
		self.generation += 1
		self.cells = np.empty(self.length, dtype=int)
		return self

	def populate_cells_from_int(self, seed):

		if not 0 < seed <= self.get_maximum_initialization_int():
			raise ValueError('Initialization seed for automata is out of bounds.')

		self.cells = np.zeros(self.length, dtype=int)

		if seed == 0:
			return self

		cur_index = self.length-1
		while seed > 0:
			if seed % 2 == 1:
				self.cells[cur_index] = 1

			seed //= 2
			cur_index -= 1

		return self

	def update_cells_by_rule(self, iterations=1):
		if iterations < 0:
			raise ValueError('Number of iterations must be positive.')
		for i in range(iterations):
			next_cells = self.rule.get_updated_state(self.cells)
			self.log_old_cells_and_clear()
			self.cells = next_cells
		return self



class Generation:
	def __init__(self, cells, rule):
		self.cells = binary_array_to_string(cells)
		self.rule = str(rule)

	def __str__(self):
		return f"[{self.cells} | {str(self.rule)}]"
