from meta_model import ModelMetaClass
from factory import factory


class Model(object):
    __metaclass__ = ModelMetaClass
    __tablename__ = NotImplemented

    def __init__(self, **kwargs):
        for field in self._fields:
            setattr(self, field, None)

        for field, value in kwargs.iteritems():
            if field not in self._fields:
                raise Exception()
            setattr(self, field, value)

    def save(self):
        query = self.__class__.get_initial_query()
        return query.save(self)
