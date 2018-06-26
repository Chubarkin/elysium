import mock
import unittest

from models import Model, Field
from factory.postgres_factory import PostgresFactory


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


@mock.patch('factory.factory', PostgresFactory())
class TestPostrgreSQLQuery(unittest.TestCase):
    def test_select_all_fields_sql(self):
        query = TestModel.select().sql()
        self.assertEqual(query, 'SELECT * FROM testmodel')

    def test_select_concrete_field_sql(self):
        query = TestModel.select(TestModel.test_field_one).sql()
        self.assertEqual(query, 'SELECT testmodel.test_field_one FROM testmodel')
