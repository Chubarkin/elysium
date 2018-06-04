from builder import QueryBuilder
from query_meta import QueryMetaClass


class Query(object):
    __metaclass__ = QueryMetaClass

    def __init__(self):
        self._query_builder = QueryBuilder()

    def select(self, *fields):
        # TODO validate fields
        self._query_builder.add_fields(*fields)
        return self

    def filter(self, *conditions):
        # TODO validate conditions
        self._query_builder.add_conditions(*conditions)
        return self

    # TODO add inner outer left joins
    def join(self, joined_table, on=None):
        # TODO validate table and conditions
        self._query_builder.add_joined_tables(joined_table)
        self._query_builder.add_joined_conditions(on)
        return self

    def all(self):
        return self

    def first(self):
        return self

    def last(self):
        return self

    def sql(self):
        return self._query_builder.build()
