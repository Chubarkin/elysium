import unittest
from models import Model, Field


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestQuery(unittest.TestCase):
    # TODO mock factory
    def test_select_all_fields_sql(self):
        query = TestModel.select().sql()
        self.assertEqual(query, 'SELECT * FROM testmodel')

    def test_select_concrete_field_sql(self):
        query = TestModel.select(TestModel.test_field_one).sql()
        self.assertEqual(query, 'SELECT testmodel.test_field_one FROM testmodel')
