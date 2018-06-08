from abstract_factory import AbstractFactory
from backends.postgresql.postgresql_builder import PostgreSQLQueryBuilder
from backends.postgresql.postgresql_query import PostgreSQLQuery


class PostgresFactory(AbstractFactory):
    def get_query_builder(self):
        return PostgreSQLQueryBuilder()

    def get_query(self):
        return PostgreSQLQuery()

    def get_operators(self):
        from backends.postgresql import operators
        return operators
