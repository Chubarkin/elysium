from abc import ABCMeta, abstractmethod


from constants import SELECT, FROM, WHERE


class Command(object):
    __metaclass__ = ABCMeta
    TYPE = NotImplemented

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def convert_to_sql(self):
        pass


class SelectCommand(Command):
    TYPE = SELECT

    def __init__(self, *args, **kwargs):
        self._args = args
        super(SelectCommand, self).__init__(self, *args, **kwargs)

    def convert_to_sql(self):
        pass


class FromCommand(Command):
    TYPE = FROM

    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        super(FromCommand, self).__init__(self, *args, **kwargs)

    def convert_to_sql(self):
        pass


class WhereCommand(Command):
    TYPE = WHERE

    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs
        super(WhereCommand, self).__init__(self, *args, **kwargs)

    def convert_to_sql(self):
        pass
