from query.operator import Operator


AND = Operator('AND', 2)
OR = Operator('OR', 1)
EQ = Operator('=', None)
NE = Operator('<>', None)
GE = Operator('>=', None)
GT = Operator('>', None)
LE = Operator('<=', None)
LT = Operator('<', None)
IN = Operator('IN', None)
IS_NULL = Operator('IS NULL', None)
IS_NOT_NULL = Operator('IS NOT NULL', None)
