class BaseError(Exception):
    def __repr__(self):
        return self.__class__.__name__


class ConditionError(Exception):
    pass


class ConfigurationError(BaseError):
    pass


class FieldError(Exception):
    pass


class ModelError(Exception):
    pass


class QueryBuilderError(Exception):
    pass


class QueryTypeError(Exception):
    pass

# __all__ = ['ConditionError']
