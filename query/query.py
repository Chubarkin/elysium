from builder import QueryBuilder
from query_meta import QueryMetaClass


class Query(object):
    __metaclass__ = QueryMetaClass

    def __init__(self):
        self._query_builder = QueryBuilder()

    def select(self, *fields):
        self._query_builder.add_fields(*fields)
        return self

    def filter(self, *conditions):
        self._query_builder.add_conditions(*conditions)
        return self

    def all(self):
        return self

    def first(self):
        return self

    def last(self):
        return self

    @property
    def sql(self):
        return self._query_builder.build()
