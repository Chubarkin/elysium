from meta_model import ModelMetaClass
from query.query import Query


class Model(object):
    __metaclass__ = ModelMetaClass
    __tablename__ = NotImplemented

    @classmethod
    def select(cls, *fields):
        query = Query()
        return query.select(*fields)

    @classmethod
    def filter(cls, *conditions):
        query = Query()
        return query.filter(*conditions)
