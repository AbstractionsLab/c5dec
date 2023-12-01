import unittest
from unittest.mock import MagicMock, patch
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
import c5dec.core.cct as cct
from c5dec.common import C5decError


class TestDCElement(unittest.TestCase):
    """not necessary"""


class TestWorkUnit(unittest.TestCase):

    def setUp(self):
        self.work_unit = cct.WorkUnit(_id="unit_id", _name="unit_name")
        self.work_unit.dc_element = "elem_id"

    def test_is_valid_with_valid_instance(self):
        self.work_unit.container = [MagicMock(cct.Text())]
        self.assertTrue(self.work_unit.is_valid())

    def test_is_valid_with_invalid_instance(self):
        with self.assertRaises(C5decError):
            self.work_unit.is_valid()

class TestWorkUnitBuilder(unittest.TestCase):

    def setUp(self):
        self.work_unit = cct.WorkUnit(_id="unit_id", _name="unit_name")
        self.builder = cct.WorkUnitBuilder(self.work_unit)

    def test_initialization(self):
        self.assertEqual(self.builder.instance, self.work_unit)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.WorkUnitBuilder("NotAWorkUnitInstance")

    def test_build_attributes_with_id(self):
        node = MagicMock(etree._Element)
        node.get.return_value = "new_id"
        parent_obj = MagicMock()
        self.builder._build_attributes(node, parent_obj)

        self.assertEqual(self.work_unit._id, "new_id")

    def test_build_attributes_without_id(self):
        node = MagicMock(etree._Element)
        node.get.return_value = None
        parent_obj = MagicMock()
        parent_obj._id = "AVA_VAN.1.1"
        self.builder._build_attributes(node, parent_obj)
        self.assertEqual(self.work_unit._id, "AVA_VAN.1-1")

    def test_build_children_ae_dc_element(self):
        xml_string = "<ae-dc-element id='elem_id'/>"
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        self.assertEqual(self.work_unit.dc_element[0]._id, "elem_id")

    @patch.object(cct.Para, "build")
    def test_build_children_para(self, mock_para_build):
        xml_string = "<para> Para Text.</para>"
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        para = mock_para_build(child)

        self.assertIn(para, self.work_unit.container)

    @patch.object(cct.SubClause, "build")
    def test_build_children_subclause(self, mock_subclause_build):
        xml_string = "<subclause> Subclause Text.</subclause>"
        child = etree.fromstring(xml_string)
        self.builder._build_children(child)
        subclause = mock_subclause_build(child)

        self.assertIn(subclause, self.work_unit.container)


class TestAElement(unittest.TestCase):

    def setUp(self):
        self.aelement = cct.AElement(_id="AE1", el_type="evaluator")
        self.aelement.container = [MagicMock(cct.Operation(op_type="selection")), 
                                   MagicMock(cct.Operation(op_type="assurance"))]
        
    def test_is_valid_success(self):
        # Test: Check is_valid returns True for proper FElement instance
        self.assertTrue(self.aelement.is_valid())

    def test_is_valid_invalid_type(self):
        self.aelement.type = "InvalidType"
        with self.assertRaises(C5decError):
            self.aelement.is_valid()

    def test_is_valid_fail_on_empty(self):
        # Test: Check is_valid raises C5decError when instance is empty
        self.aelement.container = []  # Assume it is empty now
        with self.assertRaises(C5decError):
            self.aelement.is_valid()

