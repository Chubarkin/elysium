from constants import CONDITION_TMPL
from factory import factory
from operand import Operand

operators = factory.get_operators()


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
        self._left_operand = Operand(left_operand)
        self._right_operand = Operand(right_operand)
        self._operator = operator

    def to_str(self):
        left_operand_str = self._left_operand.to_str()
        right_operand_str = self._right_operand.to_str()

        return CONDITION_TMPL % (
            left_operand_str, self._operator.string_repr, right_operand_str)

    def get_table_names(self):
        return self._get_table_names(Operand(self))

    def _get_table_names(self, operand):
        if operand.is_condition():
            return self._get_table_names(operand.instance.left_operand) | \
                self._get_table_names(operand.instance.right_operand)
        return {operand.instance.table_name} if operand.is_field() else set()

    @staticmethod
    def _validate(left_operand, right_operand, operator):
        if operator in [operators.AND, operators.OR] \
            and not (isinstance(left_operand, Condition)
                     and isinstance(right_operand, Condition)):

            raise Exception()

    @property
    def left_operand(self):
        return self._left_operand

    @property
    def right_operand(self):
        return self._right_operand
