import mock
import unittest

from elysium.models import Model, Field


class TestField(unittest.TestCase):
    def setUp(self):
        self.field = Field()

        class ModelExample(Model):
            pass

        self.model_class = ModelExample

    def test_get(self):
        self.assertIsNone(self.field._model)

        self.model_class.field = self.field

        self.assertEqual(self.model_class.field._model, self.model_class)
        self.assertEqual(self.field._model, self.model_class)

    @mock.patch('elysium.models.field.FIELD_NAME_TMPL', '%s.%s')
    def test_to_str(self):
        self.field._model = self.model_class
        self.model_class.__tablename__ = 'table'
        self.field._field_name = 'field'

        field_str = self.field.to_str()
        self.assertEqual(field_str, 'table.field')

        field_str = self.field.to_str(alias='t')
        self.assertEqual(field_str, 't.field')

    def test__set_field_name(self):
        self.field._field_name = None
        self.field._set_field_name('field_name')
        self.assertEqual(self.field._field_name, 'field_name')

        self.field._set_field_name('new_field_name')
        self.assertEqual(self.field._field_name, 'field_name')

    def test__get_field_name(self):
        self.field._field_name = 'field'
        field_name = self.field._get_field_name()
        self.assertEqual(field_name, 'field')

    def test__set_model(self):
        self.field._model = None
        self.field._set_model(self.model_class)
        self.assertEqual(self.field._model, self.model_class)

        class NewModelExample(Model):
            pass

        self.field._set_model(NewModelExample)
        self.assertEqual(self.field._model, self.model_class)

    def test__get_model(self):
        self.field._model = self.model_class
        model = self.field._get_model()
        self.assertEqual(model, self.model_class)
