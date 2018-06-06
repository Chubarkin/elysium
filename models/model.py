from meta_model import ModelMetaClass
from factory import factory

class Model(object):
    __metaclass__ = ModelMetaClass
    __tablename__ = NotImplemented

    @classmethod
    def select(cls, *fields):
        query = factory.get_query()
        return query.select(*fields)

    @classmethod
    def filter(cls, *conditions):
        query = factory.get_query()
        return query.filter(*conditions)
