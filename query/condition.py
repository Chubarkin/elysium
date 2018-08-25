from elysium.exceptions import ConditionError
from elysium.factory import factory
from elysium.query.constants import CONDITION_TMPL
from elysium.query.operand import Operand, EmptyOperand

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

    def in_(self, iterable):
        return Condition(self, iterable, operators.IN)

    def is_null(self):
        return Condition(self, EmptyOperand(), operators.IS_NULL)

    def is_not_null(self):
        return Condition(self, EmptyOperand(), operators.IS_NOT_NULL)


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

    def get_data(self, data=None):
        if data is None:
            data = []

        self._add_operand_data(self._left_operand, data)
        self._add_operand_data(self._right_operand, data)
        return data

    @staticmethod
    def _add_operand_data(operand, data):
        if operand.is_data():
            data.append(operand.instance)
        elif operand.is_condition():
            operand.instance.get_data(data)

    def get_models(self):
        return self._get_models(Operand(self))

    def _get_models(self, operand):
        if operand.is_condition():
            return self._get_models(operand.instance.left_operand) | \
                self._get_models(operand.instance.right_operand)
        return {operand.instance.model} if operand.is_field() else set()

    @staticmethod
    def _validate(left_operand, right_operand, operator):
        if operator in [operators.AND, operators.OR] \
            and not (isinstance(left_operand, Condition)
                     and isinstance(right_operand, Condition)):

            raise ConditionError(
                'The condition can not be constructed. '
                'Are you sure that the condition is in parentheses?'
            )

    @property
    def left_operand(self):
        return self._left_operand

    @property
    def right_operand(self):
        return self._right_operand
