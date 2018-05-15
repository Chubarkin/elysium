from query.query import Query


class Model(object):
    _query = Query()
    __tablename__ = NotImplemented

    @classmethod
    def select(cls, fields):
        return cls._query.select(fields)
