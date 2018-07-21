import mock
import unittest

from models import Model, Field
from backends.postgresql.postgresql_query import PostgreSQLQuery


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestPostrgreSQLQuery(unittest.TestCase):
    def setUp(self):
        self.query = PostgreSQLQuery()
        self.query._query_builder = mock.patch(
            'backends.postgresql.postgresql_builder.PostgreSQLQueryBuilder').start()

    def test_select(self):
        query = self.query.select()
        self.query._query_builder.add_fields.return_value = None
        self.assertTrue(self.query._query_builder.add_fields.called)
        self.assertEqual(query, self.query)

    def test_filter(self):
        query = self.query.filter(TestModel.test_field_one == TestModel.test_field_two)
        self.query._query_builder.add_conditions.return_value = None
        self.assertTrue(self.query._query_builder.add_conditions.called)
        self.assertEqual(query, self.query)

    @mock.patch('backends.postgresql.postgresql_query.PostgreSQLQuery._join')
    def test_outer_join(self, _join):
        _join.return_value = None
        query = self.query.outer_join(TestModel)
        self.assertTrue(_join.called)
        self.assertEqual(query, self.query)

    @mock.patch('backends.postgresql.postgresql_query.PostgreSQLQuery._join')
    def test_join(self, _join):
        _join.return_value = None
        query = self.query.join(TestModel)
        self.assertTrue(_join.called)
        self.assertEqual(query, self.query)

    @mock.patch('backends.postgresql.postgresql_query.PostgreSQLQuery._join')
    def test_left_join(self, _join):
        _join.return_value = None
        query = self.query.left_join(TestModel)
        self.assertTrue(_join.called)
        self.assertEqual(query, self.query)

    @mock.patch('backends.postgresql.postgresql_query.PostgreSQLQuery._join')
    def test_right_join(self, _join):
        _join.return_value = None
        query = self.query.left_join(TestModel)
        self.assertTrue(_join.called)
        self.assertEqual(query, self.query)

    def test_order_by(self):
        query = self.query.order_by(TestModel.test_field_two)
        self.query._query_builder.add_ordering_fields.return_value = None
        self.assertTrue(self.query._query_builder.add_ordering_fields.called)
        self.assertEqual(query, self.query)
