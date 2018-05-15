import operators

CONDITION_TMPL = '%s %s %s'
CONDITION_TMPL_WITH_PARENTHESES = '(%s %s %s)'


class ConditionMixin(object):
    def __eq__(self, other):
        return Condition(self, other, operators.EQ)

    def __ne__(self, other):
        return Condition(self, other, operators.NE)

    def __and__(self, other):
        return Condition(self, other, operators.AND)

    def __or__(self, other):
        return Condition(self, other, operators.OR)

    def __ge__(self, other):
        return Condition(self, other, operators.GE)

    def __gt__(self, other):
        return Condition(self, other, operators.GT)

    def __le__(self, other):
        return Condition(self, other, operators.LE)

    def __lt__(self, other):
        return Condition(self, other, operators.LT)

    def contains(self, item):
        return Condition(item, self, operators.IN)

    def is_null(self):
        return Condition(self, None, operators.IS_NULL)

    def is_not_null(self):
        return Condition(self, None, operators.IS_NOT_NULL)


class Condition(ConditionMixin):
    def __init__(self, left_operand, right_operand, operator):
        self._validate(left_operand, right_operand, operator)
        self._left_operand = left_operand
        self._right_operand = right_operand
        self._operator = operator

    def to_str(self):
        return self._to_str(self._operator.priority)

    def _to_str(self, upper_priority):
        if self._operator.priority and \
                self._operator.priority < upper_priority:
            tmpl = CONDITION_TMPL_WITH_PARENTHESES
        else:
            tmpl = CONDITION_TMPL

        left_operand_str = self._get_operand_str(self._left_operand)
        right_operand_str = self._get_operand_str(self._right_operand)

        return tmpl % (left_operand_str, self._operator.string_repr,
                       right_operand_str)

    def _get_operand_str(self, operand):
        if isinstance(operand, Condition):
            return operand._to_str(self._operator.priority)

        return operand.to_str() if operand else ''

    @staticmethod
    def _validate(left_operand, right_operand, operator):
        if operator.priority is None \
            and (isinstance(left_operand, Condition)
                 or isinstance(right_operand, Condition)):

            raise Exception()

