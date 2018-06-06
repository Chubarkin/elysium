from abc import ABCMeta, abstractmethod


class QueryBuilder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_tables(self, tables):
        pass

    @abstractmethod
    def add_fields(self, *fields):
        pass

    @abstractmethod
    def add_conditions(self, *conditions):
        pass

    @abstractmethod
    def add_joined_tables(self, joined_table):
        pass

    @abstractmethod
    def add_joined_conditions(self, joined_conditions):
        pass

    @abstractmethod
    def add_join_types(self, join_type):
        pass

    @abstractmethod
    def build(self):
        pass
