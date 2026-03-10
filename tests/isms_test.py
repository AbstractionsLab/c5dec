import csv
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, mock_open, patch

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

import c5dec.core.isms as isms


_PERSONS_DATA = json.dumps({
    "Alan Turing": "ATU",
    "John von Neumann": "JVN",
})


class TestWordTagProcessorInit(unittest.TestCase):

    def test_initial_state(self):
        processor = isms.WordTagProcessor()
        self.assertFalse(processor.params_are_set)
        self.assertFalse(processor.ignore_missing_tag_mapping)
        self.assertEqual(processor.default_link, "https://google.com")

    def test_regex_compiles(self):
        processor = isms.WordTagProcessor()
        m = processor.tag_regex.search("Some text #S-CTRL-1 more text")
        self.assertIsNotNone(m)

    def test_regex_no_match_on_plain_text(self):
        processor = isms.WordTagProcessor()
        m = processor.tag_regex.search("No hash tag here")
        self.assertIsNone(m)


class TestWordTagProcessorSetParams(unittest.TestCase):

    def setUp(self):
        self.processor = isms.WordTagProcessor()

    @patch("c5dec.core.isms.docx.Document")
    def test_set_params_marks_ready(self, mock_doc):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            f.write("tag,url\n#S-CTRL-1,https://example.com\n")
            csv_path = f.name
        try:
            self.processor.set_params("fake.docx", csv_path, r"(.*?)(#S(?:-\w+)+)(.*?)")
            self.assertTrue(self.processor.params_are_set)
        finally:
            os.unlink(csv_path)

    @patch("c5dec.core.isms.docx.Document")
    def test_set_params_invalid_csv_unsets_ready(self, mock_doc):
        self.processor.set_params("fake.docx", "/nonexistent/path.csv", r"(.*?)(#S(?:-\w+)+)(.*?)")
        self.assertFalse(self.processor.params_are_set)

    @patch("c5dec.core.isms.docx.Document")
    def test_set_params_sets_output_name(self, mock_doc):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
            f.write("tag,url\n")
            csv_path = f.name
        try:
            self.processor.set_params("myreport.docx", csv_path, r"(.*?)(#S(?:-\w+)+)(.*?)")
            self.assertIn("myreport.docx", self.processor.output_name)
        finally:
            os.unlink(csv_path)


class TestWordTagProcessorReadCsv(unittest.TestCase):

    def setUp(self):
        self.processor = isms.WordTagProcessor()

    def test_read_csv_returns_dict(self):
        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False, mode="w", newline=""
        ) as f:
            writer = csv.writer(f)
            writer.writerow(["#S-TAG-1", "https://example.com"])
            writer.writerow(["#S-TAG-2", "https://other.com"])
            csv_path = f.name
        try:
            result = self.processor.read_csv_into_dict(csv_path)
            self.assertIsInstance(result, dict)
            self.assertIn("#S-TAG-1", result)
            self.assertEqual(result["#S-TAG-1"], "https://example.com")
        finally:
            os.unlink(csv_path)

    def test_read_csv_nonexistent_returns_none(self):
        result = self.processor.read_csv_into_dict("/nonexistent/file.csv")
        self.assertIsNone(result)


class TestWordTagProcessorStaticHelpers(unittest.TestCase):

    def test_create_run_element_returns_element(self):
        run = isms.WordTagProcessor.create_run_element()
        self.assertIsNotNone(run)

    def test_create_text_element_sets_text(self):
        elem = isms.WordTagProcessor.create_text_element("hello")
        self.assertEqual(elem.text, "hello")

    def test_convert_tags_raises_when_not_set(self):
        processor = isms.WordTagProcessor()
        with self.assertRaises(IOError):
            processor.convert_tags_to_hyperlinks()


class TestDocListAssistantInit(unittest.TestCase):

    def test_default_state(self):
        assistant = isms.DocListAssistant()
        self.assertEqual(assistant.doclist, [])
        self.assertEqual(assistant.doclist_path, "")
        self.assertEqual(assistant.doc_scan_path, "")
        self.assertEqual(assistant.unlisted_docs, [])
        self.assertEqual(assistant.used_filename_column_name, "UsedFilename")
        self.assertIsInstance(assistant.folders, dict)


