import mock
import unittest

from elysium import exceptions
from elysium.models import Model, Field
from elysium.query import condition, commands
from elysium.backends.postgresql.builder import PostgreSQLSelectQueryBuilder, PostgreSQLInsertQueryBuilder


class TestModel(Model):
    __tablename__ = 'testmodel'
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    __tablename__ = 'testmodeltwo'
    test_field_one = Field()
    test_field_two = Field()


class TestPostgreSQLSelectQueryBuilder(unittest.TestCase):
    def setUp(self):
        self._query_builder = PostgreSQLSelectQueryBuilder()
        self._prefix = 'elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder.'

    def test_add_tables(self):
        self._query_builder.add_model(TestModel)
        self.assertEqual(self._query_builder._models, {TestModel})

    def test_add_fields(self):
        self._query_builder.add_fields(TestModel.test_field_one)
        self.assertEqual(self._query_builder._fields, {TestModel.test_field_one})
        # TODO Add exceptions
        self.assertRaises(exceptions.FieldError, self._query_builder.add_fields, 'Not field instance')

    def test_add_models_from_fields(self):
        self._query_builder._fields.add(TestModel.test_field_one)
        self._query_builder.add_models_from_fields()
        self.assertEqual(self._query_builder._models, {TestModel})

    @mock.patch('elysium.query.condition.Condition.get_models')
    def test_add_conditions(self, get_models):
        get_models.return_value = {TestModel}
        self._query_builder.add_conditions(TestModel.test_field_one == TestModelTwo.test_field_one)
        self.assertEqual(len(self._query_builder._conditions), 1)
        self.assertIsInstance(self._query_builder._conditions.pop(), condition.Condition)
        self.assertRaises(exceptions.ConditionError, self._query_builder.add_conditions, 'Not condition instance')

    def test_add_models_from_conditions(self):
        self._query_builder._conditions.add(TestModel.test_field_one == TestModelTwo.test_field_one)
        self._query_builder.add_models_from_conditions()
        self.assertEqual(self._query_builder._models, {TestModel, TestModelTwo})

    def test_add_joined_models(self):
        self._query_builder.add_joined_models(TestModel)
        self.assertEqual(self._query_builder._joined_models, [TestModel])
        self.assertRaises(exceptions.ModelError, self._query_builder.add_joined_models, 'Not model class')

    def test_add_joined_conditions(self):
        self._query_builder.add_joined_conditions(TestModel.test_field_one == TestModelTwo.test_field_one)
        self.assertEqual(len(self._query_builder._joined_conditions), 1)
        self.assertIsInstance(self._query_builder._joined_conditions[0], condition.Condition)
        self.assertRaises(exceptions.ConditionError, self._query_builder.add_joined_conditions, 'Not condition instance')

    def test_add_join_types(self):
        self._query_builder.add_join_types(1)
        self.assertEqual(self._query_builder._join_types, [1])

    def test_add_ordering_fields(self):
        self._query_builder.add_ordering_fields(TestModel.test_field_one)
        self.assertEqual(len(self._query_builder._ordering_fields), 0)
        self._query_builder._models.add(TestModel)
        self._query_builder.add_ordering_fields(TestModel.test_field_one)
        self.assertEqual(self._query_builder._ordering_fields, [TestModel.test_field_one])
        self.assertRaises(exceptions.FieldError, self._query_builder.add_ordering_fields, 'Not field instance')
        self._query_builder.add_ordering_fields(TestModelTwo.test_field_one)
        self.assertEqual(self._query_builder._ordering_fields, [TestModel.test_field_one])

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._add_commands')
    @mock.patch('elysium.query.commands.SelectCommand.to_str')
    def test_build(self, command_to_str, _add_commands):
        command_to_str.return_value = 'SELECT *'
        _add_commands.return_value = None

        self._query_builder._commands.append(commands.SelectCommand())
        sql = self._query_builder.build()
        self.assertEqual(_add_commands.call_count, 1)
        self.assertEqual(sql, 'SELECT *')

    def test__add_commands(self):
        patches = [
            mock.patch(self._prefix + '_add_select_command'),
            mock.patch(self._prefix + '_add_from_command'),
            mock.patch(self._prefix + '_add_join_commands'),
            mock.patch(self._prefix + '_add_where_command'),
            mock.patch(self._prefix + '_add_order_by_command')
        ]

        for patch in patches:
            patch.start()

        self._query_builder._add_commands()
        self.assertEqual(self._query_builder._add_select_command.call_count, 1)
        self.assertEqual(self._query_builder._add_from_command.call_count, 1)
        self.assertEqual(self._query_builder._add_join_commands.call_count, 1)
        self.assertEqual(self._query_builder._add_where_command.call_count, 1)
        self.assertEqual(self._query_builder._add_order_by_command.call_count, 1)

        for patch in patches:
            patch.stop()

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_fields_string')
    def test__add_select_command(self, _get_fields_string):
        self._query_builder._commands = []
        _get_fields_string.return_value = '*'
        self._query_builder._add_select_command()
        self.assertIsInstance(self._query_builder._commands[0], commands.SelectCommand)

        self._query_builder._commands = []
        _get_fields_string.return_value = 'test'
        self._query_builder._add_select_command()
        self.assertIsInstance(self._query_builder._commands[0], commands.SelectCommand)

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_tables_string')
    def test__add_from_command(self, _get_tables_string):
        _get_tables_string.return_value = 'test'
        self._query_builder._add_from_command()
        self.assertIsInstance(self._query_builder._commands[0], commands.FromCommand)

        _get_tables_string.return_value = ''
        self.assertRaises(exceptions.QueryBuilderError, self._query_builder._add_from_command)

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_join_string')
    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_join_type_command')
    def test__add_join_commands(self, _get_join_type_command, _get_join_string):
        _get_join_string.return_value = 'test'
        _get_join_type_command.return_value = commands.RightCommand
        self._query_builder._add_join_commands()
        self.assertEqual(self._query_builder._commands, [])

        self._query_builder._joined_models.append(TestModelTwo)
        self.assertEqual(self._query_builder._commands, [])

        self._query_builder._joined_conditions.append(TestModelTwo.test_field_one == TestModel.test_field_one)
        self._query_builder._join_types.append('test')
        self._query_builder._add_join_commands()
        self.assertIsInstance(self._query_builder._commands[0], commands.RightCommand)

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_conditions_string')
    def test__add_where_command(self, _get_conditions_string):
        _get_conditions_string.return_value = ''
        self._query_builder._add_where_command()
        self.assertEqual(self._query_builder._commands, [])

        _get_conditions_string.return_value = 'test'
        self._query_builder._add_where_command()
        self.assertIsInstance(self._query_builder._commands[0], commands.WhereCommand)

    @mock.patch('elysium.backends.postgresql.builder.PostgreSQLSelectQueryBuilder._get_ordering_fields_string')
    def test__add_order_by_command(self, _get_ordering_fields_string):
        _get_ordering_fields_string.return_value = ''
        self._query_builder._add_order_by_command()
        self.assertEqual(self._query_builder._commands, [])

        _get_ordering_fields_string.return_value = 'test'
        self._query_builder._add_order_by_command()
        self.assertIsInstance(self._query_builder._commands[0], commands.OrderByCommand)

    @mock.patch('elysium.backends.postgresql.constants.FIELDS_SPLITTER', ', ')
    @mock.patch('elysium.backends.postgresql.constants.ALL_FIELDS_SELECTOR', '*')
    @mock.patch('elysium.models.field.Field.to_str')
    def test__get_fields_string(self, to_str):
        fields_str = self._query_builder._get_fields_string()
        self.assertEqual(fields_str, '*')

        to_str.return_value = 'test'
        self._query_builder._fields.add(TestModel.test_field_one)
        fields_str = self._query_builder._get_fields_string()
        self.assertEqual(fields_str, 'test')

        self._query_builder._fields.add(TestModel.test_field_two)
        fields_str = self._query_builder._get_fields_string()
        self.assertEqual(fields_str, 'test, test')

    @mock.patch('elysium.backends.postgresql.constants.TABLES_SPLITTER', ', ')
    def test__get_tables_string(self):
        tables_str = self._query_builder._get_tables_string()
        self.assertEqual(tables_str, '')

        self._query_builder._models.add(TestModel)
        tables_str = self._query_builder._get_tables_string()
        self.assertEqual(tables_str, 'testmodel')

        self._query_builder._models.add(TestModelTwo)
        tables_str = self._query_builder._get_tables_string()
        self.assertIn(tables_str, ['testmodel, testmodeltwo',
                                   'testmodeltwo, testmodel'])

        self._query_builder._joined_models.append(TestModel)
        tables_str = self._query_builder._get_tables_string()
        self.assertEqual(tables_str, 'testmodeltwo')

    @mock.patch('elysium.query.commands.JoinCommand.to_str')
    @mock.patch('elysium.query.commands.OnCommand.to_str')
    @mock.patch('elysium.query.condition.Condition.to_str')
    def test__get_join_string(self, condition_to_str, on_command_to_str, join_command_to_str):
        condition_to_str.return_value = 'test'
        on_command_to_str.return_value = 'ON'
        join_command_to_str.return_value = 'JOIN '

        join_str = self._query_builder._get_join_string(
            ('test', TestModel, TestModel.test_field_one == TestModelTwo.test_field_two))
        self.assertEqual(on_command_to_str.call_count, 1)
        self.assertEqual(join_command_to_str.call_count, 1)
        self.assertEqual(join_str, 'JOIN ON')

    @mock.patch('elysium.backends.postgresql.constants.CONDITIONS_SPLITTER', ' AND ')
    @mock.patch('elysium.query.condition.Condition.to_str')
    def test__get_conditions_string(self, to_str):
        to_str.return_value = 'test'
        condition_str = self._query_builder._get_conditions_string()
        self.assertEqual(condition_str, '')

        self._query_builder._conditions.add(TestModel.test_field_one == TestModel.test_field_two)
        condition_str = self._query_builder._get_conditions_string()
        self.assertEqual(condition_str, 'test')

        self._query_builder._conditions.add(TestModel.test_field_one == TestModelTwo.test_field_two)
        condition_str = self._query_builder._get_conditions_string()
        self.assertEqual(condition_str, 'test AND test')

    @mock.patch('elysium.backends.postgresql.constants.FIELDS_SPLITTER', ', ')
    @mock.patch('elysium.backends.postgresql.constants.ORDERING_FIELDS_TMPL', '%s %s')
    @mock.patch('elysium.models.field.Field.to_str')
    @mock.patch('elysium.query.commands.DescCommand.to_str')
    def test__get_ordering_fields_string(self, desc_to_str, field_to_str):
        field_to_str.return_value = 'test'
        desc_to_str.return_value = 'DESC'

        ordering_str = self._query_builder._get_ordering_fields_string()
        self.assertEqual(ordering_str, '')

        self._query_builder._ordering_fields.append(TestModel.test_field_one)
        ordering_str = self._query_builder._get_ordering_fields_string()
        self.assertEqual(ordering_str, 'test')

        self._query_builder._ordering_fields.append(TestModel.test_field_two.desc())
        ordering_str = self._query_builder._get_ordering_fields_string()
        self.assertIn(ordering_str, 'test, test DESC')

    @mock.patch('elysium.backends.postgresql.builder.const')
    def test__get_join_type_command(self, constants):
        constants.INNER_JOIN_TYPE = 0
        constants.OUTER_JOIN_TYPE = 1
        constants.LEFT_JOIN_TYPE = 2
        constants.RIGHT_JOIN_TYPE = 3

        command = self._query_builder._get_join_type_command(constants.INNER_JOIN_TYPE)
        self.assertEqual(command, commands.InnerCommand)

        command = self._query_builder._get_join_type_command(constants.OUTER_JOIN_TYPE)
        self.assertEqual(command, commands.OuterCommand)

        command = self._query_builder._get_join_type_command(constants.LEFT_JOIN_TYPE)
        self.assertEqual(command, commands.LeftCommand)

        command = self._query_builder._get_join_type_command(constants.RIGHT_JOIN_TYPE)
        self.assertEqual(command, commands.RightCommand)

        command = self._query_builder._get_join_type_command(None)
        self.assertEqual(command, commands.InnerCommand)


