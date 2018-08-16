from elysium.query.constants import SUBSTITUTION_TMPL


class EmptyOperand(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(EmptyOperand, cls).__new__(cls)
        return cls._instance


class Operand(object):
    def __init__(self, instance):
        self._instance = instance

    def is_condition(self):
        from elysium.query.condition import Condition
        return isinstance(self._instance, Condition)

    def is_field(self):
        from elysium.models.field import Field
        return isinstance(self._instance, Field)

    def is_data(self):
        return not self.is_condition() and not self.is_field()\
               and not isinstance(self._instance, EmptyOperand)

    def to_str(self):
        if self.is_condition() or self.is_field():
            return self._instance.to_str()
        elif isinstance(self._instance, EmptyOperand):
            return ''
        return SUBSTITUTION_TMPL

    @property
    def instance(self):
        return self._instance
