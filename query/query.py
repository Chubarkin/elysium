from abc import abstractmethod

from elysium.query.query_meta import QueryMetaClass


class Query(object):
    __metaclass__ = QueryMetaClass

    def __init__(self, query_type):
        from elysium.factory import factory
        self._query_builder = factory.get_query_builder(query_type)

    @abstractmethod
    def select(self, *fields):
        pass

    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def filter(self, *conditions):
        pass

    @abstractmethod
    def join(self, joined_table, on=None):
        pass

    @abstractmethod
    def outer_join(self, joined_table, on=None):
        pass

    @abstractmethod
    def left_join(self, joined_table, on=None):
        pass

    @abstractmethod
    def right_join(self, joined_table, on=None):
        pass

    @abstractmethod
    def all(self):
        pass

    @abstractmethod
    def first(self):
        pass

    @abstractmethod
    def last(self):
        pass

    @abstractmethod
    def save(self, instance):
        pass

    @abstractmethod
    def sql(self):
        pass
