import unittest
from unittest.mock import MagicMock, patch
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
import c5dec.core.cct as cct
from c5dec.common import C5decError

class TestFEItem(unittest.TestCase):
    
    def setUp(self):
        self.fe_item = cct.FEItem()

    def test_is_valid_raises_value_error_when_empty(self):
        with self.assertRaises(C5decError, msg="Object cannot be empty."):
            self.fe_item.is_valid()

    def test_is_valid_passes_when_non_empty(self):
        # Adding dummy object to container to make FEItem non-empty
        self.fe_item.container.append("Non-empty")
        try:
            self.fe_item.is_valid()
        except C5decError:
            self.fail("is_valid() raised C5decError unexpectedly!")

    def test_initial_container_empty(self):
        self.assertListEqual(self.fe_item.container, [], "Container should be initialized as empty.")

    def test_initial_list_empty(self):
        self.assertListEqual(self.fe_item.list, [], "List should be initialized as empty.")
        
    def test_initial_operation_empty(self):
        self.assertListEqual(self.fe_item.operation, [], "Operation should be initialized as empty.")

class TestFEItemBuilder(unittest.TestCase):

    def setUp(self):
        self.fe_item_instance = cct.FEItem()
        self.fe_item_builder = cct.FEItemBuilder(self.fe_item_instance)

    def test_init_raises_value_error_for_invalid_instance(self):
        with self.assertRaises(C5decError):
            cct.FEItemBuilder("Not an FEItem")

    def test_build_calls_is_valid(self):
        xml_string = "<fe-item/>"
        node = etree.fromstring(xml_string)
        
        self.fe_item_instance.is_valid = MagicMock()
        self.fe_item_builder.build(node)
        
        self.fe_item_instance.is_valid.assert_called_once()

    @patch.object(cct.FEItemBuilder, "build")
    @patch.object(cct.OperationBuilder, "build")
    def test_build_children_for_non_fe_list(self, mock_op_builder_build, mock_fe_item_builder_build):
        xml_string = "<fe-selectionitem/>"
        node = etree.fromstring(xml_string)

        # Set up the mocked build methods to return dummy instances
        mock_fe_item_builder_build.return_value = cct.FEItem()
        mock_op_builder_build.return_value = cct.Operation()

        self.fe_item_builder._build_children(node)
        
        # Ensure the build method on OperationBuilder is called
        mock_op_builder_build.assert_called_once()

    @patch.object(cct.FEItemBuilder, "build")
    @patch.object(cct.FEListBuilder, "build")
    def test_build_children_for_fe_list(self, mock_fe_list_builder_build, mock_fe_item_builder_build):
        xml_string = "<fe-list/>"
        node = etree.fromstring(xml_string)

        # Set up the mocked build methods to return dummy instances
        mock_fe_item_builder_build.return_value = cct.FEItem()
        mock_fe_list_builder_build.return_value = cct.FEList()
        
        self.fe_item_builder._build_children(node)
        
        # Ensure the build method on FEListBuilder is called
        mock_fe_list_builder_build.assert_called_once()

    def test_build_children_handles_text_and_tail(self):
        xml_string = '''
        <fe-selectionitem>
            Text content
            <fe-list> 
                List Text
                <fe-item>This is the item text</fe-item>
            </fe-list>
            Tail content
        </fe-selectionitem>
        '''
        node = etree.fromstring(xml_string)
        # Mock to avoid actual object build
        with patch.object(cct.FEItemBuilder, "build"), \
             patch.object(cct.FEListBuilder, "build"), \
             patch.object(cct.OperationBuilder, "build"):
            
            for child in node:
                self.fe_item_builder._build_children(child)
            # Check if text and tail content is appended to container
            text_contents = [elem.text for elem in self.fe_item_instance.container if isinstance(elem, cct.Text)]

            self.assertIn("List Text", ' '.join(text_contents))
            self.assertIn("Tail content", ' '.join(text_contents))


class TestFEList(unittest.TestCase):
    def setUp(self):
        self.fe_list = cct.FEList()

    def test_is_valid(self):
        # Test: FEList instance should not be valid when 'item' list is empty
        with self.assertRaises(C5decError) as context:
            self.fe_list.is_valid()
        self.assertIn("must contain items", str(context.exception))

        # Test: FEList instance should be valid when 'item' list is not empty
        self.fe_list.item.append("dummy_item")
        self.assertTrue(self.fe_list.is_valid())  # No exception should be raised

    def test_initialization(self):
        # Test: Check attributes after initialization
        self.assertIsNone(self.fe_list._id)
        self.assertIsNone(self.fe_list._name)
        self.assertEqual(self.fe_list.item, [])

