from typing import Generic, TypeVar, Any

from models.automata_models.error_types import NoneCellException

# generic type for GenericCell
T = TypeVar("T")


class GenericCell(Generic[T]):

	def __init__(self, value: T = None, position: int = -1) -> None:
		"""

		:param value:
			The value that the cell holds
		:param position:
			The position assigned to the cell.
			Can be used in graphs to signify node number.
			Defaults to -1 when empty or < 0
		"""
		self._value = value
		if position < 0:
			self.position = -1
		else:
			self.position = position

	def get_value(self) -> T:
		"""
		Getter for the cell's value
		:return:
		"""
		return self._value

	def set_value(self, value: T) -> bool:
		"""
		Setter for the cell's value.
		Returns false if the assignment was incompatible
		:param value: The new value for the cell
		:return: Whether the value was accepted
		"""
		if self._value is None or self.accepts_value(value):
			self._value = value
			return True
		return False

	def accepts_value(self, value: Any) -> bool:
		"""
		Returns whether the cell can 'admit' a certain value to contain.
		:param value: The value being tested
		:return: Whether the value was accepted
		"""

		# This version just checks for class relation between the two
		return (
				isinstance(self._value, type(value)) or
				isinstance(value, type(self._value))
		)

	def __str__(self) -> str:
		"""
		The string representation of a GenericCell
		:return: a string with the type and value of the GenericCell
		"""
		return f"GenericCell<{T}>({self._value})"

	def __bool__(self) -> bool:
		"""
		A boolean representing if the cell has a value
		:return: bool
		"""
		return self._value is not None

	def __check_and_raise_none_error(self, other: Any) -> None:
		"""
		Raises a NoneCellException if self or other hold any None values
		:param other:
		:return: None
		"""
		if self._value is None:
			raise NoneCellException(
				"Cannot compare values with None-valued GenericCell")
		if other is None or (
				isinstance(other, GenericCell) and other.get_value() is None
		):
			raise NoneCellException(
				"Cannot compare GenericCells with None value")

	def __eq__(self, other: Any) -> bool:
		"""
		Determines equality of a cell and the value 'other'. If both are cells,
		compare their internal values.
		If self._value is a subtype of other's class or vice-versa,
		use the pre-existing comparison method.
		Otherwise, return False

		:param other:
			The object to be compared
		:return:
			A boolean whether the objects or values are equivalent
		"""
		self.__check_and_raise_none_error(other)

		if isinstance(other, GenericCell):
			return self._value == other.get_value()
		if self.accepts_value(other):
			return self._value == other
		return False

	def __lt__(self, other: Any) -> bool:
		"""
		Determines if 'other' is less than this cell's value

		:param other:
			The object to be compared
		:return:
			A boolean whether 'other' is less than this cell's value
		"""
		self.__check_and_raise_none_error(other)

		if (
				isinstance(other, GenericCell) and
				self.accepts_value(other.get_value())
		):
			return self._value > other.get_value()
		if self.accepts_value(other):
			return self._value > other
		raise ValueError(
			f"Incompatible comparison of {type(other)} with a GenericCell of type {T}")

	def __gt__(self, other: Any) -> bool:
		"""
		Determines if 'other' is greater than this cell's value

		:param other:
			The object to be compared
		:return:
			A boolean whether 'other' is greater than this cell's value
		"""

		self.__check_and_raise_none_error(other)

		if (
				isinstance(other, GenericCell) and
				self.accepts_value(other.get_value())
		):
			return self._value < other.get_value()
		if self.accepts_value(other):
			return self._value < other
		raise ValueError(
			f"Incompatible comparison of {type(other)} with a GenericCell of type {T}")

	def __le__(self, other: Any) -> bool:
		"""
		Determines if 'other' is less than or equal to this cell's value

		:param other:
			The object to be compared
		:return:
			A boolean whether 'other' is less than or equal to this cell's value
		"""

		self.__check_and_raise_none_error(other)

		if(
			isinstance(other, GenericCell) and
			self.accepts_value(other.get_value())
		):
			return self._value >= other.get_value()
		if self.accepts_value(other):
			return self._value >= other
		raise ValueError(
			f"Incompatible comparison of {type(other)} with a GenericCell of type {T}")

	def __ge__(self, other: Any) -> bool:
		"""
		Determines if 'other' is greater than or equal to this cell's value

		:param other:
			The object to be compared
		:return:
			A boolean whether 'other' is >= to this cell's value
		"""
		self.__check_and_raise_none_error(other)

		if (
				isinstance(other, GenericCell) and
				self.accepts_value(other.get_value())
		):
			return self._value <= other.get_value()
		if self.accepts_value(other):
			return self._value <= other
		raise ValueError(
			f"Incompatible comparison of {type(other)} with a GenericCell of type {T}")
