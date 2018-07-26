from abstract_factory import AbstractFactory
from backends.postgresql.postgresql_builder import PostgreSQLSelectQueryBuilder, PostgreSQLInsertQueryBuilder
from backends.postgresql.postgresql_query import PostgreSQLQuery
from query.constants import SELECT_QUERY_TYPE, INSERT_QUERY_TYPE


class PostgresFactory(AbstractFactory):
    def get_query_builder(self, query_type):
        if query_type == SELECT_QUERY_TYPE:
            return PostgreSQLSelectQueryBuilder()
        elif query_type == INSERT_QUERY_TYPE:
            return PostgreSQLInsertQueryBuilder()
        raise Exception()

    def get_query(self, query_type):
        return PostgreSQLQuery(query_type)

    def get_operators(self):
        from backends.postgresql import operators
        return operators