class TestFEListBuilder(unittest.TestCase):
    def setUp(self):
        self.fe_list = cct.FEList()
        self.builder = cct.FEListBuilder(self.fe_list)

    def test_init_with_invalid_instance(self):
        # Test: Check initialization with invalid instance type
        with self.assertRaises(C5decError) as context:
            cct.FEListBuilder("InvalidInstance")
        self.assertIn("Object must be", str(context.exception))

    def test_build_attributes(self):
        # Mocked XML node
        node = MagicMock(spec=etree._Element)
        # Parent object mock
        parent_obj = MagicMock()

        # Test: Check if parent_obj is assigned to instance's parent attribute
        self.builder._build_attributes(node, parent_obj)
        self.assertEqual(self.fe_list.parent, parent_obj)

    def test_build_children(self):
        # XML string for creating a node
        xml_string = "<fe-item></fe-item>"
        node = etree.fromstring(xml_string)
        # Mock to avoid actual object build and method call
        with patch.object(cct.FEItemBuilder, "build", return_value="MockItem"):  # Replace path accordingly
            self.builder._build_children(node)
            # Check if mock item is appended to container and item of instance
            self.assertIn("MockItem", self.fe_list.container)
            self.assertIn("MockItem", self.fe_list.item)

    def test_build(self):
        # XML string for creating a node
        xml_string = "<fe-list><fe-item></fe-item></fe-list>"
        node = etree.fromstring(xml_string)
        # Mocks to avoid actual object build and method call
        with patch.object(cct.FEListBuilder,"_build_attributes"), \
             patch.object(cct.FEListBuilder,"_build_children"), \
             patch.object(cct.FEList, "is_valid"):
            built_instance = self.builder.build(node)
            # Check if instance is returned
            self.assertEqual(built_instance, self.fe_list)


class TestFElement(unittest.TestCase):
    
    def setUp(self):
        self.fe_element = cct.FElement(_id="FE1", _name="Functional Element 1")
        self.fe_element.container = [MagicMock(cct.Operation(op_type="selection")), 
                                     MagicMock(cct.Operation(op_type="assurance"))]

    def test_is_valid_success(self):
        # Test: Check is_valid returns True for proper FElement instance
        self.assertTrue(self.fe_element.is_valid())

    def test_is_valid_fail_on_empty(self):
        # Test: Check is_valid raises C5decError when instance is empty
        self.fe_element.container = []  # Assume it is empty now
        with self.assertRaises(C5decError):
            self.fe_element.is_valid()

class TestFElementBuilder(unittest.TestCase):
    
    def setUp(self):
        self.fe_element = cct.FElement(_id="FE1", _name="Functional Element 1")
        self.fe_element_builder = cct.FElementBuilder(instance=self.fe_element)

    def test_init_validates_instance_type(self):
        with self.assertRaises(C5decError):
            # Trying to initialize with an invalid instance type should raise a C5decError.
            cct.FElementBuilder(instance="invalid_instance")
    
    def test_build_children(self):
        xml_string = '''
        <fe-element>
            Element Text 1
            <fe-selection>
                <fe-selectionitem>SelItemA</fe-selectionitem>
                <fe-selectionitem>SelItemB</fe-selectionitem>
            </fe-selection><fe-list>
                <fe-item>ItemA</fe-item>
                <fe-item>ItemB</fe-item>
            </fe-list>
        </fe-element>
        '''
        node = etree.fromstring(xml_string)

        for child in node:
            self.fe_element_builder._build_children(child)

        container_types = [type(obj) for obj in self.fe_element.container]
        self.assertEqual(container_types, [cct.Text, cct.Operation, cct.FEList])

    def test_build_requirement(self):
        mock_text_1 = MagicMock(spec=cct.Text, text="This is ")
        mock_text_2 = MagicMock(spec=cct.Text, text="just a ")
        mock_text_3 = MagicMock(spec=cct.Text, text="simple test.")
    
        # Assign the mocks to the container attribute
        self.fe_element.container = [mock_text_1, mock_text_2, mock_text_3]

        self.fe_element_builder._build_requirement()
        self.assertEqual(self.fe_element.requirement, "This is just a simple test.")

    def test_build_children_handles_fe_list(self):
        # Creating a sample XML element that has 'fe-list' as a child node.
        xml_string = "<fe-element>Some text<fe-list/>Tail content</fe-element>"
        node = etree.fromstring(xml_string)

        # Mocking the build method of FEListBuilder to avoid actual building.
        with patch.object(cct.FEListBuilder, "build", return_value=cct.FEList()):
            self.fe_element_builder.build(node)

            # Check if fe_list is appended to container
            self.assertIsInstance(self.fe_element.container[-1], cct.FEList)

    def test_build_children_handles_text_and_tail(self):
        xml_string = '''
        <fe-element>
            <fe-selectionitem>
                Text content
                <fe-list> 
                    List Text
                    <fe-item>This is the item text</fe-item>
                </fe-list>
                Tail content
            </fe-selectionitem>
            Tail content.
        </fe-element>
        '''
        node = etree.fromstring(xml_string)
        # Mock to avoid actual object build
        with patch.object(cct.FEItemBuilder, "build"), \
             patch.object(cct.FEListBuilder, "build"), \
             patch.object(cct.OperationBuilder, "build"):
            
            for child in node:
                self.fe_element_builder._build_children(child)
            # Check if text and tail content is appended to container
            text_contents = [elem.text for elem in self.fe_element.container if isinstance(elem, cct.Text)]
            self.assertIn("Text content", ' '.join(text_contents))
            self.assertIn("Tail content", ' '.join(text_contents))


