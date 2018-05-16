from field import Field


class ModelMetaClass(type):
    def __new__(metaname, classname, baseclasses, attrs):
        for variable, value in attrs.iteritems():
            if isinstance(value, Field):
                value.set_field_name(variable)

        if '__tablename__' not in attrs.keys():
            attrs['__tablename__'] = classname.lower()

        return super(ModelMetaClass, metaname)\
            .__new__(metaname, classname, baseclasses, attrs)
