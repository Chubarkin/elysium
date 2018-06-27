from meta_model import ModelMetaClass
from factory import factory


class Model(object):
    __metaclass__ = ModelMetaClass
    __tablename__ = NotImplemented

    @classmethod
    def select(cls, *fields):
        # TODO remove duplicate code
        query = factory.get_query()
        query.set_table(cls.__tablename__)
        return query.select(*fields)

    @classmethod
    def filter(cls, *conditions):
        query = factory.get_query()
        query.set_table(cls.__tablename__)
        return query.filter(*conditions)