class TestFCoAudit(unittest.TestCase):

    def setUp(self):
        self.fco_audit = cct.FCoAudit(level="minimal")

    def test_is_valid_with_valid_instance(self):
            # Mocking is_empty method to return False.
            self.fco_audit.is_empty = lambda: False
            self.assertTrue(self.fco_audit.is_valid())
        
    def test_is_valid_with_invalid_level(self):
        # Assigning an invalid level
        self.fco_audit.level = "invalid_level"
        with self.assertRaises(C5decError):
            self.fco_audit.is_valid()

    def test_is_valid_with_empty_instance(self):
        # Mocking is_empty method to return True.
        self.fco_audit.is_empty = lambda: True
        with self.assertRaises(C5decError):
            self.fco_audit.is_valid()

class TestFCoAuditBuilder(unittest.TestCase):

    def setUp(self):
        self.fco_audit = cct.FCoAudit(level="minimal")
        self.builder = cct.FCoAuditBuilder(self.fco_audit)
        # Assuming you have a function `clean_string` in your module. If it's in another module, adjust accordingly.
        self.clean_string = cct.clean_string  

    def test_init_with_valid_instance(self):
        self.assertIsInstance(self.builder, cct.FCoAuditBuilder)

    def test_init_with_invalid_instance(self):
        with self.assertRaises(C5decError):
            cct.FCoAuditBuilder("Invalid instance")

    def test_build_attributes(self):
        xml_string = '''
        <fco-audit level="basic" equal="test_equal">
            Some Text.
        </fco-audit>
        '''
        node = etree.fromstring(xml_string)
        self.builder.build(node)

        self.assertEqual(self.fco_audit.level, "basic")
        self.assertEqual(self.fco_audit.isequal, "test_equal")
        
    def test_build_children_noop(self):
        # Since _build_children is a no-op, this is just to ensure it doesn't break existing functionality.
        self.builder._build_children(None)

    def test_build_with_isequal(self):
        xml_string = '''
        <fco-audit level="basic" equal="test_equal">
            Some Text.
        </fco-audit>
        '''
        node = etree.fromstring(xml_string)
        built_instance = self.builder.build(node)

        self.assertEqual(built_instance.text, "Equal to test_equal")
        self.assertEqual(built_instance.level, "basic")
        self.assertEqual(built_instance.isequal, "test_equal")

    def test_build_without_isequal(self):
        xml_string = '''
        <fco-audit level="basic">
            Some Text.
        </fco-audit>
        '''
        node = etree.fromstring(xml_string)
        built_instance = self.builder.build(node)

        self.assertEqual(built_instance.text, "Some Text.")
        self.assertEqual(built_instance.level, "basic")
        self.assertIsNone(built_instance.isequal)

    def test_build_invalid(self):
        node = MagicMock()
        node.text = "Some text"
        node.attrib = {"level": "invalid_level"}
        parent_obj = None

        with self.assertRaises(C5decError):
            self.builder.build(node, parent_obj)


class TestFCoManagement():
    """See TestFCoAudit"""

class TestFCoManagementBuilder():
    """See TestFCoAuditBuilder"""


