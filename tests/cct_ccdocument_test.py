import unittest
from unittest.mock import MagicMock, patch
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from lxml import etree
from c5dec.core.cct import CCDocument, CCDocumentBuilder
import c5dec.core.cct as cct
from c5dec.common import C5decError, C5decWarning

class TestCCDocument(unittest.TestCase):

    def setUp(self):
        self.doc = CCDocument()
        self.doc.version = "3"
        self.doc.revision = "5"
        self.doc.clause = [MagicMock(cct.Clause())]
        self.doc.f_class = [MagicMock(cct.FClass(_id="fclass_id", _name="fclass_name"))]
        self.doc.a_class = [MagicMock(cct.AClass(_id="aclass_id", _name="aclass_name"))]
        self.doc.eal = [MagicMock(cct.Package(_id="eal1"))]
        self.doc.cap = [MagicMock(cct.Package(_id="cap1"))]

    def test_is_valid(self):
        self.assertTrue(self.doc.is_valid())

    def test_missing_attributes_raises_warning(self):
        self.doc.f_class = []
        with self.assertRaises(C5decWarning):
            self.doc.is_valid()
    
    def test_missing_version_raises_attribute(self):
        self.doc.version = ""
        with self.assertRaises(C5decError):
            self.doc.is_valid()

    def test_missing_revision_raises_attribute(self):
        self.doc.revision = ""
        with self.assertRaises(C5decError):
            self.doc.is_valid()

class TestAClassBuilder(unittest.TestCase):

    def setUp(self):
        self.doc = MagicMock(CCDocument())
        self.builder = CCDocumentBuilder(self.doc)

    def test_initialization(self):
        self.assertIsInstance(self.builder.instance, CCDocument)

    def test_initialization_wrong_instance_type(self):
        with self.assertRaises(C5decError):
            CCDocumentBuilder("INVALIDELEMENT")

    def test_build_attributes(self):
        xml_string = '''
        <cc version="5" revision="5" lang="en"/>
        '''
        node = etree.fromstring(xml_string)
        self.builder._build_attributes(node)

        self.assertEqual(self.doc._id, "CCv5R5")
        self.assertEqual(self.doc.lang, "en")

    @patch.object(cct.Clause, "build")
    @patch.object(cct.FClassBuilder, "build")
    @patch.object(cct.AClassBuilder, "build")
    def test_build_children(self, MockABuilder, MockFBuilder, MockClause):
        xml_string = '''
        <cc version="5" revision="5" lang="en">
            <clause title="Some Title"/>
            <f-class id="fclass_id" name="fclass_name"/>
            <a-class id="aclass_id" name="aclass_name"/>
        </cc>
        '''
        node = etree.fromstring(xml_string)
        for child in node:
            self.builder._build_children(child)
        
        MockClause.assert_called_once()
        MockFBuilder.assert_called_once()
        MockABuilder.assert_called_once()

        self.assertTrue(all([self.doc.clause, self.doc.f_class, self.doc.a_class]))

    @patch.object(CCDocumentBuilder, "_build_attributes")
    @patch.object(CCDocumentBuilder, "_build_children")
    def test_build(self, MockBuildChildren, MockBuildAttrib):
        xml_string = '''
        <cc version="5" revision="5" lang="en">
            <clause title="Some Title"/>
        </cc>
        '''
        node = etree.fromstring(xml_string)
        result = self.builder.build(node)
        
        MockBuildAttrib.assert_called_once_with(node)
        MockBuildChildren.assert_called_once_with(list(node)[0])

        self.assertEqual(result, self.doc)


if __name__ == "__main__":
    unittest.main()