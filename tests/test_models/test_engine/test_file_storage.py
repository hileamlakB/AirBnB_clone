#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.
Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import models
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""
    def test_FileStorage_instantiation_no_args(self):
        self.assertIsInstance(FileStorage(), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertIsInstance(FileStorage._FileStorage__file_path, str)

    def testFileStorage_objects_is_private_dict(self):
        self.assertIsInstance(FileStorage._FileStorage__objects, dict)

    def test_storage_initializes(self):
        self.assertIsInstance(models.storage, FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        self.cls_bm = BaseModel()
        models.storage.new(self.cls_bm)

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertIsInstance(models.storage.all(), dict)

    def test_all_with_arg(self):
        self.assertRaises(TypeError, models.storage.all, None)

    def test_new(self):

        self.assertIn("BaseModel." + self.cls_bm.id,
                      models.storage.all().keys())

    def test_new_with_None(self):
        self.assertRaises(AttributeError, models.storage.new, None)

    def test_save(self):

        models.storage.save()
        save_text = ""
        with open("file.json", "r") as json_file:
            save_text = json_file.read()
            self.assertIn("BaseModel." + self.cls_bm, save_text)

    def test_save_with_arg(self):
        self.assertRaises(TypeError, models.storage.save, None)

    def test_reload(self):

        FileStorage._FileStorage__objects = {}
        models.storage.reload()
        self.assertIn("BaseModel." + self.cls_bm.id,
                      FileStorage._FileStorage__objects.keys())

    def test_reload_no_file(self):
        self.assertRaises(FileNotFoundError, models.storage.reload)

    def test_reload_with_arg(self):
        self.assertRaises(TypeError, models.storage.reload, None)


if __name__ == "__main__":
    unittest.main()