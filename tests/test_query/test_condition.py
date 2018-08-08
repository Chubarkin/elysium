import mock
import unittest

from elysium import exceptions
from elysium.models import Model, Field
from elysium.query.condition import Condition, ConditionMixin
from elysium.query.operand import Operand
from elysium.query.operator import Operator


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestCondition(unittest.TestCase):
    def setUp(self):
        self.condition = Condition(TestModel.test_field_one, TestModelTwo.test_field_two, Operator('='))

    @mock.patch('elysium.query.operand.Operand.to_str')
    def test_to_str(self, to_str):
        to_str.return_value = 'testmodel.test_field_one'
        self.assertEqual(self.condition.to_str(), '(testmodel.test_field_one = testmodel.test_field_one)')

    @mock.patch('elysium.query.condition.Condition._get_models')
    def test_get_models(self, _get_models):
        self.condition.get_models()
        self.assertEqual(_get_models.call_count, 1)

    @mock.patch('elysium.query.operand.Operand.is_condition')
    def test__get_models(self, is_condition):
        is_condition.return_value = True
        self.assertRaises(AttributeError, self.condition._get_models, Operand(self.condition))
        is_condition.return_value = False
        models = self.condition._get_models(Operand(TestModel.test_field_one))
        self.assertEqual(models, {TestModel})

    @mock.patch('elysium.query.condition.operators')
    def test__validate(self, _operators):
        _operators.AND = Operator('TEST_AND')
        self.assertRaises(exceptions.ConditionError, self.condition._validate,
                          TestModelTwo.test_field_one, TestModelTwo.test_field_two, _operators.AND)


class TestConditionMixin(unittest.TestCase):
    def setUp(self):
        self.first_instance = ConditionMixin()
        self.second_instance = ConditionMixin()
        self.operators_patch = mock.patch('elysium.query.condition.operators')
        self.operators = self.operators_patch.start()
        self.validate_patch = mock.patch('elysium.query.condition.Condition._validate')
        validate = self.validate_patch.start()
        validate.return_value = True

    def tearDown(self):
        self.operators_patch.stop()
        self.validate_patch.stop()

    def test_eq(self):
        self.operators.EQ = Operator('TEST_EQ')
        condition = self.first_instance == self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.EQ)

    def test_ne(self):
        self.operators.EQ = Operator('TEST_NE')
        condition = self.first_instance != self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.NE)

    def test_and(self):
        self.operators.AND = Operator('TEST_AND')
        condition = self.first_instance & self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.AND)

    def test_or(self):
        self.operators.AND = Operator('TEST_OR')
        condition = self.first_instance | self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.OR)

    def test_ge(self):
        self.operators.EQ = Operator('TEST_GE')
        condition = self.first_instance >= self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.GE)

    def test_gt(self):
        self.operators.EQ = Operator('TEST_GT')
        condition = self.first_instance > self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.GT)

    def test_le(self):
        self.operators.EQ = Operator('TEST_LE')
        condition = self.first_instance <= self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.LE)

    def test_lt(self):
        self.operators.EQ = Operator('TEST_LT')
        condition = self.first_instance < self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.LT)

    def test_contains(self):
        self.operators.IN = Operator('TEST_IN')
        condition = self.first_instance.contains([1, 2, 3])
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.IN)

    def test_is_null(self):
        self.operators.IS_NULL = Operator('TEST_IS_NULL')
        condition = self.first_instance.is_null()
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.IS_NULL)

    def test_is_not_null(self):
        self.operators.IS_NULL = Operator('TEST_IS_NOT_NULL')
        condition = self.first_instance.is_not_null()
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition._operator, self.operators.IS_NOT_NULL)
