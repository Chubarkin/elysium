import constants as const

from factory import factory
from query_meta import QueryMetaClass


class Query(object):
    __metaclass__ = QueryMetaClass

    def __init__(self):
        self._query_builder = factory.get_query_builder()

    def select(self, *fields):
        self._query_builder.add_fields(*fields)
        return self

    def filter(self, *conditions):
        self._query_builder.add_conditions(*conditions)
        return self

    def join(self, joined_table, on=None):
        self._join(joined_table, on=on, join_type=const.INNER_JOIN_TYPE)
        return self

    def outer_join(self, joined_table, on=None):
        self._join(joined_table, on=on, join_type=const.OUTER_JOIN_TYPE)
        return self

    def left_join(self, joined_table, on=None):
        self._join(joined_table, on=on, join_type=const.LEFT_JOIN_TYPE)
        return self

    def right_join(self, joined_table, on=None):
        self._join(joined_table, on=on, join_type=const.RIGHT_JOIN_TYPE)
        return self

    def all(self):
        return self

    def first(self):
        return self

    def last(self):
        return self

    def sql(self):
        return self._query_builder.build()

    def _join(self, joined_table, on, join_type):
        self._query_builder.add_joined_tables(joined_table)
        self._query_builder.add_joined_conditions(on)
        self._query_builder.add_join_types(join_type)