class TestAElementBuilder(unittest.TestCase):

    def setUp(self):
        self.aelement = cct.AElement(_id='valid_id', el_type='developer')
        self.builder = cct.AElementBuilder(self.aelement)

    def test_init_with_valid_aelement(self):
        self.assertIsInstance(self.builder, cct.AElementBuilder)

    def test_init_with_invalid_aelement_raises_value_error(self):
        with self.assertRaises(C5decError):
            cct.AElementBuilder("INVALIDELEMENT")

    def test_build_attributes_sets_id(self):
        node = MagicMock()
        node.attrib = {"id": "new_id"}
        node.get.return_value = node.attrib["id"]
        self.builder._build_attributes(node)
        self.assertEqual(self.aelement._id, "new_id")

    @patch.object(cct.List, "build")
    def test_build_children_list(self, mock_build):
        node = MagicMock()
        node.tag = 'list'
        self.builder._build_children(node)
        mocked= mock_build(node)
        self.assertEqual(self.aelement.list[0], mocked)

    @patch.object(cct.OperationBuilder, "build")
    def test_build_children_operation(self, mock_build):
        node = MagicMock()
        node.tag = 'selection'
        self.builder._build_children(node)
        mocked = mock_build(node)
        self.assertEqual(self.aelement.operation[0], mocked)

    @patch.object(cct.XRef, "build")
    def test_build_children_operation(self, mock_build):
        node = MagicMock()
        node.tag = 'xref'
        self.builder._build_children(node)
        mocked = mock_build(node)
        self.assertIn(mocked, self.aelement.container)

    @patch.object(cct.WorkUnitBuilder, "build")
    def test_build_children_operation(self, mock_build):
        node = MagicMock()
        node.tag = 'm-workunit'
        self.builder._build_children(node)
        mocked = mock_build(node)
        self.assertIn(mocked, self.aelement.children)

    def test_build_attributes_is_called(self):
        self.builder._build_attributes = MagicMock()
        node = MagicMock(etree._Element)
        node.text = "SOME NODE TEXT."
        self.builder.build(node)
        self.builder._build_attributes.assert_called_once_with(node, None)

    def test_build_children_is_called_for_each_child(self):
        self.builder._build_children = MagicMock()
        node = MagicMock(etree._Element)
        node.text = "SOME NODE TEXT."
        child1 = MagicMock(etree._Element)
        child1.text = "SOME CHILD NODE TEXT."
        child2 = MagicMock(etree._Element)
        child2.text = "SOME CHILD NODE TEXT."
        node.__iter__.return_value = iter([child1, child2])
        self.builder.build(node)
        self.assertEqual(self.builder._build_children.call_count, 2)

    def test_requirement_is_updated_with_text(self):
        node = MagicMock(etree._Element)
        node.text = "SOME NODE TEXT."
        self.builder.build(node)
        self.assertNotEqual(self.aelement.requirement, "SOME NODE TEXT.")

    def test_text_is_added_to_container(self):
        node = MagicMock(etree._Element)
        node.text = "SOME NODE TEXT."
        self.builder.build(node)
        self.assertGreater(len(self.aelement.container), 0)
        self.assertIsInstance(self.aelement.container[-1], cct.Text)

    def test_returns_instance(self):
        node = MagicMock(etree._Element)
        node.text = "SOME NODE TEXT."
        instance = self.builder.build(node)
        self.assertEqual(instance, self.aelement)

    def tearDown(self):
        cct.Index.clear()

class TestAComponent(unittest.TestCase):

    def setUp(self):
        self.acomponent = cct.AComponent(_id="test_id", _name="test_name")
        self.acomponent.children = [MagicMock(cct.AElement())]

    def test_valid_child_type(self):
        self.assertTrue(self.acomponent.is_valid())

    def test_invalid_child_type_raises_error(self):
        self.acomponent.children.append("InvalidChildType")
        with self.assertRaises(C5decError):
            self.acomponent.is_valid()

class TestAComponentBuilder(unittest.TestCase):

    def setUp(self):
        self.acomponent = cct.AComponent(_id='valid_id', _name='valid_name')
        self.builder = cct.AComponentBuilder(self.acomponent)

    def test_initialization(self):
        self.assertIsInstance(self.builder.instance, cct.AComponent)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.AComponentBuilder("INVALIDELEMENT")

    @patch.object(cct.ParaSequence, "build")
    def test_build_children_parasequence(self, mock_parasequence_build):

        xml_string = '''
        <a-component>
            <aco-objectives>
                Component Objective.
            </aco-objectives>
            <aco-application-notes>
                Component Application Notes.
            </aco-application-notes>
            <msa-objectives>
                Evaluation Sub-activity Objective.
            </msa-objectives>
            <msa-application-notes>
                Evaluation Sub-activity Appplication Notes.
            </msa-application-notes>
            <msa-input>
                Evaluation Sub-activtiy input.
            </msa-input>
        </a-component>
        '''

        node = etree.fromstring(xml_string)
        mocked_parasequence = []
        for child in node:
            self.builder._build_children(child)
            mocked_parasequence.append(mock_parasequence_build(child))
        
        self.assertEqual(mocked_parasequence, self.acomponent.container)

    def test_build_children_hierarchical(self):
        xml_string = '''
        <a-component>
            <aco-hierarchical acomponent="Comp_Id.1"/>
        </a-component>
        '''
        node = etree.fromstring(xml_string)
        for child in node:
            self.builder._build_children(child)

        self.assertEqual(self.acomponent.hierarchical, ["Comp_Id.1"])
    
    def test_build_children_dependencies(self):
        xml_string = '''
        <a-component>
            <aco-dependsoncomponent acomponent="Comp_Id.2"/>
        </a-component>
        '''
        node = etree.fromstring(xml_string)
        for child in node:
            self.builder._build_children(child)

        self.assertEqual(self.acomponent.dependencies, ["Comp_Id.2"])

    @patch.object(cct.AElementBuilder, "build")
    def test_build_children_element(self, mock_element_build):
        xml_string = '''
        <a-component>
            <ae-developer>
                Developer Action Element.
            </ae-developer>
            <ae-content>
                Content and Presentation Element.
            </ae-content>
            <ae-evaluator>
                Evaluator Action Element.
            </ae-evaluator>
        </a-component>
        '''
        node = etree.fromstring(xml_string)
        mocked_elements = []
        for child in node:
            self.builder._build_children(child)
            mocked_elements.append(mock_element_build(child))

        self.assertEqual(mocked_elements, self.acomponent.children)