class TestPostgreSQLInsertQueryBuilder(unittest.TestCase):
    prefix = 'elysium.backends.postgresql.builder.PostgreSQLInsertQueryBuilder.'

    def setUp(self):
        self._query_builder = PostgreSQLInsertQueryBuilder()

    def test_add_insertion_data(self):
        self._query_builder.add_insertion_data({'field': 1})
        self.assertEqual(self._query_builder._insertion_fields, ['field'])
        self.assertEqual(self._query_builder._insertion_values, [1])

    def test_add_model(self):
        self._query_builder.add_model(TestModel)
        self.assertEqual(self._query_builder._model, TestModel)

    @mock.patch(prefix + '_add_insert_into_command')
    @mock.patch(prefix + '_add_values_command')
    def test__add_commands(self, _add_values_command, _add_insert_into_command):
        self._query_builder._add_commands()
        self.assertEqual(_add_insert_into_command.call_count, 1)
        self.assertEqual(_add_values_command.call_count, 1)

    def test__add_insert_into_command(self):
        self._query_builder._add_insert_into_command()
        self.assertEqual(self._query_builder._commands, [])

        self._query_builder._insertion_fields.append('test')
        self._query_builder._model = TestModel
        self._query_builder._add_insert_into_command()
        self.assertIsInstance(self._query_builder._commands[0],
                              commands.InsertIntoCommand)

    def test__add_values_command(self):
        self._query_builder._add_values_command()
        self.assertEqual(self._query_builder._commands, [])

        self._query_builder._insertion_values.append('test')
        self._query_builder._add_values_command()
        self.assertIsInstance(self._query_builder._commands[0],
                              commands.ValuesCommand)
