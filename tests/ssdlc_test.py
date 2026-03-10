import os
import shutil
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import c5dec.core.ssdlc as ssdlc
import c5dec.settings as c5settings


class TestCreateDocengineTemplate(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_invalid_template_type_returns_false(self):
        result = ssdlc.create_docengine_template("invalid_type", "myproject", destination=self.tmp)
        self.assertFalse(result)

    @patch("c5dec.core.ssdlc.shutil.copytree")
    @patch("c5dec.core.ssdlc.shutil.make_archive")
    def test_report_template_returns_true(self, mock_archive, mock_copy):
        dest = os.path.join(self.tmp, "report_output")
        result = ssdlc.create_docengine_template("report", "testreport", destination=dest)
        mock_copy.assert_called_once()
        mock_archive.assert_called_once()
        self.assertTrue(result)

    @patch("c5dec.core.ssdlc.shutil.copytree")
    @patch("c5dec.core.ssdlc.shutil.make_archive")
    def test_presentation_template_returns_true(self, mock_archive, mock_copy):
        dest = os.path.join(self.tmp, "pres_output")
        result = ssdlc.create_docengine_template("presentation", "testpres", destination=dest)
        mock_copy.assert_called_once()
        mock_archive.assert_called_once()
        self.assertTrue(result)

    @patch("c5dec.core.ssdlc.shutil.copytree")
    @patch("c5dec.core.ssdlc.shutil.make_archive")
    def test_cra_tech_doc_template_returns_true(self, mock_archive, mock_copy):
        dest = os.path.join(self.tmp, "cra_output")
        result = ssdlc.create_docengine_template("cra-tech-doc", "testcra", destination=dest)
        mock_copy.assert_called_once()
        mock_archive.assert_called_once()
        self.assertTrue(result)

    def test_existing_destination_returns_false(self):
        dest = os.path.join(self.tmp, "exists")
        os.makedirs(dest)
        result = ssdlc.create_docengine_template("report", "testreport", destination=dest)
        self.assertFalse(result)

    @patch("c5dec.core.ssdlc.shutil.copytree", side_effect=OSError("disk full"))
    def test_copytree_failure_returns_false(self, mock_copy):
        dest = os.path.join(self.tmp, "fail_output")
        result = ssdlc.create_docengine_template("report", "failreport", destination=dest)
        self.assertFalse(result)


class TestArtifactRepositoryFunctions(unittest.TestCase):

    def _make_mock_tree(self):
        mock_tree = MagicMock()
        mock_document = MagicMock()
        mock_item = MagicMock()
        mock_item.uid = "REQ-001"
        mock_item.links = [MagicMock(string="SRS-001")]
        mock_document.items = [mock_item]
        mock_tree.find_document.return_value = mock_document
        mock_tree.find_item.return_value = mock_item
        return mock_tree, mock_document, mock_item

    @patch("c5dec.core.ssdlc.doorstop.build")
    def test_get_artifact_repository_returns_document(self, mock_build):
        mock_tree, mock_doc, _ = self._make_mock_tree()
        mock_build.return_value = mock_tree
        result = ssdlc.get_artifact_repository("REQ")
        mock_tree.find_document.assert_called_once_with("REQ")
        self.assertEqual(result, mock_doc)

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_get_item_text_returns_text(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        mock_item.text = "Some requirement text"
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        result = ssdlc.get_item_text("REQ-001")
        self.assertEqual(result, "Some requirement text")

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_set_item_text_updates_item(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        ssdlc.set_item_text("REQ-001", "New text")
        self.assertEqual(mock_item.text, "New text")

    # TST-026
    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_link_child_to_parent_calls_link(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_get_tree.return_value = mock_tree
        ssdlc.link_child_item_to_parent("SRS-001", "REQ-001")
        mock_tree.link_items.assert_called_once_with("SRS-001", "REQ-001")

    # TST-026
    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_unlink_child_calls_unlink(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_get_tree.return_value = mock_tree
        ssdlc.unlink_child_item_to_parent("SRS-001", "REQ-001")
        mock_tree.unlink_items.assert_called_once_with("SRS-001", "REQ-001")

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_get_item_links_returns_uid_strings(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        link1 = MagicMock()
        link1.string = "SRS-001"
        link2 = MagicMock()
        link2.string = "SRS-002"
        mock_item.links = [link1, link2]
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        result = ssdlc.get_item_links("REQ-001")
        self.assertEqual(result, ["SRS-001", "SRS-002"])

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_add_item_calls_document_add(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_get_tree.return_value = mock_tree
        ssdlc.add_item("REQ", count=1)
        mock_doc.add_item.assert_called_once()

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_add_item_count_three_calls_add_three_times(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_get_tree.return_value = mock_tree
        ssdlc.add_item("REQ", count=3)
        self.assertEqual(mock_doc.add_item.call_count, 3)

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_remove_item_calls_delete(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        ssdlc.remove_item("REQ-001")
        mock_item.delete.assert_called_once()

    @patch("c5dec.core.ssdlc.doorstop.build")
    def test_clear_repository_clears_all_items(self, mock_build):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        item1 = MagicMock()
        item2 = MagicMock()
        mock_doc.items = [item1, item2]
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        ssdlc.clear_repository("REQ")
        item1.clear.assert_called_once()
        item2.clear.assert_called_once()

    @patch("c5dec.core.ssdlc.doorstop.build")
    def test_review_repository_reviews_all_items(self, mock_build):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        item1 = MagicMock()
        item2 = MagicMock()
        mock_doc.items = [item1, item2]
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        ssdlc.review_repository("REQ")
        item1.review.assert_called_once()
        item2.review.assert_called_once()

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_clear_item_calls_clear(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        ssdlc.clear_item("REQ-001")
        mock_item.clear.assert_called_once()

    @patch("c5dec.core.ssdlc.get_artifact_tree")
    def test_review_item_calls_review(self, mock_get_tree):
        mock_tree = MagicMock()
        mock_item = MagicMock()
        mock_tree.find_item.return_value = mock_item
        mock_get_tree.return_value = mock_tree
        ssdlc.review_item("REQ-001")
        mock_item.review.assert_called_once()


class TestCreateNewC5decProject(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    @patch("c5dec.core.ssdlc.shutil.copytree")
    @patch("c5dec.core.ssdlc.shutil.make_archive")
    @patch("c5dec.core.ssdlc.shutil.rmtree")
    @patch("c5dec.core.ssdlc.os.path.exists", return_value=False)
    def test_creates_project_with_lowercase_name(
        self, mock_exists, mock_rmtree, mock_archive, mock_copy
    ):
        ssdlc.create_new_c5dec_project(project="MyProject", user="tester")
        mock_copy.assert_called_once()
        call_args = mock_copy.call_args[0]
        self.assertIn("myproject", call_args[1])

    @patch("c5dec.core.ssdlc.os.path.exists", return_value=True)
    def test_existing_destination_logs_error_and_returns(self, mock_exists):
        result = ssdlc.create_new_c5dec_project(project="existing", user="u")
        self.assertIsNone(result)


class TestStubFunctions(unittest.TestCase):

    def test_generate_rtm_returns_none(self):
        self.assertIsNone(ssdlc.generate_rtm())

    def test_link_artifacts_in_batch_returns_none(self):
        self.assertIsNone(ssdlc.link_artifacts_in_batch())

    def test_add_item_attribute_from_file_returns_none(self):
        self.assertIsNone(ssdlc.add_item_attribute_from_file())

    def test_visualize_req_graph_returns_none(self):
        self.assertIsNone(ssdlc.visualize_req_graph())


if __name__ == "__main__":
    unittest.main()
