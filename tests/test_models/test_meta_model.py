import mock
import unittest

from elysium.backends.postgresql.query import PostgreSQLQuery
from elysium.factory.postgresql_factory import PostgreSQLFactory
from elysium.models.field import Field
from elysium.models.meta_model import ModelMetaClass


class TestModelMetaClass(unittest.TestCase):
    def test_new(self):
        model_cls = ModelMetaClass('Model', (), {'field': Field()})
        self.assertEqual(model_cls.__tablename__, 'model')
        self.assertEqual(model_cls._fields, {'field'})

        model_cls = ModelMetaClass(
            'Model', (), {'field': Field(), '__tablename__': 'test_model'})
        self.assertEqual(model_cls.__tablename__, 'test_model')
        self.assertEqual(model_cls._fields, {'field'})

    @mock.patch('elysium.models.meta_model.ModelMetaClass.get_initial_query')
    @mock.patch('elysium.backends.postgresql.query.PostgreSQLQuery.select')
    @mock.patch('elysium.factory.postgresql_factory.SELECT_QUERY_TYPE', 1)
    def test_select(self, select, get_initial_query):
        get_initial_query.return_value = PostgreSQLQuery(1)
        model_cls = ModelMetaClass('Model', (), {'field': Field()})
        model_cls.select()
        self.assertEqual(get_initial_query.call_count, 1)
        self.assertEqual(select.call_count, 1)

    @mock.patch('elysium.models.meta_model.ModelMetaClass.get_initial_query')
    @mock.patch('elysium.backends.postgresql.query.PostgreSQLQuery.filter')
    @mock.patch('elysium.factory.postgresql_factory.SELECT_QUERY_TYPE', 1)
    def test_filter(self, filter, get_initial_query):
        get_initial_query.return_value = PostgreSQLQuery(1)
        model_cls = ModelMetaClass('Model', (), {'field': Field()})
        model_cls.filter()
        self.assertEqual(get_initial_query.call_count, 1)
        self.assertEqual(filter.call_count, 1)

    @mock.patch('elysium.factory.factory', PostgreSQLFactory())
    @mock.patch('elysium.factory.postgresql_factory.SELECT_QUERY_TYPE', 1)
    @mock.patch('elysium.factory.postgresql_factory.PostgreSQLFactory.get_query')
    @mock.patch('elysium.backends.postgresql.query.PostgreSQLQuery.set_model')
    def test_get_initial_query(self, set_model, get_query):
        get_query.return_value = PostgreSQLQuery(1)
        model_cls = ModelMetaClass('Model', (), {'field': Field()})
        query = model_cls.get_initial_query(1)
        self.assertEqual(get_query.call_count, 1)
        self.assertEqual(set_model.call_count, 1)
