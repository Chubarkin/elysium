from abc import ABCMeta, abstractmethod


class QueryBuilder(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_models(self, models):
        pass

    @abstractmethod
    def add_fields(self, *fields):
        pass

    @abstractmethod
    def add_conditions(self, *conditions):
        pass

    @abstractmethod
    def add_joined_models(self, joined_model):
        pass

    @abstractmethod
    def add_joined_conditions(self, joined_conditions):
        pass

    @abstractmethod
    def add_join_types(self, join_type):
        pass

    @abstractmethod
    def add_insertion_data(self, data):
        pass

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def set_query_type(self, query_type):
        pass
