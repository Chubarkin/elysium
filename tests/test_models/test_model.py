import mock
import unittest

from elysium import exceptions
from elysium.backends.postgresql.query import PostgreSQLQuery
from elysium.models import Model, Field


class TestModel(unittest.TestCase):
    def setUp(self):
        class ModelExample(Model):
            field_one = Field()
            field_two = Field()

        self.model_class = ModelExample

    def test_init(self):
        self.model_class._fields = {'field_one', 'field_two'}
        instance = self.model_class(field_one=1, field_two='test')
        self.assertEqual(instance.field_one, 1)
        self.assertEqual(instance.field_two, 'test')

        self.assertRaises(exceptions.FieldError, self.model_class, field_one=1,
                          field_two='test', field_three='wrong')

    @mock.patch('elysium.models.meta_model.ModelMetaClass.get_initial_query')
    @mock.patch('elysium.backends.postgresql.query.PostgreSQLQuery.save')
    @mock.patch('elysium.factory.postgresql_factory.INSERT_QUERY_TYPE', 1)
    def test_save(self, save, get_initial_query):
        get_initial_query.return_value = PostgreSQLQuery(1)
        instance = self.model_class(field_one=1, field_two='test')
        instance.save()
        self.assertEqual(save.call_count, 1)
