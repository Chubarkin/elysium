from factory import Factory
from query.builder import QueryBuilder


class PostgresFactory(Factory):
    def get_query_builder(self):
        return QueryBuilder()
