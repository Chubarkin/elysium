import unittest

from models import Model, Field
from query import condition
from backends.postgresql.postgresql_builder import PostgreSQLQueryBuilder


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestPostgreSQLQueryBuilder(unittest.TestCase):
    def setUp(self):
        self._query_builder = PostgreSQLQueryBuilder()

    def test_add_tables(self):
        self._query_builder.add_models(TestModel, TestModelTwo)
        self.assertEqual(self._query_builder._models, {TestModel, TestModelTwo})

    def test_add_fields(self):
        self._query_builder.add_fields(TestModel.test_field_one)
        self.assertEqual(self._query_builder._fields, {TestModel.test_field_one})
        # TODO Add exceptions
        self.assertRaises(Exception, self._query_builder.add_fields, 'Not field instance')

    def test_add_conditions(self):
        self._query_builder.add_conditions(TestModel.test_field_one == TestModelTwo.test_field_one)
        self.assertEqual(len(self._query_builder._conditions), 1)
        self.assertIsInstance(self._query_builder._conditions.pop(), condition.Condition)
        self.assertRaises(Exception, self._query_builder.add_conditions, 'Not condition instance')

    def test_add_joined_models(self):
        self._query_builder.add_joined_models(TestModel)
        self.assertEqual(self._query_builder._joined_models, [TestModel])
        self.assertRaises(Exception, self._query_builder.add_joined_models, 'Not model class')

    def test_add_joined_conditions(self):
        self._query_builder.add_joined_conditions(TestModel.test_field_one == TestModelTwo.test_field_one)
        self.assertEqual(len(self._query_builder._joined_conditions), 1)
        self.assertIsInstance(self._query_builder._joined_conditions[0], condition.Condition)
        self.assertRaises(Exception, self._query_builder.add_joined_conditions, 'Not condition instance')

    def test_add_join_types(self):
        self._query_builder.add_join_types(1)
        self.assertEqual(self._query_builder._join_types, [1])

    def test_add_ordering_fields(self):
        self._query_builder.add_ordering_fields(TestModel.test_field_one)
        self.assertEqual(len(self._query_builder._ordering_fields), 0)
        self._query_builder.add_models(TestModel)
        self._query_builder.add_ordering_fields(TestModel.test_field_one)
        self.assertEqual(self._query_builder._ordering_fields, {TestModel.test_field_one})
        self.assertRaises(Exception, self._query_builder.add_ordering_fields, 'Not field instance')
        self._query_builder.add_ordering_fields(TestModelTwo.test_field_one)
        self.assertEqual(self._query_builder._ordering_fields, {TestModel.test_field_one})

    def test_build(self):
        self._query_builder.add_models(TestModel)
        self._query_builder.add_fields(TestModel.test_field_one)
        self._query_builder.add_joined_models(TestModelTwo)
        self._query_builder.add_joined_conditions(TestModel.test_field_one == TestModelTwo.test_field_two)
        self._query_builder.add_fields(TestModelTwo.test_field_one)
        self._query_builder.add_join_types(0)
        self._query_builder.add_conditions(TestModel.test_field_two > 2)
        self._query_builder.add_ordering_fields(TestModelTwo.test_field_two.desc())
        sql_query = self._query_builder.build().rstrip()
        self.assertEqual(sql_query, 'SELECT testmodel.test_field_one, testmodeltwo.test_field_one '
                                    'FROM testmodel '
                                    'INNER JOIN testmodeltwo ON (testmodel.test_field_one = testmodeltwo.test_field_two)  '
                                    'WHERE (testmodel.test_field_two > 2) '
                                    'ORDER BY testmodeltwo.test_field_two DESC')
