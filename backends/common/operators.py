from elysium.query.operator import Operator


AND = Operator('AND')
OR = Operator('OR')
EQ = Operator('=')
NE = Operator('<>')
GE = Operator('>=')
GT = Operator('>')
LE = Operator('<=')
LT = Operator('<')
IN = Operator('IN')
IS_NULL = Operator('IS NULL')
IS_NOT_NULL = Operator('IS NOT NULL')
