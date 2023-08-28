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

	def test_accepts_value(self):
		"""
		Check that the cell accepts a value
		:return:
		"""
		cell = GenericCell()
		cell.set_value("hello")
		assert cell.get_value() == "hello"

		assert cell.accepts_value("pictionary")
		assert not cell.accepts_value(5)

		class SubclassOfString(str): pass

		assert cell.accepts_value(SubclassOfString("hi"))
		cell.set_value(SubclassOfString("hi"))
		assert cell.accepts_value("hey")
