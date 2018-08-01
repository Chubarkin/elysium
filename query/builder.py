from abc import ABCMeta, abstractmethod


class QueryBuilder(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._commands = []

    @abstractmethod
    def _add_commands(self):
        pass

    def build(self):
        self._add_commands()
        return ''.join([command.to_str() for command in self._commands])


class SelectQueryBuilder(QueryBuilder):
    @abstractmethod
    def add_model(self, model):
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


class InsertQueryBuilder(QueryBuilder):
    @abstractmethod
    def add_model(self, model):
        pass

    @abstractmethod
    def add_insertion_data(self, data):
        pass
