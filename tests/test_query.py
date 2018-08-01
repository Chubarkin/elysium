import mock
import unittest

from models import Model, Field
from backends.postgresql.query import PostgreSQLQuery
from query.constants import SELECT_QUERY_TYPE


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestPostrgreSQLQuery(unittest.TestCase):
    prefix = 'backends.postgresql.builder.PostgreSQLSelectQueryBuilder.'

    def setUp(self):
        self.query = PostgreSQLQuery(SELECT_QUERY_TYPE)

    @mock.patch(prefix + 'add_fields')
    @mock.patch(prefix + 'add_models_from_fields')
    def test_select(self, add_models_from_fields, add_fields):
        self._query = PostgreSQLQuery(0)
        query = self.query.select()
        add_fields.return_value = None
        self.assertTrue(add_fields.called)
        self.assertTrue(add_models_from_fields.called)
        self.assertIs(query, self.query)

    @mock.patch(prefix + 'add_conditions')
    def test_filter(self, add_conditions):
        query = self.query.filter(TestModel.test_field_one == TestModel.test_field_two)
        add_conditions.return_value = None
        self.assertTrue(add_conditions.called)
        self.assertIs(query, self.query)

    @mock.patch('backends.postgresql.query.PostgreSQLQuery._join')
    def test_outer_join(self, _join):
        _join.return_value = None
        query = self.query.outer_join(TestModel)
        self.assertTrue(_join.called)
        self.assertIs(query, self.query)

    @mock.patch('backends.postgresql.query.PostgreSQLQuery._join')
    def test_join(self, _join):
        _join.return_value = None
        query = self.query.join(TestModel)
        self.assertTrue(_join.called)
        self.assertIs(query, self.query)

    @mock.patch('backends.postgresql.query.PostgreSQLQuery._join')
    def test_left_join(self, _join):
        _join.return_value = None
        query = self.query.left_join(TestModel)
        self.assertTrue(_join.called)
        self.assertIs(query, self.query)

    @mock.patch('backends.postgresql.query.PostgreSQLQuery._join')
    def test_right_join(self, _join):
        _join.return_value = None
        query = self.query.left_join(TestModel)
        self.assertTrue(_join.called)
        self.assertIs(query, self.query)

    @mock.patch(prefix + 'add_ordering_fields')
    def test_order_by(self, add_ordering_fields):
        query = self.query.order_by(TestModel.test_field_two)
        add_ordering_fields.return_value = None
        self.assertTrue(add_ordering_fields.called)
        self.assertEqual(query, self.query)

    # TODO FIX after adding logic
    def test_all(self):
        query = self.query.all()
        self.assertIs(query, self.query)

    # TODO FIX after adding logic
    def test_first(self):
        query = self.query.first()
        self.assertIs(query, self.query)

    # TODO FIX after adding logic
    def test_last(self):
        query = self.query.last()
        self.assertIs(query, self.query)

    @mock.patch(prefix + 'build')
    def test_sql(self, build):
        build.return_value = 'test'
        query = self.query.sql()
        self.assertEqual(query, 'test')

