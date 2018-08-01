from elysium.query.constants import STRING_TMPL


class Operand(object):
    def __init__(self, instance):
        self._instance = instance

    def is_condition(self):
        from condition import Condition
        return isinstance(self._instance, Condition)

    def is_field(self):
        from elysium.models.field import Field
        return isinstance(self._instance, Field)

    def to_str(self):
        if self.is_condition() or self.is_field():
            return self._instance.to_str()
        elif isinstance(self._instance, str):
            return STRING_TMPL % self._instance
        elif self._instance is not None:
            return str(self._instance)

        return ''

    @property
    def instance(self):
        return self._instance
