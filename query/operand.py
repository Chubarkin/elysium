# TODO Try to remove cyclic imports


class Operand(object):
    def __init__(self, instance):
        self._instance = instance

    def is_condition(self):
        from condition import Condition
        return isinstance(self._instance, Condition)

    def is_field(self):
        from models.field import Field
        return isinstance(self._instance, Field)

    def to_str(self):
        from models.field import Field
        from condition import Condition
        if isinstance(self._instance, Condition):
            return self._instance.to_str()
        elif isinstance(self._instance, Field):
            return self._instance.to_str()
        elif isinstance(self._instance, str):
            return '"%s"' % self._instance

        return self._instance

    @property
    def instance(self):
        return self._instance
