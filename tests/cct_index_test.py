from unittest.mock import MagicMock
from c5dec.core.cct import Index, BaseClass
from c5dec.common import C5decError
import unittest
import sys
import os
# Add the parent directory to the sys.path so modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

# Average cyclomatic complexity is A (3.0366). Calculated with Radon.


class TestBaseClass(BaseClass):
    def is_valid(self):
        pass  # Implement the abstract method is_valid for testing


class TestIndex(unittest.TestCase):

    def setUp(self):
        # Create an instance of the Index class
        self.index = Index()

    def test_update_and_get(self):
        # Create objects for testing
        obj1 = TestBaseClass(_id="obj1")
        obj2 = TestBaseClass(_id="obj2")

        # Update the index with objects
        self.index.update("obj1", obj1)
        self.index.update("obj2", obj2)

        # Retrieve objects from the index and check if they match the originals
        retrieved_obj1 = self.index.get("obj1")
        retrieved_obj2 = self.index.get("obj2")

        self.assertEqual(retrieved_obj1, obj1)
        self.assertEqual(retrieved_obj2, obj2)

    def test_update_and_get_keys(self):
        obj1 = TestBaseClass(_id="obj1")
        obj2 = TestBaseClass(_id="obj2")

        # Update the index with objects
        self.index.update("obj1", obj1)
        self.index.update("obj2", obj2)

        keys = self.index.keys()
        self.assertEqual(list(keys), [obj1._id, obj2._id])

    def test_update_non_unique(self):
        # Create objects with non-unique IDs
        obj1 = TestBaseClass(_id="duplicate_id")
        obj2 = TestBaseClass(_id="duplicate_id")

        # Update the index with the first object (should not raise an error)
        self.index.update("duplicate_id", obj1)
        size = len(self.index._index)

        # Attempt to update the index with the second object (should raise a ValueError)
        with self.assertRaises(C5decError):
            self.index.update("duplicate_id", obj2)

        # Update the index with the same initial object. No changes expected
        self.index.update("duplicate_id", obj1)
        self.assertEqual(size, len(self.index._index))

    def test_get_nonexistent_key(self):
        # Try to retrieve an object with a key that does not exist in the index
        with self.assertRaises(KeyError):
            retrieved_obj = self.index.get("nonexistent_key")

    def test_yield_objects(self):
        # define BaseClass subclasses
        class SubClass1(BaseClass):
            def is_valid(self):
                pass
        
        class SubClass2(BaseClass):
            def is_valid(self):
                pass
        
        # initialize subclasses
        sub1 = SubClass1(_id="sub1", _name="subclass1")
        sub2 = SubClass1(_id="sub2", _name="subclass2")
        sub3 = SubClass2(_id="sub3", _name="subclass3")
        
        # update index
        self.index.update(sub1._id, sub1)
        self.index.update(sub2._id, sub2)
        self.index.update(sub3._id, sub3)

        # yield objects of type SubClass1
        type1 = list(self.index.yield_obj(SubClass1))

        self.assertEqual(type1, [sub1, sub2])

    def test_clear(self):
        # Create a mock object for BaseClass
        obj = MagicMock(spec=BaseClass)
        obj._id = "obj_to_clear"  # Set necessary attributes for the mock object

        # Update the index with the mock object
        self.index.update("obj_to_clear", obj)

        # Clear the index and check if it's empty
        self.index.clear()
        self.assertFalse(self.index.keys())

    def test_update_with_different_types(self):
        # Create objects with different types
        int_key = 123
        str_value = "string_value"

        # Attempt to update the index with non-BaseClass objects (should raise a ValueError)
        with self.assertRaises(C5decError):
            self.index.update(int_key, str_value)

    def test_update_with_subclass_of_BaseClass(self):
        # Create a subclass of BaseClass
        class SubClass(BaseClass):
            def is_valid(self):
                pass

        # Create an object of the subclass
        obj = SubClass(_id="subclass_obj")

        # Update the index with the subclass object (should not raise an error)
        self.index.update("subclass_obj", obj)

        # Retrieve the object from the index and check if it matches the original
        retrieved_obj = self.index.get("subclass_obj")
        self.assertEqual(retrieved_obj, obj)

    def tearDown(self):
        self.index.clear()

if __name__ == '__main__':
    unittest.main()

