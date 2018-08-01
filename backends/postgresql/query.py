from __future__ import absolute_import

import elysium.backends.postgresql.constants as const
from elysium.query.query import Query


class PostgreSQLQuery(Query):
    def select(self, *fields):
        self._query_builder.add_fields(*fields)
        self._query_builder.add_models_from_fields()
        return self

    def set_model(self, model):
        self._query_builder.add_model(model)
        return self

    def filter(self, *conditions):
        self._query_builder.add_conditions(*conditions)
        self._query_builder.add_models_from_conditions()
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

    def order_by(self, *fields):
        self._query_builder.add_ordering_fields(*fields)
        return self

    def all(self):
        return self

    def first(self):
        return self

    def last(self):
        return self

    def save(self, instance):
        self._query_builder.add_insertion_data(instance.__dict__)
        return self

    def sql(self):
        return self._query_builder.build()

    def _join(self, joined_model, on, join_type):
        self._query_builder.add_joined_models(joined_model)
        self._query_builder.add_joined_conditions(on)
        self._query_builder.add_join_types(join_type)
