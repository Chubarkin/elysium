import mock
import unittest

from elysium.backends.postgresql.builder import PostgreSQLSelectQueryBuilder, PostgreSQLInsertQueryBuilder
from elysium.backends.postgresql.query import PostgreSQLQuery
from elysium.factory.postgresql_factory import PostgreSQLFactory


class TestPostgreSQLFactory(unittest.TestCase):
    def setUp(self):
        self.factory = PostgreSQLFactory()

    @mock.patch('elysium.factory.postgresql_factory.SELECT_QUERY_TYPE', 0)
    @mock.patch('elysium.factory.postgresql_factory.INSERT_QUERY_TYPE', 1)
    def test_get_query_builder(self):
        query_builder = self.factory.get_query_builder(0)
        self.assertIsInstance(query_builder, PostgreSQLSelectQueryBuilder)

        query_builder = self.factory.get_query_builder(1)
        self.assertIsInstance(query_builder, PostgreSQLInsertQueryBuilder)

        self.assertRaises(Exception, self.factory.get_query_builder, 2)

    @mock.patch('elysium.factory.postgresql_factory.PostgreSQLFactory.get_query_builder')
    def test_get_query(self, get_query_builder):
        get_query_builder.return_value = PostgreSQLSelectQueryBuilder()
        query = self.factory.get_query(0)
        self.assertIsInstance(query, PostgreSQLQuery)

    def test_get_operators(self):
        from elysium.backends.postgresql import operators
        returned_operators = self.factory.get_operators()
        self.assertEqual(returned_operators, operators)
