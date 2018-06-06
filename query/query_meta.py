import functools
from abc import ABCMeta

import constants as const


class QueryMetaClass(ABCMeta):
    @staticmethod
    def _validate_operation_order(operation, operation_name):
        @functools.wraps(operation)
        def validated(self, *args, **kwargs):
            if getattr(self, '_prev_operation', None) and \
                    const.PREVIOUS_OPERATION.get(operation_name) and \
                    const.PREVIOUS_OPERATION[operation_name] != self._prev_operation:
                raise Exception()

            if getattr(self, '_next_operation', None) and \
                    self._next_operation != operation_name:
                raise Exception()

            result = operation(self, *args, **kwargs)
            self._prev_operation = operation_name
            self._next_operation = const.NEXT_OPERATION.get(operation_name)
            return result

        return validated

    def __new__(metaname, classname, baseclasses, attrs):
        for variable, value in attrs.iteritems():
            if variable in const.VALIDATED_OPERATIONS:
                attrs[variable] = \
                    metaname._validate_operation_order(value, variable)

        return super(QueryMetaClass, metaname) \
            .__new__(metaname, classname, baseclasses, attrs)
