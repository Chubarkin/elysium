import unittest

from models import Model, Field
from query.operand import Operand
from query.condition import Condition
from query.operator import Operator


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestOperand(unittest.TestCase):
    def test_is_condition(self):
        operand = Operand(Condition(TestModel.test_field_one,
                                    TestModel.test_field_two, Operator('=')))
        self.assertTrue(operand.is_condition())
        operand = Operand(TestModel.test_field_one)
        self.assertFalse(operand.is_condition())

    def test_is_field(self):
        operand = Operand(Condition(TestModel.test_field_one,
                                    TestModel.test_field_two, Operator('=')))
        self.assertFalse(operand.is_field())
        operand = Operand(TestModel.test_field_one)
        self.assertTrue(operand.is_field())

    def test_to_str(self):
        operand = Operand(Condition(TestModel.test_field_one,
                          TestModel.test_field_two, Operator('=')))
        self.assertEqual(operand.to_str(), '(testmodel.test_field_one = testmodel.test_field_two)')
        operand = Operand(TestModel.test_field_one)
        self.assertEqual(operand.to_str(), 'testmodel.test_field_one')
        operand = Operand(1)
        self.assertEqual(operand.to_str(), '1')
        operand = Operand('1')
        self.assertEqual(operand.to_str(), '"1"')
        operand = Operand(None)
        self.assertEqual(operand.to_str(), '')
