#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            storage.all().clear()
        except:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        n = {'Name': 'test'}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_create_valid_class_no_params(self):
        """Tests creating an object with a valid class name and no parameters."""
        args = "User"
        self.hbnb.do_create(args)
        self.assertIn(args, storage.all().keys())

    def test_create_invalid_class(self):
        """Tests creating an object with an invalid class name."""
        args = "InvalidClass"
        with self.assertRaises(Exception) as e:
            self.hbnb.do_create(args)
            self.assertEqual(str(e.exception), "** class doesn't exist **")

    def test_create_valid_class_with_params(self):
        """Tests creating an object with a valid class name and parameters."""
        args = "User email='johndoe@example.com' name='John Doe'"
        self.hbnb.do_create(args)
        user = storage.all()["User." + self.hbnb.last_instance]
        self.assertEqual(user.email, "johndoe@example.com")
        self.assertEqual(user.name, "John Doe")

    def test_create_with_invalid_param_format(self):
        """Tests creating an object with an invalid parameter format."""
        args = "User invalid_param"
        with self.assertRaises(Exception) as e:
            self.hbnb.do_create(args)
            self.assertEqual(str(e.exception), "** bad format for param **")

    def test_create_with_missing_param_value(self):
        """Tests creating an object with a parameter missing a value."""
        args = "User name="
        with self.assertRaises(Exception) as e:
            self.hbnb.do_create(args)
            self.assertEqual(str(e.exception), "** value missing **")

    def test_parse_params_valid_params(self):
        """Tests parsing valid parameters."""
        params_str = "email='johndoe@example.com', name='John Doe'"
        params = self.hbnb.parse_params(params_str)
        self.assertEqual(params, {"email": "johndoe@example.com", "name": "John Doe"})

    def test_parse_params_empty_param(self):
        """Tests parsing an empty parameter string."""
        params_str = ""
        params = self.hbnb.parse_params(params_str)
        self.assertEqual(params, {})

    def test_parse_params_invalid_param_format(self):
        """Tests parsing a parameter string with an invalid format."""
        params_str = "invalid_param"
        with self.assertRaises(Exception) as e:
            self.hbnb.parse_params(params_str)
            self.assertEqual(str(e.exception), "** bad format for param **")

    def test_parse_value_string(self):
        """Tests parsing a string value."""
        value_str = '"This is a string with quotes"'
        parsed_value = self.hbnb.parse_value(value_str)
        self.assertEqual(parsed_value, "This is a string with quotes")

    def test_parse_value_integer(self):
        """Tests parsing an integer value."""
        value_str = "100"
        parsed_value = self.hbnb.parse_value(value_str)
        self.assertEqual(parsed_value, 100)

    def test_parse_value_float(self):
        """Tests parsing a float value."""
        value_str = "4.54"
        parsed_value = self.hbnb.parse_value(value_str)
        self.assertEqual(parsed_value, 4.54)
