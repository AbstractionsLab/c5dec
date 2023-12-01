from c5dec.core.cct import BaseClass
from c5dec.common import C5decError
from unittest.mock import patch, call
import unittest
import sys
import os

# Add the parent directory to the sys.path so that modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)


class MockBaseClass(BaseClass):
    def is_valid(self):
        pass  # Implement the abstract method is_valid for testing

class AnotherClass:
    pass
    
class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.base_instance = MockBaseClass(_id="test_id", _name="test_name")
        self.child_instance = MockBaseClass(_id="child_id", _name="child_name")
        self.sibling_instance = MockBaseClass(_id="sibling_id", _name="sibling_name")

    def test_init_and_attributes(self):
        self.assertEqual(self.base_instance._id, "test_id")
        self.assertEqual(self.base_instance._name, "test_name")
        self.assertIn("_id", self.base_instance.attrib)
        self.assertIn("_name", self.base_instance.attrib)

    def test_repr(self):
        self.assertEqual(repr(self.base_instance), "<class: MockBaseClass id=test_id>")

    def test_clone(self):
        cloned = self.base_instance.clone()
        self.assertNotEqual(id(cloned), id(self.base_instance))
        self.assertEqual(cloned._id, self.base_instance._id)
    
    def test_clone_deep_copy(self):
        # Clone the instance
        cloned_instance = self.base_instance.clone()

        # Make sure both instances are not the same object
        self.assertNotEqual(id(self.base_instance), id(cloned_instance))

        # Update attributes in the cloned instance
        cloned_instance._id = "456"
        cloned_instance._name = "UpdatedTestInstance"
        cloned_instance.text = "Sample Text"
        cloned_instance.children.append(MockBaseClass(_id="child", _name="ChildInstance"))

        # Assert that changes in the cloned instance do not affect the original instance
        self.assertNotEqual(cloned_instance._id, self.base_instance._id)
        self.assertNotEqual(cloned_instance._name, self.base_instance._name)
        self.assertNotEqual(cloned_instance.text, self.base_instance.text)
        self.assertNotEqual(len(cloned_instance.children), len(self.base_instance.children))

        # Modify the original and ensure it doesn't affect the clone
        self.base_instance._name = "AnotherName"
        self.assertNotEqual(cloned_instance._name, self.base_instance._name)

        self.assertEqual(self.base_instance._name, "AnotherName")
        self.assertEqual(cloned_instance._name, "UpdatedTestInstance")

    def test_collector_attribute(self):
        self.base_instance.children.append(self.child_instance)
        collected = list(self.base_instance.collector(target="_name", mode="attribute"))
        self.assertIn("test_name", collected)
        self.assertIn("child_name", collected)

    def test_collector_type(self):
        collected = list(self.base_instance.collector(target=BaseClass, mode="type"))
        self.assertIn(self.base_instance, collected)
    
    def test_collector_invalid_mode(self):
        collected = list(self.base_instance.collector("some_attr", mode="invalid_mode"))
        self.assertEqual(len(collected), 0)

    def test_collector_recursive_collection(self):
        grandchild = MockBaseClass(_id="grandchild")
        grandchild.some_attr = "deep_value"
        child = MockBaseClass(_id="child")
        child.children = [grandchild]
        self.base_instance.children = [child]

        collected = list(self.base_instance.collector("some_attr"))
        self.assertEqual(len(collected), 1)
        self.assertEqual(collected[0], "deep_value")

    def test_basic_functionality(self):
        instance = MockBaseClass(_id="test", _name="TestName")
        result = instance.get_formatted_text()
        expected = "\n# TEST TestName\n\n"
        self.assertEqual(result, expected)

    def test_hierarchy_handling(self):
        child = MockBaseClass(_id="child", _name="ChildName")
        instance = MockBaseClass(_id="test", _name="TestName")
        instance.container = [child]
        result = instance.get_formatted_text()
        expected = "\n# TEST TestName\n\n\n## CHILD ChildName\n\n"
        self.assertEqual(result, expected)

    def test_missing_name(self):
        instance = MockBaseClass(_id="test")
        result = instance.get_formatted_text()
        expected = "\n# TEST \n\n"
        self.assertEqual(result, expected)

    def test_custom_level(self):
        instance = MockBaseClass(_id="test", _name="TestName")
        result = instance.get_formatted_text(level=3)
        expected = "\n### TEST TestName\n\n"
        self.assertEqual(result, expected)
    
    def test_empty_container(self):
        instance = MockBaseClass(_id="test", _name="TestName")
        instance.container = []  # Explicitly setting an empty container.
        result = instance.get_formatted_text()
        expected = "\n# TEST TestName\n\n"
        self.assertEqual(result, expected)
    
    def test_multiple_elements_container(self):
        child1 = MockBaseClass(_id="child1", _name="ChildName1")
        child2 = MockBaseClass(_id="child2", _name="ChildName2")
        
        instance = MockBaseClass(_id="test", _name="TestName")
        instance.container = [child1, child2]
        
        result = instance.get_formatted_text()
        expected = "\n# TEST TestName\n\n\n## CHILD1 ChildName1\n\n\n## CHILD2 ChildName2\n\n"
        self.assertEqual(result, expected)

    def test_object_without_get_formatted_text(self):
        child = AnotherClass()
        instance = MockBaseClass(_id="test", _name="TestName")
        instance.container = [child]
        
        with self.assertRaises(AttributeError):
            instance.get_formatted_text()

    def test_is_empty(self):
        self.assertTrue(self.base_instance.is_empty())

    def test_valid_id(self):
        self.base_instance._id = "123"
        self.assertTrue(self.base_instance.has_valid_id())

    def test_missing_id(self):
        self.base_instance._id = None
        with self.assertRaises(C5decError):
            self.base_instance.has_valid_id()

    def test_invalid_id_data_type(self):
        self.base_instance._id = 123  # integer
        with self.assertRaises(C5decError):
            self.base_instance.has_valid_id()

    def test_valid_name(self):
        self.base_instance._name = "John"
        self.assertTrue(self.base_instance.has_valid_name())

    def test_missing_name(self):
        self.base_instance._name = None
        with self.assertRaises(C5decError):
            self.base_instance.has_valid_name()

    def test_invalid_name_data_type(self):
        self.base_instance._name = 123  # integer
        with self.assertRaises(C5decError):
            self.base_instance.has_valid_name()

    def test_contains(self):
        self.base_instance.children.append(self.child_instance)
        self.assertTrue(self.base_instance.contains(self.child_instance))
        self.assertFalse(self.base_instance.contains(self.sibling_instance))

    def test_get_children(self):
        self.base_instance.children.append(self.child_instance)
        self.base_instance.children.append(self.sibling_instance)
        self.assertListEqual(self.base_instance.get_children(), [self.child_instance,
                                                                  self.sibling_instance])
                                                                  
    def test_get_child_by_id(self):
        self.base_instance.children.append(self.child_instance)
        self.base_instance.children.append(self.sibling_instance)
        self.assertEqual(self.base_instance.get_child_by_id("child_id"), self.child_instance)

    def test_get_descendants(self):
        grandchild = MockBaseClass(_id="grandchild", _name="Grand Child")
        self.child_instance.children.append(grandchild)
        self.base_instance.children.append(self.child_instance)
        descendants = self.base_instance.get_descendants()
        self.assertIn(self.child_instance, descendants)
        self.assertIn(grandchild, descendants)

    def test_circular_reference_in_descendants(self):
        self.child_instance.children.append(self.base_instance)
        self.base_instance.children.append(self.child_instance)
        with self.assertRaises(C5decError) as context:
            self.base_instance.get_descendants()
        self.assertIn("Circular reference detected", str(context.exception))

    def test_get_parent(self):
        self.child_instance.parent = self.base_instance
        self.assertEqual(self.child_instance.get_parent(), self.base_instance)

    def test_get_ancestors(self):
        parent2 = MockBaseClass(_id="parent2", _name="Parent 2")
        self.base_instance.parent = parent2
        self.child_instance.parent = self.base_instance
        self.assertListEqual(self.child_instance.get_ancestors(), [self.base_instance, parent2])
    
    def test_get_ancestors_circular_reference(self):
        parent_instance = MockBaseClass(_id="parent_id", _name="parent_name")
        child_instance = MockBaseClass(_id="child_id", _name="child_name")
        grandchild_instance = MockBaseClass(_id="grandchild_id", _name="grandchild_name")

        child_instance.parent = parent_instance
        grandchild_instance.parent = child_instance
        parent_instance.parent = grandchild_instance
        with self.assertRaises(C5decError) as context:
            grandchild_instance.get_ancestors()
        self.assertIn("Circular reference detected", str(context.exception))

    def test_get_siblings(self):
        self.child_instance.parent = self.base_instance
        self.sibling_instance.parent = self.base_instance
        self.base_instance.children.extend([self.child_instance, self.sibling_instance])
        self.assertListEqual(self.child_instance.get_siblings(), [self.sibling_instance])

    def test_get_item_tree_basic(self):
        expected_tree = {"id": "test_id", "name": "test_name"}
        self.assertDictEqual(self.base_instance.get_item_tree(), expected_tree)

    def test_get_item_tree_with_children(self):
        # Adding children
        self.base_instance.children = [MockBaseClass(_id="test_id_2", _name="child1"), MockBaseClass(_id="test_id_3", _name="child2")]
        expected_tree = {"id": "test_id", "name": "test_name", "children": [{"id": "test_id_2", "name": "child1"},
                                                                          {"id": "test_id_3", "name": "child2"}]}
        self.assertDictEqual(self.base_instance.get_item_tree(), expected_tree)

    def test_get_item_tree_return_type(self):
        self.assertIsInstance(self.base_instance.get_item_tree(), dict)

    def test_get_item_tree_deeply_nested_structure(self):
        # Creating a deeply nested structure
        child = MockBaseClass(_id="test_id_1", _name="child1")
        child.children = [MockBaseClass(_id="test_id_1.1", _name="grandchild1")]
        self.base_instance.children = [MockBaseClass(_id="test_id_2", _name="child2"), child]

        expected_tree = {
            "id": "test_id", 
            "name": "test_name", 
            "children": [{"id": "test_id_2", "name": "child2"},
                         {"id": "test_id_1", "name": "child1", "children": [
                             {"id": "test_id_1.1", "name": "grandchild1"}]}]}
        self.assertDictEqual(self.base_instance.get_item_tree(), expected_tree)

    def test_get_item_tree_edge_cases(self):
        # Edge case: Empty _name
        self.base_instance._name = ""
        expected_tree = {"id": "test_id", "name": ""}
        self.assertDictEqual(self.base_instance.get_item_tree(), expected_tree)


if __name__ == "__main__":
    unittest.main()
