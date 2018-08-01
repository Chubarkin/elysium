# TODO try remove cycling imports
from elysium.models.field import Field
from elysium.factory import factory
from elysium.query.constants import SELECT_QUERY_TYPE


class ModelMetaClass(type):
    def __new__(metaname, classname, baseclasses, attrs):
        attrs['_fields'] = set()
        for variable, value in attrs.iteritems():
            if isinstance(value, Field):
                value.field_name = variable
                attrs['_fields'].add(variable)

        if '__tablename__' not in attrs.keys():
            attrs['__tablename__'] = classname.lower()

        return super(ModelMetaClass, metaname)\
            .__new__(metaname, classname, baseclasses, attrs)

    def select(cls, *fields):
        query = cls.get_initial_query(SELECT_QUERY_TYPE)
        return query.select(*fields)

    def filter(cls, *conditions):
        query = cls.get_initial_query(SELECT_QUERY_TYPE)
        return query.filter(*conditions)

    def get_initial_query(cls, query_type):
        query = factory.get_query(query_type)
        query.set_model(cls)
        return query
