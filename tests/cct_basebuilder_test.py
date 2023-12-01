import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
# Add the parent directory to the sys.path so modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
from c5dec.core.cct import BaseClass, BaseBuilder, Index

class MockBaseClass(BaseClass):
    def is_valid(self):
        pass  # Implement the abstract method is_valid for testing

class MockBaseBuilder(BaseBuilder):
    
    def _build_children(self, child):
        pass # Implement the abstract method _build_children for testing


class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.base_instance = MockBaseClass()
        self.base_builder = MockBaseBuilder(self.base_instance)

    def test_build_attributes(self):
        xml_string = '<Item id="123" name="TestItem"/>'
        node = etree.fromstring(xml_string)
        parent_obj = MockBaseClass(_id="parent_id", _name="parent_name")
        
        self.base_builder._build_attributes(node, parent_obj)
        
        self.assertEqual(self.base_instance._id, "123")
        self.assertEqual(self.base_instance._name, "TestItem")
        self.assertEqual(self.base_instance.parent, parent_obj)

    def test_build(self):
        xml_string = '''
        <Item id="123" name="TestItem">
            <ChildItem id="456" name="Child"/>
        </Item>
        '''
        node = etree.fromstring(xml_string)
        parent_obj = MockBaseClass(_id="parent_id", _name="parent_name")
        
        # Mocking methods to avoid actual calls and assert they were called correctly
        self.base_builder._build_attributes = MagicMock()
        self.base_builder._build_children = MagicMock()
        self.base_instance.is_valid = MagicMock()

        # assuming that _build_attributes correctly set the attributes
        self.base_instance._id = "123"
        self.base_instance._name = "TestItem"
        result = self.base_builder.build(node, parent_obj)
        
        # test that build methods were called
        self.base_builder._build_attributes.assert_called_once_with(node, parent_obj)
        self.base_builder._build_children.assert_called_once_with(node[0])

        # test that build returns the build instance.
        self.assertEqual(result, self.base_instance)

    def test_build_children_called_correctly(self):
        xml_string = '''
        <Item id="123" name="TestItem">
            <ChildItem id="456" name="Child"/>
            <ChildItem id="789" name="Child2"/>
        </Item>
        '''
        node = etree.fromstring(xml_string)

        # Mocking _build_children method
        with patch.object(MockBaseBuilder, '_build_children', return_value=None) as mock_method:
            self.base_builder.build(node)

            self.assertEqual(mock_method.call_count, len(node))

    def test_build_with_empty_xml(self):
        xml_string = ''
        with self.assertRaises(Exception): 
            node = etree.fromstring(xml_string)
            self.base_builder.build(node)
    
    def test_build_with_malformed_xml(self):
        xml_string = '<Item id="123" name=TestItem></Item>'
        with self.assertRaises(etree.XMLSyntaxError):  # lxml raises XMLSyntaxError for malformed XML
            node = etree.fromstring(xml_string)
            self.base_builder.build(node)
    
    def test_build_attributes_with_unexpected_attributes(self):
        xml_string = '<Item id="123" name="TestItem" unexpected_attr="unexpected"></Item>'
        node = etree.fromstring(xml_string)
        parent_obj = MockBaseClass(_id="parent_id", _name="parent_name")

        # Assume it ignores unexpected attributes without raising an exception
        try:
            self.base_builder._build_attributes(node, parent_obj)
        except Exception as e:
            self.fail(f"_build_attributes() raised {type(e)} unexpectedly!")
    
    def test_build_with_no_children(self):
        xml_string = '<Item id="TestID" name="TestItem"></Item>'
        node = etree.fromstring(xml_string)
        
        with patch.object(MockBaseBuilder, '_build_children', return_value=None) as mock_method:
            self.base_builder.build(node)
            mock_method.assert_not_called()
    
    def test_build_with_deeply_nested_xml(self):
        xml_string = '''
        <Item id="1" name="Item1">
            <ChildItem id="1.1" name="Child1">
                <ChildItem id="1.1.1" name="GrandChild1">
                    <ChildItem id="1.1.1.1" name="GrandGrandChild1"/>
                </ChildItem>
            </ChildItem>
            <ChildItem id="1.2" name="Child2">
                <ChildItem id="1.2.1" name="GrandChild2">
                    <ChildItem id="1.2.1.1" name="GrandGrandChild2">
                        <ChildItem id="1.2.1.1.1" name="GrandGrandGrandChild1"/>
                    </ChildItem>
                </ChildItem>
            </ChildItem>
            <ChildItem id="1.3" name="Child3">
                <ChildItem id="1.3.1" name="GrandChild3">
                    <ChildItem id="1.3.1.1" name="GrandGrandChild3"/>
                </ChildItem>
            </ChildItem>
        </Item>
        '''
        node = etree.fromstring(xml_string)
        
        with patch.object(MockBaseBuilder, '_build_children', return_value=None) as mock_method:
            self.base_builder.build(node)
            # Assert that _build_children is called 3 times (once for each child)
            self.assertEqual(mock_method.call_count, 3)

    def tearDown(self):
        Index.clear()

if __name__ == "__main__":
    unittest.main()
