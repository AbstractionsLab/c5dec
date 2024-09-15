import unittest
import sys
import os
# sys.path.append("../c5dec")
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(parent_dir)
import c5dec.core.pm as pm

class TimesheetConsolidationTest(unittest.TestCase):
    def setUp(self):
        os.chdir('./c5dec') 
    
    def test_timesheet_consolidation_function(self):
        timerep_assistant = pm.TimeReportAssistant()
        folder_name = "source-TSH"
        timerep_assistant.set_tsh_folder_name(folder_name)
        date_format = '%d-%m-%Y'
        timerep_assistant.set_timerep_parameters(source_folder=folder_name,apply_filters=False)
        timerep_assistant.consolidate_timesheets()
    
    def tearDown(self):
        os.chdir('..')

class TimeReportProcessingTest(unittest.TestCase):
    def setUp(self):
        os.chdir('./c5dec')

    def test_time_report_processing_function(self):
        timerep_assistant = pm.TimeReportAssistant()
        input_file_name = "export-29-06-2023-T-11-55-49.xls"
        timerep_assistant.input_file_name = input_file_name
        timerep_assistant.convert_openproject_time_report_to_IAL_format()

    def tearDown(self):
        os.chdir('..')

class CostReportProcessingTest(unittest.TestCase):
    def setUp(self):
        os.chdir('./c5dec')

    def test_time_report_processing_function(self):
        timerep_assistant = pm.TimeReportAssistant()
        timerep_assistant.input_file_name = "tsh.xlsx"
        timerep_assistant.compute_cost_report()

    def tearDown(self):
        os.chdir('..')


if __name__ == "__main__":
    unittest.main()
