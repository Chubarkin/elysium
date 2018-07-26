from abc import ABCMeta, abstractmethod


class AbstractFactory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_query_builder(self, query_type):
        pass

    @abstractmethod
    def get_query(self, query_type):
        pass

    @abstractmethod
    def get_operators(self):
        pass