class TestFComponent(unittest.TestCase):

    def setUp(self):
        self.component = cct.FComponent(_id='test_id', _name='test_name')

    def test_init(self):
        self.assertEqual(self.component._id, 'test_id')
        self.assertEqual(self.component._name, 'test_name')
        self.assertIsNone(self.component.fco_levelling)
        self.assertIsNone(self.component.audit)
        self.assertEqual(self.component.hierarchical, [])
        self.assertEqual(self.component.dependencies, [])

    def test_valid_component(self):
        self.component.fco_levelling = MagicMock()
        self.component.fco_levelling.original_tag = "fco-levelling"
        fake_element = MagicMock(cct.FElement)
        self.component.children = [fake_element]

        # Check if no exception is raised for a valid component
        self.assertTrue(self.component.is_valid())

    def test_missing_levelling(self):
        fake_element = MagicMock(cct.FElement)
        self.component.children = [fake_element]

        with self.assertRaises(C5decError):
            self.component.is_valid()

    def test_invalid_levelling_tag(self):
        self.component.fco_levelling = MagicMock()
        self.component.fco_levelling.original_tag = "invalid_tag"
        fake_element = MagicMock(cct.FElement)
        self.component.children = [fake_element]

        with self.assertRaises(C5decError):
            self.component.is_valid()

    def test_missing_children(self):
        self.component.fco_levelling = MagicMock()
        self.component.fco_levelling.original_tag = "fco-levelling"

        with self.assertRaises(C5decError):
            self.component.is_valid()

    def test_invalid_children_type(self):
        self.component.fco_levelling = MagicMock()
        self.component.fco_levelling.original_tag = "fco-levelling"
        self.component.children = [MagicMock()]  # Not an FElement instance

        with self.assertRaises(C5decError):
            self.component.is_valid()

class TestFComponentBuilder(unittest.TestCase):

    def setUp(self):
        self.component = cct.FComponent()
        self.builder = cct.FComponentBuilder(self.component)

    def test_init_valid_instance(self):
        self.assertIsInstance(self.builder, cct.FComponentBuilder)
        
    def test_init_invalid_instance(self):
        with self.assertRaises(C5decError):
            cct.FComponentBuilder("InvalidType")

    @patch.object(cct.FCoManagementBuilder, "build")  
    def test_build_children_management(self, mock_mgmt_build):
        xml_string = '''
        <fco-management>
            Some Component Management Text.
        </fco-management>
        '''
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        fco_mgmt = mock_mgmt_build(child)
        self.assertEqual(self.component.management, fco_mgmt)
        
    @patch.object(cct.FCoAuditBuilder, "build")
    def test_build_children_audit(self, mock_audit_build):
        xml_string = '''
        <fco-audit>
            Some Component Audit Text.
        </fco-audit>
        '''
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        fco_audit = mock_audit_build(child)
        self.assertEqual(self.component.audit, fco_audit)

    @patch.object(cct.FElementBuilder, "build") 
    def test_build_children_element(self, mock_felement_build):
        xml_string = '''
        <f-element>
            Some Element Text.
        </f-element>
        '''
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        f_element = mock_felement_build(child)

        self.assertEqual(self.component.children[0], f_element)

    def test_build_children_parasequence_objects(self):
        child = MagicMock()
        child.tag = "fco-rationale"
        self.builder._build_children(child)
        self.assertIsInstance(self.component.fco_rationale, cct.ParaSequence)

    def test_build_children_hierarchical(self):
        child = MagicMock()
        child.tag = "fco-hierarchical"
        child.get.return_value = "TEST_COMPONENT"
        self.builder._build_children(child)
        self.assertEqual(["TEST_COMPONENT"], self.component.hierarchical)

    def test_build_children_dependencies(self):
        child = MagicMock()
        child.tag = "fco-dependencies"
        mock_component = MagicMock(etree._Element)
        mock_component.get.return_value ="TEST_COMPONENT"
        child.__iter__.return_value = [mock_component]
        self.builder._build_children(child)
        self.assertEqual(["TEST_COMPONENT"], self.component.dependencies)

    def test_build_children_or_dependencies(self):
        child = MagicMock()
        child.tag = "fco-dependencies"
        grandchild = MagicMock()
        grandchild.tag = "fco-or"
        mock_component = MagicMock(etree._Element)
        mock_component.get.return_value ="TEST_COMPONENT"
        grandchild.__iter__.return_value = [mock_component]
        child.__iter__.return_value = [grandchild]
        self.builder._build_children(child)
        self.assertEqual([["TEST_COMPONENT"]], self.component.dependencies)

    def test_build_children_without_dependencies(self):
        child = MagicMock()
        grandchild = MagicMock()
        grandchild.get.retun_value = None
        child.__iter__.return_value = [grandchild]
        self.builder._build_children(child)
        self.assertEqual([], self.component.dependencies)


