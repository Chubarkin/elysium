from query.condition import ConditionMixin

FIELD_NAME_TMPL = '%s.%s'


class Field(ConditionMixin):
    def __init__(self, field_name=None):
        self._model = None
        self._field_name = field_name
        self._descending = False

    def __get__(self, instance, owner):
        self.model = owner
        return self

    def to_str(self, alias=None):
        table_name = alias or self._model.__tablename__
        return FIELD_NAME_TMPL % (table_name, self._field_name)

    def _set_field_name(self, field_name):
        if not self._field_name:
            self._field_name = field_name

    def _get_field_name(self):
        return self._field_name

    field_name = property(_get_field_name, _set_field_name)

    def _set_model(self, model):
        if not self._model:
            self._model = model

    def _get_model(self):
        return self._model

    model = property(_get_model, _set_model)

    def desc(self):
        self._descending = True
        return self

    @property
    def is_descending(self):
        is_descending = self._descending
        self._descending = False
        return is_descending
