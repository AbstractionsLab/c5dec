import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os
# Add the parent directory to the sys.path so modules can be imported
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
from c5dec.core.cct import Operation, OperationBuilder, FEItem, FEItemBuilder, FEList, FEListBuilder, \
AElement, FElement, ParaSequence
from c5dec.common import C5decError

class TestOperation(unittest.TestCase):

    def setUp(self):
        self.functional_operation = Operation(_id='func1', op_type='selection', exclusive='NO')
        self.functional_operation.parent = MagicMock(FElement(_id="func_el_id"))
        self.assurance_operation = Operation(_id='ass1', op_type='selection')
        self.assurance_operation.parent = MagicMock(AElement(_id="ass_el_id", el_type="developer"))
    
    def test_init(self):
        self.assertEqual(self.functional_operation._id, 'func1')
        self.assertEqual(self.functional_operation.type, 'selection')
        self.assertEqual(self.functional_operation.exclusive, 'NO')

    def test_is_valid_with_valid_functional_operation(self):
        # Valid functional operation containes FEItems
        mock_item = MagicMock(FEItem())
        self.functional_operation.item = [mock_item]
        self.assertTrue(self.functional_operation.is_valid())

    def test_is_valid_with_valid_assurance_operation(self):
        # As per the provided method, this should return True without raising an exception.
        self.assertTrue(self.assurance_operation.is_valid())
    
    def test_is_valid_with_invalid_type(self):
        self.functional_operation.type = 'invalid_type'
        with self.assertRaises(C5decError) as context:
            self.functional_operation.is_valid()
        self.assertIn("invalid.", str(context.exception))

    def test_is_valid_with_invalid_functional_operation(self):
        with self.assertRaises(C5decError) as context:
            self.functional_operation.is_valid()
        self.assertIn("Operation must contain", str(context.exception))


class TestOperationBuilder(unittest.TestCase):
    
    def setUp(self):
        self.operation = Operation()
        self.builder = OperationBuilder(self.operation)

    def test_invalid_instance_type_raises_value_error(self):
        with self.assertRaises(C5decError):
            OperationBuilder("invalid_instance")

    def test_build_attributes(self):
        xml_string = '<Operation id="123" exclusive="NO"/>'
        node = etree.fromstring(xml_string)

        self.builder._build_attributes(node)

        self.assertEqual(self.operation._id, "123")
        self.assertEqual(self.operation.exclusive, "NO")
        
    def test_build_children_fe_assignmentitem(self):
        xml_string = '<Operation><fe-assignmentitem/></Operation>'
        node = etree.fromstring(xml_string)

        with patch.object(FEItemBuilder, 'build', return_value=FEItem()) as mock_build:
            self.builder._build_children(node[0])

        mock_build.assert_called_once()
        self.assertIsInstance(self.operation.item[0], FEItem)
        self.assertIsInstance(self.operation.container[0], FEItem)
        
    def test_build_children_fe_assignmentnotes(self):
        xml_string = '<Operation><fe-assignmentnotes/></Operation>'
        node = etree.fromstring(xml_string)

        with patch.object(ParaSequence, 'build', return_value=ParaSequence()) as mock_build:
            self.builder._build_children(node[0])

        mock_build.assert_called_once()
        self.assertIsInstance(self.operation.note, ParaSequence)
        self.assertIsInstance(self.operation.container[0], ParaSequence)

    def test_build_children_fe_list(self):
        xml_string = '<Operation><fe-list/></Operation>'
        node = etree.fromstring(xml_string)

        with patch.object(FEListBuilder, 'build', return_value=FEList()) as mock_build:
            self.builder._build_children(node[0])

        mock_build.assert_called_once()
        self.assertIsInstance(self.operation.container[0], FEList)

    def test_build(self):
        xml_string = '<Operation id="123" exclusive="NO"><fe-assignmentitem/></Operation>'
        node = etree.fromstring(xml_string)

        self.builder._build_attributes = MagicMock()
        self.builder._build_children = MagicMock()
        self.operation.is_valid = MagicMock()

        result = self.builder.build(node)

        self.builder._build_attributes.assert_called_once_with(node, None)
        self.builder._build_children.assert_called_once_with(node[0])
        self.operation.is_valid.assert_called_once()
        self.assertEqual(result, self.operation)


if __name__ == "__main__":
    unittest.main()