class TestFFamily(unittest.TestCase):

    def setUp(self):
        self.ffamily = cct.FFamily(_id="ID001", _name="TestFamily")

    def test_initialization(self):
        self.assertEqual(self.ffamily._id, "ID001")
        self.assertEqual(self.ffamily._name, "TestFamily")
        self.assertIsNone(self.ffamily.ff_behaviour)
        self.assertIsNone(self.ffamily.ff_application_notes)
        self.assertIsNone(self.ffamily.ff_user_notes)
        self.assertIsNone(self.ffamily.ff_evaluator_notes)
        self.assertEqual(self.ffamily.children, [])

    def test_is_valid_valid_id_and_name(self):
        self.ffamily.has_valid_id = MagicMock(return_value=True)
        self.ffamily.has_valid_name = MagicMock(return_value=True)
        self.ffamily.children = [MagicMock(cct.FComponent)]
        self.ffamily.ff_behaviour = MagicMock()
        self.ffamily.ff_behaviour.original_tag = "ff-behaviour"
        self.assertTrue(self.ffamily.is_valid())

    def test_is_valid_missing_behaviour(self):
        self.ffamily.ff_behaviour = None
        with self.assertRaises(C5decError) as context:
            self.ffamily.is_valid()
        self.assertIn("is missing family behaviour.", str(context.exception))

    def test_is_valid_wrong_original_tag_behaviour(self):
        self.ffamily.ff_behaviour = MagicMock()
        self.ffamily.ff_behaviour.original_tag = "other-tag"
        with self.assertRaises(C5decError) as context:
            self.ffamily.is_valid()
        self.assertIn("is missing family behaviour.", str(context.exception))

    def test_is_valid_no_children(self):
        self.ffamily.children = []
        self.ffamily.ff_behaviour = MagicMock()
        self.ffamily.ff_behaviour.original_tag = "ff-behaviour"
        with self.assertRaises(C5decError) as context:
            self.ffamily.is_valid()
        self.assertIn("must contain child elements of type", str(context.exception))

    def test_is_valid_wrong_child_type(self):
        self.ffamily.children = [MagicMock()]  # A mock that isn't an FComponent
        self.ffamily.ff_behaviour = MagicMock()
        self.ffamily.ff_behaviour.original_tag = "ff-behaviour"
        with self.assertRaises(C5decError) as context:
            self.ffamily.is_valid()
        self.assertIn("must contain child elements of type", str(context.exception))

class TestFFamilyBuilder(unittest.TestCase):

    def setUp(self):
        self.ffamily_instance = cct.FFamily(_id="ID001", _name="TestFamily")
        self.builder = cct.FFamilyBuilder(self.ffamily_instance)

    def test_initialization(self):
        self.assertEqual(self.builder.instance, self.ffamily_instance)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.FFamilyBuilder("NotAnFFamilyInstance")

    @patch.object(cct.ParaSequence, 'build')
    @patch.object(cct.FFamily, '__setattr__')
    def test_build_children_para_sequence_objects(self, mock_setattr, mock_build):
        # Creating a dummy xml element
        xml_string = '<ff-behaviour>Test Behaviour Text</ff-behaviour>'
        child = etree.fromstring(xml_string)
        
        # Mocking the build method to return a dummy ParaSequence object
        dummy_parasequence = cct.ParaSequence()
        mock_build.return_value = dummy_parasequence

        self.builder._build_children(child)
        
        mock_build.assert_called_once_with(child, self.builder.instance)
        mock_setattr.assert_called_once_with('ff_behaviour', dummy_parasequence)
        self.assertIn(dummy_parasequence, self.builder.instance.container)

    @patch.object(cct.FComponentBuilder, 'build')
    def test_build_children_f_component(self, mock_build):
        xml_string = '<f-component></f-component>'
        child = etree.fromstring(xml_string)
        
        dummy_fcomponent = cct.FComponent()
        mock_build.return_value = dummy_fcomponent

        self.builder._build_children(child)
        
        mock_build.assert_called_once_with(child, self.builder.instance)
        self.assertIn(dummy_fcomponent, self.builder.instance.children)
        

