import mock
import unittest

from elysium.models import Model, Field
from elysium.backends.postgresql import operators
from elysium.factory.postgres_factory import PostgresFactory
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

    def test_to_str(self):
        self.assertEqual(self.condition.to_str(), '(testmodel.test_field_one = testmodeltwo.test_field_two)')

    def test_get_models(self):
        models = self.condition.get_models()
        self.assertEqual(models, {TestModel, TestModelTwo})

    def test__get_models(self):
        models = self.condition._get_models(Operand(self.condition))
        self.assertEqual(models, {TestModel, TestModelTwo})

    @mock.patch('elysium.factory.factory', PostgresFactory())
    def test__validate(self):
        self.assertRaises(Exception, self.condition._validate,
                          TestModelTwo.test_field_one, TestModelTwo.test_field_two, operators.AND)


@mock.patch('elysium.factory.factory', PostgresFactory())
class TestConditionMixin(unittest.TestCase):
    def setUp(self):
        self.first_instance = ConditionMixin()
        self.second_instance = ConditionMixin()
        self.template = '(%s %s %s)'

    def test_eq(self):
        condition = self.first_instance == self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.EQ.string_repr, self.second_instance))

    def test_ne(self):
        condition = self.first_instance != self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.NE.string_repr, self.second_instance))

    def test_and(self):
        with self.assertRaises(Exception):
            self.first_instance & self.second_instance

    def test_or(self):
        with self.assertRaises(Exception):
            self.first_instance | self.second_instance

    def test_ge(self):
        condition = self.first_instance >= self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.GE.string_repr, self.second_instance))

    def test_gt(self):
        condition = self.first_instance > self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.GT.string_repr, self.second_instance))

    def test_le(self):
        condition = self.first_instance <= self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.LE.string_repr, self.second_instance))

    def test_lt(self):
        condition = self.first_instance < self.second_instance
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.LT.string_repr, self.second_instance))

    def test_contains(self):
        condition = self.first_instance.contains([1, 2, 3])
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % ([1, 2, 3], operators.IN.string_repr, self.first_instance))

    def test_is_null(self):
        condition = self.first_instance.is_null()
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.IS_NULL.string_repr, ''))

    def test_is_not_null(self):
        condition = self.first_instance.is_not_null()
        self.assertIsInstance(condition, Condition)
        self.assertEqual(condition.to_str(),
                         self.template % (self.first_instance, operators.IS_NOT_NULL.string_repr, ''))
