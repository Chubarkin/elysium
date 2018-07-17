import mock
import unittest

from models import Model, Field
from factory.postgres_factory import PostgresFactory


class TestModel(Model):
    test_field_one = Field()
    test_field_two = Field()


class TestModelTwo(Model):
    test_field_one = Field()
    test_field_two = Field()


@mock.patch('factory.factory', PostgresFactory())
class TestPostrgreSQLQuery(unittest.TestCase):
    def test_select(self):
        query = TestModel.select().sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel')

        query = TestModel.select(TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT testmodel.test_field_one FROM testmodel')

    def test_filter(self):
        query = TestModel.filter(TestModel.test_field_one == 2).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel WHERE (testmodel.test_field_one = 2)')

        query = TestModel.filter(TestModel.test_field_one == 2, TestModel.test_field_two == 3).sql().rstrip()
        self.assertIn(query, ['SELECT * FROM testmodel '
                              'WHERE (testmodel.test_field_one = 2) AND (testmodel.test_field_two = 3)',
                              'SELECT * FROM testmodel '
                              'WHERE (testmodel.test_field_two = 3) AND (testmodel.test_field_one = 2)'])

        query = TestModel.filter(TestModelTwo.test_field_two == 2).sql().rstrip()
        self.assertIn(query, ['SELECT * FROM testmodel, testmodeltwo '
                              'WHERE (testmodeltwo.test_field_two = 2)',
                              'SELECT * FROM testmodeltwo, testmodel '
                              'WHERE (testmodeltwo.test_field_two = 2)'])

    def test_outer_join(self):
        query = TestModel.select().outer_join(
            TestModelTwo, on=TestModelTwo.test_field_two == TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel '
                                'OUTER JOIN testmodeltwo ON (testmodeltwo.test_field_two = testmodel.test_field_one)')

    def test_join(self):
        query = TestModel.select().join(
            TestModelTwo, on=TestModelTwo.test_field_two == TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel '
                                'INNER JOIN testmodeltwo ON (testmodeltwo.test_field_two = testmodel.test_field_one)')

    def test_left_join(self):
        query = TestModel.select().left_join(
            TestModelTwo, on=TestModelTwo.test_field_two == TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel '
                                'LEFT JOIN testmodeltwo ON (testmodeltwo.test_field_two = testmodel.test_field_one)')

    def test_right_join(self):
        query = TestModel.select().right_join(
            TestModelTwo, on=TestModelTwo.test_field_two == TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel '
                                'RIGHT JOIN testmodeltwo ON (testmodeltwo.test_field_two = testmodel.test_field_one)')

    def test_order_by(self):
        query = TestModel.select().order_by(TestModel.test_field_one).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel ORDER BY testmodel.test_field_one')

        query = TestModel.select().order_by(TestModel.test_field_one, TestModel.test_field_two).sql().rstrip()
        self.assertIn(query, ['SELECT * FROM testmodel '
                              'ORDER BY testmodel.test_field_one, testmodel.test_field_two',
                              'SELECT * FROM testmodel '
                              'ORDER BY testmodel.test_field_two, testmodel.test_field_one'])

        query = TestModel.select().order_by(TestModel.test_field_one.desc()).sql().rstrip()
        self.assertEqual(query, 'SELECT * FROM testmodel '
                                'ORDER BY testmodel.test_field_one DESC')
