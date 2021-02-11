#!/usr/bin/python3
"""
Tests classes and functions in the base_model module
"""
from models.base_model import BaseModel
from datetime import datetime
import unittest


class TestBaseInitiation(unittest.TestCase):
    """
    Tests the correct initiation of the BaseModel class
    """
    def test_iniation(self):
        """Tests initiation"""
        cls = BaseModel()
        self.assertIsInstance(cls, BaseModel)


class TestBaseCorrectness(unittest.TestCase):
    """
    Tests the existance of public attributes
    and their correctness.

    Requirment:
        Public instance attributes:
            id: string - assign with an uuid when an instance is created:
            created_at: datetime - assign with the current datetime when an instance is created
            updated_at: datetime - assign with the current datetime when an instance is created and it will be updated every time you change your object
        __str__: should print: [<class name>] (<self.id>) <self.__dict__>
        Public instance methods:
            save(self): updates the public instance attribute updated_at with the current datetime
            to_obj(self): returns a dictionary containing all keys/values of __dict__ of the instance:
                - by using self.__dict__, only instance attributes set will be returned
                - a key __class__ must be added to this dictionary with the class name of the object
                - created_at and updated_at must be converted to string object in ISO format:
                    format: %Y-%m-%dT%H:%M:%S.%f (ex: 2017-06-14T22:31:03.285259)
    """

    def assertDateTimeEqualEqual(self, time1, time2):
        """
            checks the equalness of two date tiems
        """
        pass

    def setUp(self):
        """
        Creates the classes needed for testing
        """

        self.NUMOFTESTS = 100
        self.cls_id_lst = [BaseModel().id for x in range(self.NUMOFTESTS)]

        self.cls1_creation = datetime.now()
        self.cls1 = BaseModel()

        self.cls2 = BaseModel()
        self.cls3 = BaseModel()
        self.cls4 = BaseModel()

    def test_id(self):
        """
        Tests the correctness of the id attribute
        """

        # Test if it is a string
        self.assertIsInstance(self.cls1.id, str)
        self.assertIsInstance(self.cls2.id, str)

        # Test that ids from different objects are infact different
        for x in range(self.NUMOFTESTS):
            for y in range(x + 1, self.NUMOFTESTS):
                self.assertNotEqual(self.cls_id_lst[x], self.cls_id_lst[y])

    def test_time(self):
        """
        Tests the correctness of the created_at and updated_at
        public attributes
        """

        # Tests if they are instances of datetime
        self.assertIsInstance(self.cls1.created_at, datetime)

        # Test if the class created_at is around the correct time
        self.assertDateTimeEqualEqual(self.cls1_creation, self.cls1.created_at)

        # Tests if the updated time is also set coorrectl set
        self.assertIsInstance(self.cls1.updated_at, datetime)
        self.assertDateTimeEqualEqual(self.cls1.created_at, self.cls1.updated_at)

        self.cls1_update = datetime.now()
        # Test the change of updtaed time with the change of attribute
        self.cls1.id = "Random string has been set to be the id"

        # Test if the class updated_at variable is updated corrctly with class updates
        self.assertDateTimeEqualEqual(self.cls1_update, self.cls1.updated_at)

    def test_str(self):
        """
        Check if the string represtnation of the object is correctly formated
        """

        returned = self.cls1.__str__()
        expected = "{} ({}) {}".format(self.cls1.__class__, self.cls1.id,
                                       self.cls1.__dict__)

        # Test if the string represntation follows the format
        self.assertEqual(returned, expected)

    def test_save(self):
        """
            Test if the save function updates the time
        """

        self.cls2_update = datetime.now()
        self.cls2.save()

        # Test if the class updated_at variable is updated corrctly with object updates
        self.assertDateTimeEqualEqual(self.cls2_update, self.cls2.updated_at)

    def test_to_obj(self):
        """
            Test if the to_obj function
            operates as it is intended
        """
        dict = self.cls3.to_obj()

        # Test if "updated_at" & "created_at" are attributes of the returned dictionary
        if "updated_at" not in dict.keys():
            self.fail("updated_at Key not found in returned dictionary")
        elif "created_at" not in dict.keys():
            self.fail("created_at Key not found in returned dictionary")
        else:
            # Test if dict["updated_at"] & dict["created_at"] use the isotime format
            self.assertEquals(dict["updated_at"], dict["updated_at"].isoformat())
            self.assertEquals(dict["created_at"], dict["updated_at"].isoformat())

        # Include extra variables to make sure they are handeld by the to_obj function
        self.cls3.name = "Random Name"
        self.cls3.number = 444

        self.cls3_dic = {
            "name": "Random Name",
            "number": 444,
            "id": self.cls3.id,
            "updated_at": self.cls3.updated_at,
            "created_at": self.cls3.created_at,
            "__class__": self.cls3.__class__,
        }

        # Test if returned dictionary from to_obj  and the excpected one are equal
        self.assertDictEqual(dict, self.cls3.to_obj())

if __name__ == "__main__":
    unittest.main()
