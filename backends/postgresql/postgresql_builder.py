import constants as const
import models
import query.condition
from query.builder import QueryBuilder
from query import commands


class PostgreSQLQueryBuilder(QueryBuilder):
    def __init__(self):
        self._tables = set()
        self._fields = set()
        self._conditions = set()
        self._joined_tables = list()
        self._joined_conditions = list()
        self._join_types = list()
        self._commands = []

    def add_tables(self, tables):
        pass

    def add_fields(self, *fields):
        self._fields = self._fields.union(fields)
        for field in self._fields:
            if not isinstance(field, models.Field):
                raise Exception()
            self._tables.add(field.table_name)

    def add_conditions(self, *conditions):
        self._conditions = self._conditions.union(conditions)
        for condition in self._conditions:
            if not isinstance(condition, query.condition.Condition):
                raise Exception()
            self._tables = self._tables.union(condition.get_table_names())

    def add_joined_tables(self, joined_table):
        if not issubclass(joined_table, models.Model):
            raise Exception()
        self._joined_tables.append(joined_table)

    def add_joined_conditions(self, joined_conditions):
        if not isinstance(joined_conditions, query.condition.Condition):
            raise Exception()
        self._joined_conditions.append(joined_conditions)

    def add_join_types(self, join_type):
        self._join_types.append(join_type)

    def build(self):
        fields_str = const.FIELDS_SPLITTER.join(
            [field.to_str() for field in self._fields]) or const.ALL_FIELDS_SELECTOR
        self._commands.append(commands.SelectCommand(fields_str))

        tables_str = const.TABLES_SPLITTER.join(self._tables)
        self._commands.append(commands.FromCommand(tables_str))

        for join_type, joined_table, joined_condition in zip(
                self._join_types, self._joined_tables, self._joined_conditions):
            join_str = ''.join([commands.JoinCommand(joined_table.__tablename__).to_str(),
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
            [const.CONDITIONS_TMPL % condition.to_str() for condition in self._conditions])
        self._commands.append(commands.WhereCommand(conditions_str))

        return ''.join([command.to_str() for command in self._commands])
