from datetime import date

from elysium.query.condition import ConditionMixin

FIELD_NAME_TMPL = '%s.%s'


class Field(ConditionMixin):
    _python_type = None

    def __init__(self, null=False, blank=False,
                 unique=False, primary_key=False,
                 default=None):
        self._model = None
        self._null = null
        self._blank = blank
        self._unique = unique
        self._primary_key = primary_key
        self._default = default
        self._descending = False
        self._field_name = None

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


class IntegerField(Field):
    _python_type = int

    def __init__(self, serial=False, *args):
        self._serial = serial
        super(IntegerField, self).__init__(*args)


class SmallIntegerField(Field):
    _python_type = int

    def __init__(self, serial=False, *args):
        self._serial = serial
        super(SmallIntegerField, self).__init__(*args)


class BigIntegerField(Field):
    _python_type = long

    def __init__(self, serial=False, *args):
        self._serial = serial
        super(BigIntegerField, self).__init__(*args)


class RealField(Field):
    _python_type = float


class DoubleField(Field):
    _python_type = float


class BooleanField(Field):
    _python_type = bool


class CharField(Field):
    _python_type = str

    def __init__(self, max_length, *args):
        self._max_length = max_length
        super(CharField, self).__init__(*args)


class TextField(Field):
    _python_type = str


class DateField(Field):
    _python_type = date


__all__ = ['Field', 'IntegerField', 'SmallIntegerField', 'BigIntegerField',
           'RealField', 'DoubleField', 'BooleanField', 'CharField',
           'TextField', 'DateField']
