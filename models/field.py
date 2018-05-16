from query.condition import ConditionMixin


class Field(ConditionMixin):
    def __init__(self, field_name=None):
        self._table_name = None
        self._field_name = field_name

    def __get__(self, instance, owner):
        self._table_name = owner.__tablename__
        return self

    def to_str(self, alias=None):
        table_name = alias or self._table_name
        return '%s.%s' % (table_name, self._field_name)

    def set_field_name(self, field_name):
        if not self._field_name:
            self._field_name = field_name
