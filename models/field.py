from query.condition import ConditionMixin

FIELD_NAME_TMPL = '%s.%s'


class Field(ConditionMixin):
    def __init__(self, field_name=None):
        self._table_name = None
        self._field_name = field_name

    def __get__(self, instance, owner):
        self.table_name = owner.__tablename__
        return self

    def to_str(self, alias=None):
        table_name = alias or self._table_name
        return FIELD_NAME_TMPL % (table_name, self._field_name)

    def _set_field_name(self, field_name):
        if not self._field_name:
            self._field_name = field_name

    def _get_field_name(self):
        return self._field_name

    field_name = property(_get_field_name, _set_field_name)

    def _set_table_name(self, table_name):
        if not self._table_name:
            self._table_name = table_name

    def _get_table_name(self):
        return self._table_name

    table_name = property(_get_table_name, _set_table_name)
