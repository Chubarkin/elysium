import mock
import unittest

from elysium.models import Model, Field
from elysium.query.operand import Operand
from elysium.query.condition import Condition
from elysium.query.operator import Operator


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

    @mock.patch('elysium.query.condition.Condition.to_str')
    @mock.patch('elysium.models.field.Field.to_str')
    def test_to_str(self, field_to_str, condition_to_str):
        condition_to_str.return_value = 'test_condition'
        field_to_str.return_value = 'test_field'

        operand = Operand(Condition(TestModel.test_field_one,
                          TestModel.test_field_two, Operator('=')))
        self.assertEqual(operand.to_str(), 'test_condition')
        self.assertTrue(condition_to_str.called)

        operand = Operand(TestModel.test_field_one)
        self.assertEqual(operand.to_str(), 'test_field')
        self.assertTrue(field_to_str.called)

        operand = Operand(1)
        self.assertEqual(operand.to_str(), '1')

        operand = Operand('1')
        self.assertEqual(operand.to_str(), '"1"')

        operand = Operand(None)
        self.assertEqual(operand.to_str(), '')
