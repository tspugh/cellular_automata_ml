from unittest import TestCase
from models.automata_models.cell.cell import GenericCell


class TestGenericCell(TestCase):

	def testInit(self):
		"""
		Check instantiation of cells
		:return:
		"""
	cellNone = GenericCell()
	cellNegativePosition = GenericCell(position=-70)
	cellValueNoPos = GenericCell(-23)
	cellValueString = GenericCell("hello, friend")
	cellValueGenericCell = GenericCell(GenericCell("meta"))
	cellValueAndPos = GenericCell('f', 5)

	assert cellNone.get_value() is None
	assert cellNone.position == -1
	assert cellNegativePosition.get_value() is None
	assert cellNegativePosition.position == -1
	assert cellValueNoPos.get_value() == -23
	assert cellValueString.get_value() == "hello, friend"
	assert type(cellValueGenericCell.get_value()) == GenericCell
	assert cellValueGenericCell.get_value().get_value() == "meta"
	assert cellValueAndPos.get_value() == 'f'
	assert cellValueAndPos.position == 5
