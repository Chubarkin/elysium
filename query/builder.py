import commands
import constants as const


class QueryBuilder(object):
    def __init__(self):
        self._tables = set()
        self._fields = set()
        self._conditions = set()
        self._joined_tables = list()
        self._joined_conditions = list()
        self._commands = []

    def add_tables(self, tables):
        pass

    def add_fields(self, *fields):
        self._fields = self._fields.union(fields)
        for field in self._fields:
            self._tables.add(field.table_name)

    def add_conditions(self, *conditions):
        self._conditions = self._conditions.union(conditions)
        for condition in self._conditions:
            self._tables = self._tables.union(condition.get_table_names())

    def add_joined_tables(self, joined_table):
        self._joined_tables.append(joined_table)

    def add_joined_conditions(self, joined_conditions):
        self._joined_conditions.append(joined_conditions)

    def build(self):
        # TODO validate tables
        fields_str = const.FIELDS_SPLITTER.join(
            [field.to_str() for field in self._fields]) or const.ALL_FIELDS_SELECTOR
        self._commands.append(commands.SelectCommand(fields_str))

        tables_str = const.TABLES_SPLITTER.join(self._tables)
        self._commands.append(commands.FromCommand(tables_str))

        for joined_table, joined_condition in zip(self._joined_tables, self._joined_conditions):
            self._commands.append(commands.JoinCommand(joined_table.__tablename__))
            self._commands.append(commands.OnCommand(joined_condition.to_str()))

        conditions_str = const.CONDITIONS_SPLITTER.join(
            [const.CONDITIONS_TMPL % condition.to_str() for condition in self._conditions])
        self._commands.append(commands.WhereCommand(conditions_str))

        return ''.join([command.to_str() for command in self._commands])
