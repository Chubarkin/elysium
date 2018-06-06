from abc import ABCMeta, abstractmethod


class Factory(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_query_builder(self):
        pass
