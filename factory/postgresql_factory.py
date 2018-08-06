from elysium.factory.abstract_factory import AbstractFactory
from elysium.query.constants import SELECT_QUERY_TYPE, INSERT_QUERY_TYPE


class PostgreSQLFactory(AbstractFactory):
    def get_query_builder(self, query_type):
        from elysium.backends.postgresql.builder import PostgreSQLSelectQueryBuilder, PostgreSQLInsertQueryBuilder
        if query_type == SELECT_QUERY_TYPE:
            return PostgreSQLSelectQueryBuilder()
        elif query_type == INSERT_QUERY_TYPE:
            return PostgreSQLInsertQueryBuilder()
        raise Exception()

    def get_query(self, query_type):
        from elysium.backends.postgresql.query import PostgreSQLQuery
        return PostgreSQLQuery(query_type)

    def get_operators(self):
        from elysium.backends.postgresql import operators
        return operators
