import os
import sys
import time
import tempfile
import shutil
import zipfile
import unittest
from unittest.mock import MagicMock, patch, call

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import c5dec.core.transformer as transformer
import c5dec.settings as c5settings


class TestImportSsdlcDocument(unittest.TestCase):

    # TST-012
    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.importer.import_file")
    def test_imports_file_into_document(self, mock_import, mock_build):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        transformer.import_ssdlc_document("some/path.csv", "REQ", ".csv")
        mock_tree.find_document.assert_called_once_with("REQ")
        mock_import.assert_called_once_with("some/path.csv", mock_doc, ".csv")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.importer.import_file")
    def test_builds_tree_before_import(self, mock_import, mock_build):
        mock_build.return_value = MagicMock()
        transformer.import_ssdlc_document("path.yml", "SRS", ".yml")
        mock_build.assert_called_once()


class TestExportSsdlcDocument(unittest.TestCase):

    # TST-012
    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.exporter.export")
    def test_export_single_document(self, mock_export, mock_build):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        result = transformer.export_ssdlc_document("REQ", path="/tmp/output.yml", format=".yml")
        mock_tree.find_document.assert_called_once_with("REQ")
        mock_export.assert_called_once_with(mock_doc, "/tmp/output.yml", ".yml")
        self.assertEqual(result, "/tmp/output.yml")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.exporter.export")
    def test_export_all_uses_tree(self, mock_export, mock_build):
        mock_tree = MagicMock()
        mock_build.return_value = mock_tree
        transformer.export_ssdlc_document("all", path="./export")
        mock_export.assert_called_once_with(mock_tree, "./export", ".yml")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.exporter.export")
    def test_export_returns_path(self, mock_export, mock_build):
        mock_build.return_value = MagicMock()
        result = transformer.export_ssdlc_document("REQ", path="/my/path.csv", format=".csv")
        self.assertEqual(result, "/my/path.csv")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.exporter.export")
    @patch("c5dec.core.transformer.common.create_dirname")
    def test_export_all_without_path_creates_default_dir(
        self, mock_mkdir, mock_export, mock_build
    ):
        mock_build.return_value = MagicMock()
        transformer.export_ssdlc_document("all")
        mock_mkdir.assert_called_once()


class TestPublishSsdlcDocument(unittest.TestCase):

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_single_document(self, mock_publish, mock_build):
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        result = transformer.publish_ssdlc_document("REQ", path="/tmp/out.html", format="html")
        mock_tree.find_document.assert_called_once_with("REQ")
        mock_publish.assert_called_once_with(mock_doc, "/tmp/out.html", "html")
        self.assertEqual(result, "/tmp/out.html")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_all_publishes_tree(self, mock_publish, mock_build):
        mock_tree = MagicMock()
        mock_build.return_value = mock_tree
        transformer.publish_ssdlc_document("all", path="./export")
        mock_publish.assert_called_once_with(mock_tree, "./export", "html")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_returns_path(self, mock_publish, mock_build):
        mock_build.return_value = MagicMock()
        result = transformer.publish_ssdlc_document("REQ", path="/out/path.html")
        self.assertEqual(result, "/out/path.html")


class TestPublish(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._original_project_root = c5settings.PROJECT_ROOT

    def tearDown(self):
        c5settings.PROJECT_ROOT = self._original_project_root
        shutil.rmtree(self.tmp, ignore_errors=True)

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_archives_specs_folder_when_exists(self, mock_publish, mock_build):
        c5settings.PROJECT_ROOT = self.tmp
        specs_folder = os.path.join(self.tmp, "docs", "specs")
        os.makedirs(specs_folder)
        open(os.path.join(specs_folder, "item.yml"), "w").close()
        mock_build.return_value = MagicMock()
        transformer.publish(prefix="all", path=os.path.join(self.tmp, "out"))
        archive_path = os.path.join(self.tmp, "docs", "c5dec-specs.zip")
        self.assertTrue(os.path.exists(archive_path))

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_deletes_specs_folder_after_archive(self, mock_publish, mock_build):
        c5settings.PROJECT_ROOT = self.tmp
        specs_folder = os.path.join(self.tmp, "docs", "specs")
        os.makedirs(specs_folder)
        open(os.path.join(specs_folder, "item.yml"), "w").close()
        mock_build.return_value = MagicMock()
        transformer.publish(prefix="all", path=os.path.join(self.tmp, "out"))
        self.assertFalse(os.path.exists(specs_folder))

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_no_specs_folder_proceeds_gracefully(self, mock_publish, mock_build):
        c5settings.PROJECT_ROOT = self.tmp
        mock_build.return_value = MagicMock()
        transformer.publish(prefix="all", path=os.path.join(self.tmp, "pub"))
        mock_build.assert_called_once()

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_single_prefix_finds_document(self, mock_publish, mock_build):
        c5settings.PROJECT_ROOT = self.tmp
        mock_tree = MagicMock()
        mock_doc = MagicMock()
        mock_tree.find_document.return_value = mock_doc
        mock_build.return_value = mock_tree
        transformer.publish(prefix="REQ", path="/tmp/req.html", format=".html")
        mock_tree.find_document.assert_called_once_with("REQ")
        mock_publish.assert_called_once_with(mock_doc, "/tmp/req.html", ".html")

    @patch("c5dec.core.transformer.doorstop.build")
    @patch("c5dec.core.transformer.doorstop.publisher.publish")
    def test_publish_defaults_format_to_md(self, mock_publish, mock_build):
        c5settings.PROJECT_ROOT = self.tmp
        mock_tree = MagicMock()
        mock_tree.find_document.return_value = MagicMock()
        mock_build.return_value = mock_tree
        transformer.publish(prefix="REQ", path="/tmp/out")
        call_args = mock_publish.call_args
        self.assertIn(".md", call_args[0])


if __name__ == "__main__":
    unittest.main()