class TestFClass(unittest.TestCase):
    
    def setUp(self):
        self.fclass = cct.FClass(_id="ID001", _name="TestClass")

    def test_initialization(self):
        self.assertEqual(self.fclass._id, "ID001")
        self.assertEqual(self.fclass._name, "TestClass")
        self.assertIsNone(self.fclass.fc_introduction)
        self.assertIsNone(self.fclass.fc_informative_notes)

    def test_valid_case(self):
        mock_intro = MagicMock(cct.ParaSequence())
        mock_intro.original_tag = "fc-introduction"
        self.fclass.fc_introduction = mock_intro
        mock_note = MagicMock(cct.ParaSequence())
        mock_note.original_tag = "fc-informative-notes"
        self.fclass.fc_informative_notes = mock_note
        self.fclass.children.append(MagicMock(cct.FFamily()))
        self.assertTrue(self.fclass.is_valid())
    
    def test_missing_fc_introduction(self):
        self.fclass.fc_introduction = None
        
        with self.assertRaises(C5decError):
            self.fclass.is_valid()

    def test_invalid_fc_introduction(self):
        mock_intro = MagicMock(cct.ParaSequence())
        mock_intro.original_tag = "invalid-tag"
        self.fclass.fc_introduction = mock_intro

        with self.assertRaises(C5decError):
            self.fclass.is_valid()

    def test_missing_fc_informative_notes(self):
        self.fclass.fc_informative_notes = None
        
        with self.assertRaises(C5decError):
            self.fclass.is_valid()

    def test_invalid_fc_informative_notes(self):
        mock_note = MagicMock(cct.ParaSequence())
        mock_note.original_tag = "invalid-tag"
        self.fclass.fc_informative_notes = mock_note
        
        with self.assertRaises(C5decError):
            self.fclass.is_valid()
    
    def test_missing_children(self):
        mock_intro = MagicMock(cct.ParaSequence())
        mock_intro.original_tag = "fc-introduction"
        self.fclass.fc_introduction = mock_intro
        mock_note = MagicMock(cct.ParaSequence())
        mock_note.original_tag = "fc-informative-notes"
        self.fclass.fc_informative_notes = mock_note
        self.fclass.children = []
        
        with self.assertRaises(C5decError):
            self.fclass.is_valid()
    
    def test_invalid_children_type(self):
        mock_intro = MagicMock(cct.ParaSequence())
        mock_intro.original_tag = "fc-introduction"
        self.fclass.fc_introduction = mock_intro
        mock_note = MagicMock(cct.ParaSequence())
        mock_note.original_tag = "fc-informative-notes"
        self.fclass.fc_informative_notes = mock_note
        self.fclass.children = ["InvalidChildType"]
        
        with self.assertRaises(C5decError):
            self.fclass.is_valid()

class TestFClassBuilder(unittest.TestCase):

    def setUp(self):
        self.fclass_instance = cct.FClass(_id="ID001", _name="TestClass")
        self.builder = cct.FClassBuilder(self.fclass_instance)

    def test_initialization(self):
        self.assertEqual(self.builder.instance, self.fclass_instance)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.FClassBuilder("NotAnFClassInstance")

    @patch.object(cct.ParaSequence, 'build')
    @patch.object(cct.FClass, '__setattr__')
    def test_build_children_para_sequence_objects(self, mock_setattr, mock_build):
        # Creating a dummy xml element
        xml_string = '<fc-introduction>Some Class Introduction.</fc-introduction>'
        child = etree.fromstring(xml_string)
        
        # Mocking the build method to return a dummy ParaSequence object
        dummy_parasequence = cct.ParaSequence()
        mock_build.return_value = dummy_parasequence

        self.builder._build_children(child)
        
        mock_build.assert_called_once_with(child, self.builder.instance)
        mock_setattr.assert_called_once_with('fc_introduction', dummy_parasequence)
        self.assertIn(dummy_parasequence, self.builder.instance.container)

    @patch.object(cct.FFamilyBuilder, 'build')
    def test_build_children_f_family(self, mock_build):
        xml_string = '<f-family></f-family>'
        child = etree.fromstring(xml_string)
        
        dummy_ffamily = cct.FFamily()
        mock_build.return_value = dummy_ffamily

        self.builder._build_children(child)
        
        mock_build.assert_called_once_with(child, self.builder.instance)
        self.assertIn(dummy_ffamily, self.builder.instance.children)



if __name__ == "__main__":
    unittest.main()

