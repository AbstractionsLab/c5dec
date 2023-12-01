from c5dec.frontend.tui.foundation.menu import BaseView
from c5dec.core.pm import TimeReportAssistant
from c5dec.frontend.tui.foundation.builder import Builder
import os
from os.path import exists, isfile
from i18n import t as translate
from docx.opc.exceptions import PackageNotFoundError

class TimeReportModel(TimeReportAssistant):
    def __init__(self) -> None:
        super(TimeReportModel, self).__init__()

class OpenProjectTimeReportAssistantView(BaseView):
    """The view of the time report assistant.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view.

        The time report assistant performs post-processing on OpenProject time reports.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("OpenProject time report assistant")
        builder.addLayout([100])

        # Input
        self.input_file_path = builder.addPath("Path to OpenProject time report file:")
        
        builder.addButton("Convert to IAL timesheet format", self.run_timerep_conversion, gap=True, 
            gap_height=2)
        
        builder.addButton("Clear fields", self.clear_fields)
        
        # Output
        builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(OpenProjectTimeReportAssistantView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: TimeReportAssistant = TimeReportAssistant() 


    def run_timerep_conversion(self):
        input_file_path = self.input_file_path.value
        try:
            if not (input_file_path is None):
                self.data_model.input_file_path = input_file_path
                _ = self.data_model.convert_openproject_time_report_to_IAL_format()
        except IOError:
            self.statusbar.value = translate("Missing or bad arguments.")
            return None
        except PackageNotFoundError:
            self.statusbar.value = translate("No xlsx file found at the provided path.")
            return None
        except Exception as e:
            self.statusbar.value = translate("Something unexpected went wrong: {}".format(e))
            return None
        self.statusbar.value = translate(
            "Done, the post-processed time report can be found in the C5-DEC folder.")

    def clear_fields(self):
        self.input_file_path.value = ""

class TimeReportAssistantView(BaseView):
    """The view of the time report assistant.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view.

        The time report assistant performs post-processing on OpenProject time reports.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("Time report assistant")
        builder.addLayout([100])

        # Input
        self.tsh_folder_path = builder.addPath("Path to folder containing time report files:")

        self.use_filters = builder.addTickBox("Apply filters?", "filteruse")

        self.from_date_picker = builder.add_date_picker("fromdatepicker", "From date:")
        self.to_date_picker = builder.add_date_picker("todatepicker", "To date:")

        # self.filter_field_name = builder.addText("Field to filter:", "fieldfiltername", gap=False)
        self.filter_field_list = builder.addDropdownList(
            "Field to filter", "targetfield", on_change=None, 
            gap=True, gap_height=2)
        self.populate_filter_field_listbox(builder=builder)

        self.filter_field_value = builder.addText("Field value to filter:", "fieldvaluefiltername", gap=False)

        builder.addButton("Consolidate time reports", self.run_tsh_consolidation, gap=True, gap_height=2)
            
        # self.input_file_path = builder.addPath("Path to consolidated timesheet file:")
        # self.to_be_merged_file = builder.addPath("Path to TSH to merge with consoliated TSH:")

        # builder.addButton("Merge file with consolidated TSH", self.merge_tsh_with_consolidated_tsh, gap=True, 
        #     gap_height=2)
        
        builder.addButton("Clear fields", self.clear_fields)
        
        # Output
        builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(TimeReportAssistantView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: TimeReportAssistant = TimeReportAssistant() 


    # def merge_tsh_with_consolidated_tsh(self):
    #     # self.statusbar.value = str(self.from_date_picker.value.year)
    #     self.statusbar.value = "Not implemented yet..."
    #     return
    #     input_file_path = self.input_file_path.value
    #     try:
    #         if not (input_file_path is None):
    #             # self.controller.set_model_params(input_file_path=input_file_path)
    #             self.data_model.input_file_path = input_file_path
    #             # self.data_model.set_tsh_folder_path(tsh_folder_path)
    #             # self.controller.convert_time_report_to_IAL_format()
    #             # _ = self.data_model.convert_openproject_time_report_to_IAL_format()
    #     except IOError:
    #         self.statusbar.value = translate("Missing or bad arguments.")
    #         # self.statusbar.value = os.getcwd()+"--"+input_file_path
    #         return None
    #     except PackageNotFoundError:
    #         self.statusbar.value = translate("No xlsx file found at the provided path.")
    #         return None
    #     self.statusbar.value = translate(
    #         "Done: the post-processed time report can be found in the C5-DEC folder.")
        
    def populate_filter_field_listbox(self, builder):
        timerep_fields = self.data_model.get_timerep_fields()
        self.filter_field_list.options = builder.zipOfList(timerep_fields)

    def run_tsh_consolidation(self):
        folder_path = self.tsh_folder_path.value
        try:
            if not (folder_path is None):
                filter_field = self.filter_field_list.options[self.filter_field_list.value][0]
                self.data_model.set_timerep_parameters(source_folder=self.tsh_folder_path.value,
                                                       apply_filters=self.use_filters.value,
                                               from_date=self.from_date_picker.value,
                                               to_date=self.to_date_picker.value,
                                               filter_field=filter_field,
                                               filter_field_value=self.filter_field_value.value)
                _ = self.data_model.consolidate_timesheets()
        except IOError:
            self.statusbar.value = translate("Missing or bad arguments.")
            return None
        except PackageNotFoundError:
            self.statusbar.value = translate("No xlsx file found at the provided path.")
            return None
        except Exception as e:
            self.statusbar.value = translate("Something unexpected went wrong: {}".format(e))
            return None
        self.statusbar.value = translate(
            "Done, time reports have been successfully consolidated.")


    def clear_fields(self):
        # self.input_file_path.value = ""
        self.tsh_folder_path.value = ""