class TestAFamily(unittest.TestCase):

    def setUp(self):
        self.afamily = cct.AFamily(_id="test_id", _name="test_name")
        self.afamily.children = [MagicMock(cct.AComponent())]

    def test_valid_child_type(self):
        self.assertTrue(self.afamily.is_valid())

    def test_invalid_child_type_raises_error(self):
        self.afamily.children.append("InvalidChildType")
        with self.assertRaises(C5decError):
            self.afamily.is_valid()

class TestAFamilyBuilder(unittest.TestCase):

    def setUp(self):
        self.afamily = cct.AFamily(_id='valid_id', _name='valid_name')
        self.builder = cct.AFamilyBuilder(self.afamily)

    def test_initialization(self):
        self.assertIsInstance(self.builder.instance, cct.AFamily)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.AFamilyBuilder("INVALIDELEMENT")

    @patch.object(cct.ParaSequence, "build")
    def test_build_children_parasequence(self, mock_parasequence_build):

        xml_string = '''
        <a-family>
            <af-objectives>
                Family Objective.
            </af-objectives>
            <af-overview>
                Family Overview.
            </af-overview>
            <af-levelling-criteria>
                Family Levelling Criteria
            </af-levelling-criteria>
            <af-application-notes>
                Family Appplication Notes.
            </af-application-notes>
        </a-family>
        '''

        node = etree.fromstring(xml_string)
        mocked_parasequence = []
        for child in node:
            self.builder._build_children(child)
            mocked_parasequence.append(mock_parasequence_build(child))
        
        self.assertEqual(mocked_parasequence, self.afamily.container)

    @patch.object(cct.AComponentBuilder, "build")
    def test_build_children_component(self, mock_component_build):
        xml_string = '''
        <a-family>
            <a-component id="Comp_id1" name="Comp_name1">
                Component text
                <ae-developer/>
                <ae-content/>
                <ae-evaluator/>
            </a-component>
            <a-component id="Comp_id2" name="Comp_name2">
                Component text
                <ae-developer/>
                <ae-content/>
                <ae-evaluator/>
            </a-component>
        </a-family>
        '''
        node = etree.fromstring(xml_string)
        mocked_elements = []
        for child in node:
            self.builder._build_children(child)
            mocked_elements.append(mock_component_build(child))

        self.assertEqual(mocked_elements, self.afamily.children)


class TestAClass(unittest.TestCase):

    def setUp(self):
        self.aclass = cct.AClass(_id="test_id", _name="test_name")
        self.aclass.children = [MagicMock(cct.AFamily())]
        self.aclass.ac_introduction = MagicMock(cct.ParaSequence())
        self.aclass.ac_introduction.original_tag = "ac-introduction"

    def test_is_valid(self):
        self.assertTrue(self.aclass.is_valid())

    def test_invalid_child_type_raises_error(self):
        self.aclass.children.append("InvalidChildType")
        with self.assertRaises(C5decError):
            self.aclass.is_valid()

    def test_missing_introduction_raises_error(self):
        self.aclass.ac_introduction = None
        with self.assertRaises(C5decError):
            self.aclass.is_valid()

class TestAClassBuilder(unittest.TestCase):

    def setUp(self):
        self.aclass = cct.AClass(_id='valid_id', _name='valid_name')
        self.builder = cct.AClassBuilder(self.aclass)

    def test_initialization(self):
        self.assertIsInstance(self.builder.instance, cct.AClass)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            cct.AClassBuilder("INVALIDELEMENT")

    @patch.object(cct.ParaSequence, "build")
    def test_build_children_parasequence(self, mock_parasequence_build):

        xml_string = '''
        <a-class>
            <ac-introduction>
                Class Introduction.
            </ac-introduction>
            <ac-overview>
                Class Overview.
            </ac-overview>
            <ac-application-notes>
                Class Application Notes.
            </ac-application-notes>
            <ma-introduction>
                Evaluation Activtiy Introduction.
            </ma-introduction>
            <ma-objectives>
                Evaluation Activity Objective.
            </ma-objectives>
            <ma-application-notes>
                Evaluation activity Appplication Notes.
            </ma-application-notes>
        </a-class>
        '''

        node = etree.fromstring(xml_string)
        mocked_parasequence = []
        for child in node:
            self.builder._build_children(child)
            mocked_parasequence.append(mock_parasequence_build(child))
        
        self.assertEqual(mocked_parasequence, self.aclass.container)

    @patch.object(cct.AFamilyBuilder, "build")
    def test_build_children_family(self, mock_family_build):
        xml_string = '''
        <a-class>
            <a-family id="Family_id" name="Family_name">
                Family.
            </a-family>
        </a-class>
        '''
        node = etree.fromstring(xml_string)
        mocked_elements = []
        for child in node:
            self.builder._build_children(child)
            mocked_elements.append(mock_family_build(child))

        self.assertEqual(mocked_elements, self.aclass.children)

if __name__ == "__main__":
    unittest.main()