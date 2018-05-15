from Queue import Queue

from builder import QueryBuilder


class Query(object):
    def __init__(self):
        self._query_builder = QueryBuilder()
        self._commands_queue = Queue()

    def select(self, *args):
        return self

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self

    def first(self):
        return self

    def last(self):
        return self
