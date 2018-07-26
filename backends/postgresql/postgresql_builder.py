import constants as const
import models
import query.condition
from query.builder import SelectQueryBuilder, InsertQueryBuilder
from query import commands


# TODO Split into classes for Select, Insert and etc.
class PostgreSQLSelectQueryBuilder(SelectQueryBuilder):
    def __init__(self):
        super(PostgreSQLSelectQueryBuilder, self).__init__()
        self._models = set()
        self._fields = set()
        self._conditions = set()
        self._joined_models = []
        self._joined_conditions = []
        self._join_types = []
        self._ordering_fields = []

    def add_models(self, *_models):
        for model in _models:
            self._models.add(model)

    def add_fields(self, *fields):
        for field in fields:
            if not isinstance(field, models.Field):
                raise Exception()
        self._fields |= set(fields)

    def add_models_from_fields(self):
        for field in self._fields:
            self._models.add(field.model)

    def add_conditions(self, *conditions):
        for condition in conditions:
            if not isinstance(condition, query.condition.Condition):
                raise Exception()
        self._conditions |= set(conditions)

    def add_models_from_conditions(self):
        for condition in self._conditions:
            self._models |= condition.get_models()

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
                self._ordering_fields.append(field)

    def _add_commands(self):
        self._add_select_command()
        self._add_from_command()
        self._add_join_commands()
        self._add_where_command()
        self._add_order_by_command()

    def _add_select_command(self):
        fields_str = self._get_fields_string()
        self._commands.append(commands.SelectCommand(fields_str))

    def _add_from_command(self):
        tables_str = self._get_tables_string()
        if not tables_str:
            raise Exception()
        self._commands.append(commands.FromCommand(tables_str))

    def _add_join_commands(self):
        for join_type, joined_model, joined_condition in zip(
                self._join_types, self._joined_models, self._joined_conditions):
            join_str = self._get_join_string((join_type, joined_model, joined_condition))
            command = self._get_join_type_command(join_type)
            self._commands.append(command(join_str))

    def _add_where_command(self):
        conditions_str = self._get_conditions_string()
        if conditions_str:
            self._commands.append(commands.WhereCommand(conditions_str))

    def _add_order_by_command(self):
        ordering_fields_str = self._get_ordering_fields_string()
        if ordering_fields_str:
            self._commands.append(commands.OrderByCommand(ordering_fields_str))

    def _get_fields_string(self):
        return const.FIELDS_SPLITTER.join(
            [field.to_str() for field in self._fields]) or const.ALL_FIELDS_SELECTOR

    def _get_tables_string(self):
        return const.TABLES_SPLITTER.join([model.__tablename__ for model in filter(
            lambda x: x not in self._joined_models, self._models)])

    @staticmethod
    def _get_join_string(join_details):
        join_type, joined_model, joined_condition = join_details
        return ''.join([commands.JoinCommand(joined_model.__tablename__).to_str(),
                        commands.OnCommand(joined_condition.to_str()).to_str()])

    def _get_conditions_string(self):
        return const.CONDITIONS_SPLITTER.join(
            [condition.to_str() for condition in self._conditions])

    def _get_ordering_fields_string(self):
        return const.FIELDS_SPLITTER.join(
            [const.ORDERING_FIELDS_TMPL % (field.to_str(), commands.DescCommand().to_str())
             if field.is_descending else field.to_str() for field in self._ordering_fields])

    @staticmethod
    def _get_join_type_command(join_type):
        command = commands.InnerCommand
        if join_type == const.OUTER_JOIN_TYPE:
            command = commands.OuterCommand
        elif join_type == const.LEFT_JOIN_TYPE:
            command = commands.LeftCommand
        elif join_type == const.RIGHT_JOIN_TYPE:
            command = commands.RightCommand

        return command


class PostgreSQLInsertQueryBuilder(InsertQueryBuilder):
    def __init__(self):
        super(PostgreSQLInsertQueryBuilder, self).__init__()
        self._insertion_fields = []
        self._insertion_values = []
        self._model = None

    def add_insertion_data(self, data):
        # TODO ADD validation and transformation
        for field, value in data.iteritems():
            self._insertion_fields.append(field)
            self._insertion_values.append(str(value))

    def add_models(self, model):
        self._model = model

    def _add_commands(self):
        self._add_insert_into_command()
        self._add_values_command()

    def _add_insert_into_command(self):
        table = self._model.__tablename__
        self._commands.append(commands.InsertIntoCommand(
            const.INSERTION_TMPL % (table, const.FIELDS_SPLITTER.join(self._insertion_fields))))

    def _add_values_command(self):
        self._commands.append(commands.ValuesCommand(
            const.VALUES_TMPL % const.FIELDS_SPLITTER.join(self._insertion_values)))