class TestDocListAssistantGetUnlisted(unittest.TestCase):

    def setUp(self):
        self.assistant = isms.DocListAssistant()

    # TST-034
    def test_returns_empty_when_column_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            import pandas as pd
            xl_path = os.path.join(tmpdir, "doclist.xlsx")
            df = pd.DataFrame({"SomeName": ["file1.txt"]})
            df.to_excel(xl_path, sheet_name="DocList", index=False)
            scan_dir = os.path.join(tmpdir, "docs")
            os.makedirs(scan_dir)
            self.assistant.doclist_path = xl_path
            self.assistant.doc_scan_path = scan_dir
            result = self.assistant.get_unlisted_docs()
            self.assertEqual(result, [])


class TestDocListAssistantSaveToCsv(unittest.TestCase):

    def setUp(self):
        self.assistant = isms.DocListAssistant()

    def test_save_creates_csv(self):
        self.assistant.activity_report = {
            "/folder": [["report-ATU.docx", "Alan Turing", "01/01/2026", "edited"]]
        }
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = f.name
        try:
            self.assistant.save_to_csv(csv_path)
            self.assertTrue(os.path.getsize(csv_path) > 0)
        finally:
            os.unlink(csv_path)


class TestActivityReportInit(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def test_init_loads_authors(self):
        report = isms.ActivityReport()
        self.assertIsInstance(report.authors, dict)
        self.assertEqual(report.path, "")
        self.assertEqual(report.beginning_date, 0)
        self.assertIsInstance(report.activity_report, dict)

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def test_get_authors_returns_dict(self):
        report = isms.ActivityReport()
        self.assertIn("Alan Turing", report.authors)
        self.assertEqual(report.authors["Alan Turing"], "ATU")


class TestActivityReportGetDaysInMonth(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def setUp(self):
        self.report = isms.ActivityReport()

    def test_january_has_31_days(self):
        self.assertEqual(self.report.get_days_in_month(1, 2024), 31)

    def test_april_has_30_days(self):
        self.assertEqual(self.report.get_days_in_month(4, 2024), 30)

    def test_february_non_leap_has_28_days(self):
        self.assertEqual(self.report.get_days_in_month(2, 2023), 28)

    def test_february_leap_year_has_29_days(self):
        self.assertEqual(self.report.get_days_in_month(2, 2024), 29)

    def test_february_century_non_leap_has_28_days(self):
        self.assertEqual(self.report.get_days_in_month(2, 1900), 28)

    def test_february_400_year_cycle_has_29_days(self):
        self.assertEqual(self.report.get_days_in_month(2, 2000), 29)


class TestActivityReportSetDate(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def setUp(self):
        self.report = isms.ActivityReport()

    def test_set_date_sets_beginning_date(self):
        self.report.set_date(0, 0, 1)
        self.assertGreater(self.report.beginning_date, 0)

    def test_set_date_past_within_range(self):
        from time import time as _time
        self.report.set_date(0, 1, 0)
        self.assertLess(self.report.beginning_date, _time())


class TestActivityReportGetUser(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def setUp(self):
        self.report = isms.ActivityReport()

    def test_known_acronym_returns_name(self):
        result = self.report.get_user("doc-description-ATU.docx")
        self.assertEqual(result, "Alan Turing")

    def test_unknown_acronym_returns_empty_string(self):
        result = self.report.get_user("doc-UNKNOWN.docx")
        self.assertEqual(result, "")

    def test_acronym_case_insensitive(self):
        result = self.report.get_user("doc-JVN.docx")
        self.assertEqual(result, "John von Neumann")


class TestActivityReportScandir(unittest.TestCase):

    @patch("builtins.open", mock_open(read_data=_PERSONS_DATA))
    def setUp(self):
        self.report = isms.ActivityReport()

    def test_scandir_populates_folders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "file-ATU.txt"), "w").close()
            self.report.path = tmpdir + os.sep
            self.report.beginning_date = 0
            self.report.scandir()
            self.assertIsInstance(self.report.folders, dict)
            all_files = [f for files in self.report.folders.values() for f in files]
            self.assertIn("file-ATU.txt", all_files)

    def test_empty_dir_returns_empty_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            self.report.path = tmpdir + os.sep
            self.report.beginning_date = 0
            self.report.scandir()
            all_files = [f for files in self.report.folders.values() for f in files]
            self.assertEqual(all_files, [])


if __name__ == "__main__":
    unittest.main()
