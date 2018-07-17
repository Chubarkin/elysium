import constants as const
import models
import query.condition
from query.builder import QueryBuilder
from query import commands


class PostgreSQLQueryBuilder(QueryBuilder):
    def __init__(self):
        self._models = set()
        self._fields = set()
        self._conditions = set()
        self._joined_models = list()
        self._joined_conditions = list()
        self._join_types = list()
        self._ordering_fields = set()
        self._commands = []

    def add_models(self, *_models):
        for model in _models:
            self._models.add(model)

    def add_fields(self, *fields):
        self._fields = self._fields.union(fields)
        for field in self._fields:
            if not isinstance(field, models.Field):
                raise Exception()
            self._models.add(field.model)

    def add_conditions(self, *conditions):
        self._conditions = self._conditions.union(conditions)
        for condition in self._conditions:
            if not isinstance(condition, query.condition.Condition):
                raise Exception()
            self._models = self._models.union(condition.get_models())

    def add_joined_models(self, joined_model):
        if not isinstance(joined_model, type) or \
                not issubclass(joined_model, models.Model):
            raise Exception()
        self._joined_models.append(joined_model)

    def add_joined_conditions(self, joined_conditions):
        if not isinstance(joined_conditions, query.condition.Condition):
            raise Exception()
        self._joined_conditions.append(joined_conditions)

    def add_join_types(self, join_type):
        self._join_types.append(join_type)

    def add_ordering_fields(self, *fields):
        for field in fields:
            if not isinstance(field, models.Field):
                raise Exception()
            if field.model in self._models:
                self._ordering_fields.add(field)

    def build(self):
        fields_str = const.FIELDS_SPLITTER.join(
            [field.to_str() for field in self._fields]) or const.ALL_FIELDS_SELECTOR
        self._commands.append(commands.SelectCommand(fields_str))

        tables_str = const.TABLES_SPLITTER.join([model.__tablename__ for model in filter(
            lambda x: x not in self._joined_models, self._models)])
        self._commands.append(commands.FromCommand(tables_str))

        for join_type, joined_model, joined_condition in zip(
                self._join_types, self._joined_models, self._joined_conditions):
            join_str = ''.join([commands.JoinCommand(joined_model.__tablename__).to_str(),
                                commands.OnCommand(joined_condition.to_str()).to_str()])
            if join_type == const.INNER_JOIN_TYPE:
                self._commands.append(commands.InnerCommand(join_str))
            elif join_type == const.OUTER_JOIN_TYPE:
                self._commands.append(commands.OuterCommand(join_str))
            elif join_type == const.LEFT_JOIN_TYPE:
                self._commands.append(commands.LeftCommand(join_str))
            elif join_type == const.RIGHT_JOIN_TYPE:
                self._commands.append(commands.RightCommand(join_str))

        conditions_str = const.CONDITIONS_SPLITTER.join(
            [condition.to_str() for condition in self._conditions])

        if conditions_str:
            self._commands.append(commands.WhereCommand(conditions_str))

        ordering_fields_str = const.FIELDS_SPLITTER.join(
            [const.ORDERING_FIELDS_TMPL % (field.to_str(), commands.DescCommand().to_str())
             if field.is_descending else field.to_str() for field in self._ordering_fields])
        if ordering_fields_str:
            self._commands.append(commands.OrderByCommand(ordering_fields_str))

        return ''.join([command.to_str() for command in self._commands])
