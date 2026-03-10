import argparse
import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

import c5dec.frontend.cli.commands as commands

_CWD = "/tmp"
_ERROR = lambda msg: None


class TestCommandGet(unittest.TestCase):

    def test_get_known_command_returns_callable(self):
        fn = commands.get("new")
        self.assertTrue(callable(fn))

    def test_get_new_returns_run_new(self):
        self.assertIs(commands.get("new"), commands.run_new)

    def test_get_view_returns_run_view(self):
        self.assertIs(commands.get("view"), commands.run_view)

    def test_get_validate_returns_run_validate(self):
        self.assertIs(commands.get("validate"), commands.run_validate)

    def test_get_transform_returns_run_transform(self):
        self.assertIs(commands.get("transform"), commands.run_transform)

    def test_get_none_returns_run(self):
        self.assertIs(commands.get(None), commands.run)

    def test_get_unknown_raises_key_error(self):
        with self.assertRaises(KeyError):
            commands.get("nonexistent_command_xyz")


class TestRunNew(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.ssdlc.create_new_c5dec_project")
    def test_run_new_delegates_to_ssdlc(self, mock_create):
        args = argparse.Namespace(project="myproject", user="user")
        commands.run_new(args, _CWD, _ERROR)
        mock_create.assert_called_once_with(project="myproject", user="user")


class TestRunDocengine(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.ssdlc.create_docengine_template", return_value=True)
    def test_returns_true_on_success(self, mock_tpl):
        args = argparse.Namespace(template_type="report", name="my-report", destination=None)
        result = commands.run_docengine(args, _CWD, _ERROR)
        self.assertTrue(result)
        mock_tpl.assert_called_once_with(template_type="report", name="my-report", destination=None)

    @patch("c5dec.frontend.cli.commands.ssdlc.create_docengine_template", return_value=None)
    def test_returns_true_when_core_returns_none(self, mock_tpl):
        args = argparse.Namespace(template_type="presentation", name="slides", destination=None)
        result = commands.run_docengine(args, _CWD, _ERROR)
        self.assertTrue(result)

    @patch("c5dec.frontend.cli.commands.ssdlc.create_docengine_template", return_value=False)
    def test_returns_false_when_core_returns_false(self, mock_tpl):
        args = argparse.Namespace(template_type="report", name="fail", destination=None)
        result = commands.run_docengine(args, _CWD, _ERROR)
        self.assertFalse(result)

    @patch("c5dec.frontend.cli.commands.ssdlc.create_docengine_template", side_effect=Exception("boom"))
    def test_returns_false_on_exception(self, mock_tpl):
        args = argparse.Namespace(template_type="report", name="err", destination=None)
        result = commands.run_docengine(args, _CWD, _ERROR)
        self.assertFalse(result)


class TestRunTimerep(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_sets_filename_and_calls_convert(self, mock_cls):
        mock_assistant = MagicMock()
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(name="export.xls")
        commands.run_timerep(args, _CWD, _ERROR)
        self.assertEqual(mock_assistant.input_file_name, "export.xls")
        mock_assistant.convert_openproject_time_report_to_IAL_format.assert_called_once()

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_exception_is_caught_and_not_raised(self, mock_cls):
        mock_assistant = MagicMock()
        mock_assistant.convert_openproject_time_report_to_IAL_format.side_effect = Exception("fail")
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(name="bad.xls")
        # Must not raise
        commands.run_timerep(args, _CWD, _ERROR)


class TestRunConsolidate(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_no_filter_sets_apply_filters_false(self, mock_cls):
        mock_assistant = MagicMock()
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(
            name="source-TSH", filter=None,
            fromdate=None, to=None, field=None, value=None
        )
        commands.run_consolidate(args, _CWD, _ERROR)
        mock_assistant.set_tsh_folder_name.assert_called_once_with("source-TSH")
        mock_assistant.set_timerep_parameters.assert_called_once_with(
            source_folder="source-TSH", apply_filters=False
        )
        mock_assistant.consolidate_timesheets.assert_called_once()

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_with_filter_passes_date_range(self, mock_cls):
        mock_assistant = MagicMock()
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(
            name="source-TSH", filter="1",
            fromdate="01-01-2024", to="31-12-2024",
            field="Domain", value="RD"
        )
        commands.run_consolidate(args, _CWD, _ERROR)
        call_kwargs = mock_assistant.set_timerep_parameters.call_args
        self.assertTrue(call_kwargs.kwargs.get("apply_filters"))
        mock_assistant.consolidate_timesheets.assert_called_once()

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_ioerror_is_caught(self, mock_cls):
        mock_assistant = MagicMock()
        mock_assistant.consolidate_timesheets.side_effect = IOError
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(
            name="source-TSH", filter=None,
            fromdate=None, to=None, field=None, value=None
        )
        # Must not raise
        commands.run_consolidate(args, _CWD, _ERROR)


class TestRunCostrep(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_sets_filename_and_calls_compute(self, mock_cls):
        mock_assistant = MagicMock()
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(name="tsh.xlsx")
        commands.run_costrep(args, _CWD, _ERROR)
        self.assertEqual(mock_assistant.input_file_name, "tsh.xlsx")
        mock_assistant.compute_cost_report.assert_called_once()

    @patch("c5dec.frontend.cli.commands.pm.TimeReportAssistant")
    def test_exception_is_caught_and_not_raised(self, mock_cls):
        mock_assistant = MagicMock()
        mock_assistant.compute_cost_report.side_effect = Exception("fail")
        mock_cls.return_value = mock_assistant
        args = argparse.Namespace(name="tsh.xlsx")
        commands.run_costrep(args, _CWD, _ERROR)


class TestRunView(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.cct.get_item")
    def test_non_verbose_passes_silence_true(self, mock_get):
        args = argparse.Namespace(id="FDP_ACC.1", version="3R5", verbose=False)
        commands.run_view(args, _CWD, _ERROR)
        mock_get.assert_called_once_with("FDP_ACC.1", "3R5", silence=True)

    @patch("c5dec.frontend.cli.commands.cct.get_item")
    def test_verbose_omits_silence_kwarg(self, mock_get):
        args = argparse.Namespace(id="FDP_ACC.1", version="3R5", verbose=True)
        commands.run_view(args, _CWD, _ERROR)
        mock_get.assert_called_once_with("FDP_ACC.1", "3R5")

    @patch("c5dec.frontend.cli.commands.cct.get_item")
    def test_sets_selected_cc_version(self, mock_get):
        import c5dec.settings as c5settings
        original = c5settings.SELECTED_CC_VERSION
        try:
            args = argparse.Namespace(id="ALC_CMC.1", version="3R4", verbose=False)
            commands.run_view(args, _CWD, _ERROR)
            self.assertEqual(c5settings.SELECTED_CC_VERSION, "3R4")
        finally:
            c5settings.SELECTED_CC_VERSION = original


class TestRunValidate(unittest.TestCase):

    @patch("c5dec.frontend.cli.commands.cct.validate")
    def test_non_verbose_passes_silence_true(self, mock_validate):
        args = argparse.Namespace(id=["FDP_ACC.1"], version="3R5", verbose=False, mode=None)
        commands.run_validate(args, _CWD, _ERROR)
        mock_validate.assert_called_once_with(["FDP_ACC.1"], "3R5", mode=None, silence=True)

    @patch("c5dec.frontend.cli.commands.cct.validate")
    def test_verbose_omits_silence_kwarg(self, mock_validate):
        args = argparse.Namespace(id=["FDP_ACC.1"], version="3R5", verbose=True, mode="dep")
        commands.run_validate(args, _CWD, _ERROR)
        mock_validate.assert_called_once_with(["FDP_ACC.1"], "3R5", mode="dep")


class TestRunTransform(unittest.TestCase):

    def test_prints_doorstop_reference(self):
        args = argparse.Namespace()
        buf = io.StringIO()
        with redirect_stdout(buf):
            commands.run_transform(args, _CWD, _ERROR)
        self.assertIn("doorstop", buf.getvalue())

    def test_prints_quarto_reference(self):
        args = argparse.Namespace()
        buf = io.StringIO()
        with redirect_stdout(buf):
            commands.run_transform(args, _CWD, _ERROR)
        self.assertIn("quarto", buf.getvalue())


class TestRunCra(unittest.TestCase):

    def _args(self, create=False, verify=False, export=None, category="default", prefix=None):
        return argparse.Namespace(
            create=create, verify=verify,
            export=export, category=category, prefix=prefix
        )

    def test_no_action_returns_true(self):
        result = commands.run_cra(self._args(), _CWD, _ERROR)
        self.assertTrue(result)

    @patch("c5dec.core.cra.CRAChecklistBuilder")
    def test_create_calls_builder_and_returns_true(self, mock_cls):
        mock_builder = MagicMock()
        mock_builder.create_cra_checklist.return_value = "/tmp/crac"
        mock_cls.return_value = mock_builder
        result = commands.run_cra(self._args(create=True, category="class_i"), _CWD, _ERROR)
        self.assertTrue(result)
        mock_builder.create_cra_checklist.assert_called_once()

    @patch("c5dec.core.cra.auto_verify_sbom_requirement", return_value=True)
    def test_verify_calls_auto_verify_and_returns_true(self, mock_verify):
        result = commands.run_cra(self._args(verify=True), _CWD, _ERROR)
        self.assertTrue(result)
        mock_verify.assert_called_once()

    @patch("c5dec.core.cra.auto_verify_sbom_requirement", return_value=False)
    @patch("c5dec.core.cra.CRAChecklistBuilder")
    def test_export_calls_export_checklist_and_returns_true(self, mock_cls, mock_verify):
        mock_builder = MagicMock()
        mock_builder.export_cra_checklist.return_value = "/tmp/crac.xlsx"
        mock_cls.return_value = mock_builder
        result = commands.run_cra(self._args(export="output.xlsx"), _CWD, _ERROR)
        self.assertTrue(result)
        mock_builder.export_cra_checklist.assert_called_once()

    @patch("c5dec.core.cra.CRAChecklistBuilder", side_effect=Exception("db error"))
    def test_exception_returns_false(self, mock_cls):
        result = commands.run_cra(self._args(create=True), _CWD, _ERROR)
        self.assertFalse(result)


class TestSystemCliVersion(unittest.TestCase):
    """System test — invokes the CLI entry point as a subprocess."""

    def test_version_flag_exits_zero(self):
        # Integration test
        result = subprocess.run(
            ["poetry", "run", "c5dec", "--version"],
            capture_output=True, text=True,
            cwd="/home/alab/c5dec"
        )
        self.assertEqual(result.returncode, 0)

    def test_help_flag_exits_zero_and_prints_c5dec(self):
        # Integration test
        result = subprocess.run(
            ["poetry", "run", "c5dec", "--help"],
            capture_output=True, text=True,
            cwd="/home/alab/c5dec"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("c5dec", result.stdout)

    def test_transform_subcommand_exits_zero(self):
        # Integration test
        result = subprocess.run(
            ["poetry", "run", "c5dec", "transform"],
            capture_output=True, text=True,
            cwd="/home/alab/c5dec"
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("quarto", result.stdout)


if __name__ == "__main__":
    unittest.main()
