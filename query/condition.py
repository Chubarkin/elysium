class ConditionMixin(object):
    def __eq__(self, other):
        return Condition(self, other, '=')

    def __and__(self, other):
        return Condition(self, other, 'AND')

    def __or__(self, other):
        return Condition(self, other, 'OR')


class Condition(ConditionMixin):
    def __init__(self, left_operand, right_operand, operation):
        self._left_operand = left_operand
        self._right_operand = right_operand
        self._operation = operation
