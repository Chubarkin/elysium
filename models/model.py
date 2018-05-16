from meta_model import ModelMetaClass


class Model(object):
    __metaclass__ = ModelMetaClass
    __tablename__ = NotImplemented
