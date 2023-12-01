from c5dec.frontend.tui.foundation.menu import BaseView
# from c5dec.frontend.tui.models.docmanagement.msword_tag_processor import WordTagProcessor
from c5dec.core.isms import WordTagProcessor
from c5dec.core.isms import DocListAssistant
from c5dec.core.isms import ActivityReport
# from c5dec.frontend.tui.controllers.docmanagement.msoffice_controller import MSOfficeController
from c5dec.frontend.tui.foundation.builder import Builder
from docx.opc.exceptions import PackageNotFoundError

from os.path import exists, isfile
from i18n import t as translate

class MSWordTagProcessingModel:
    def __init__(self) -> None:
        pass

class MSWordTagProcessingView(BaseView):
    """The view of MS Word tag processing.
    
    This is the view part of the MVC structure of the MS Word tag processing
    function.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view for the Word tag processor.

        The Word tag processor has an input field for the docx
        path and another one for the CSV file.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("MS Word tag processor")
        builder.addLayout([100])

        # Input
        self.doc_path = builder.addPath('MS Word (.docx) file path')
        self.csv_path = builder.addPath('CSV file path')
        self.keep_style_flag = False
        self.ignore_missing_tag_mapping = False

        self.keep_style_tb = builder.addTickBox("Keep style?", "keep_style", self.toggle_style_status)
        self.ignore_missing_tag_tb = builder.addTickBox("Ignore missing tag to link mapping?", "ignore_tag", self.toggle_missing_tag_behavior)

        builder.addButton("Process", self.process_word_tags, gap=True, 
            gap_height=5)

        # Output
        builder.addLayout([100], True)
        self.statusbar = builder.addStatusBar()
        super(MSWordTagProcessingView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: WordTagProcessor = WordTagProcessor() 

    def toggle_style_status(self):
        self.keep_style_flag = self.keep_style_tb.value
    
    def toggle_missing_tag_behavior(self):
        self.ignore_missing_tag_mapping = self.ignore_missing_tag_tb.value

    def process_word_tags(self):
        """Process word tags and create new document.
        """
        doc_path = self.doc_path.value
        csv_path = self.csv_path.value
        regex_text = "(.*?)(#S(?:-\w+)+)(.*?)"
        try:
            if not (doc_path is None or csv_path is None):
                self.data_model.set_params(doc_path, csv_path, regex_text, ignore_missing_tag=self.ignore_missing_tag_mapping)
                self.data_model.convert_tags_to_hyperlinks(keep_style=self.keep_style_flag)
        except IOError:
            self.statusbar.value = translate("Missing or bad arguments.")
            return None
        except PackageNotFoundError:
            self.statusbar.value = translate("No docx file found at the provided path.")
            return None
        self.statusbar.value = translate(
            "The processed Word document can be found in the same folder.")

class DocListAssistantModel:
    def __init__(self) -> None:
        pass

class DocListAssistantView(BaseView):
    """The view of the document list assistant.
    
    This is the view part of the MVC structure of the document list
    validator.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view for the doc list validator.

        The doc list validator ...

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("Document list assistant")
        builder.addLayout([100])

        # Input
        self.scan_path = builder.addPath("Path to folder:")
        self.doclist_path = builder.addPath("Path to the document list (DOL):")
        self.filename_col_name = builder.addText(
            "Table column name for used filename (optional)", "UsedFilename", gap=True, gap_height=2)
        
        builder.addButton("Show docs not listed in DOL", self.show_unlisted_docs, gap=True, 
            gap_height=2)  
        
        builder.addButton("Clear fields", self.clear_fields)
        
        # Output
        builder.addLayout([100], True)
        self.listbox_files = builder.addListBox(
            "files", "max", [], parser=True, position=0)
        self.statusbar = builder.addStatusBar()
        super(DocListAssistantView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: DocListAssistant = DocListAssistant() 


    def show_unlisted_docs(self):
        self.listbox_files.options = self.builder.zipOfList(list())

        doclist_path = self.doclist_path.value
        doc_scan_path = self.scan_path.value
        col_name = self.filename_col_name.value
        try:
            if not (doclist_path is None or doc_scan_path is None):
                self.data_model.doclist_path = doclist_path
                self.data_model.doc_scan_path = doc_scan_path
                if not col_name == "":
                    self.data_model.used_filename_column_name = col_name

                options = self.builder.zipOfList(self.data_model.get_unlisted_docs())
                self.listbox_files.options = options
        except IOError:
            self.statusbar.value = translate("Missing or bad arguments.")
            return None
        except PackageNotFoundError:
            self.statusbar.value = translate("No xlsx file found at the provided path.")
            return None
        self.statusbar.value = translate(
            "The unlisted documents are shown above.")

    
    def clear_fields(self):     
        self.scan_path.value = ""
        self.doclist_path.value = ""

class ActivityReportModel(ActivityReport):
    def __init__(self) -> None:
        super(ActivityReportModel, self).__init__()

class ActivityReportView(BaseView):
    """The view of the activity report.
    
    This is the view part of the MVC structure of the activity report
    function.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view for the activity report generator.

        The activity report generator has an input field for the folder
        path, input fields for months, days and hours to set how long
        to look back, a dropdownlist to specify the author, a checkbox 
        to say if you want to save the output to a csv file and a 
        corresponding input field to give the output file.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("Activity Report")
        builder.addLayout([100])

        # Input
        self.path = builder.addPath()
        self.months = builder.addText("months", "months")
        self.days = builder.addText("days", "days")
        self.hours = builder.addText("hours", "hours", gap=True)
        self.author = builder.addDropdownList("Author", "author", 
            options=self.get_authors(), gap=True)
        self.csv = builder.addTickBox("Save as csv?", "csv", self.toggle_csv)
        self.saveto = builder.addText("Save to", "save_to", gap=True)
        builder.addButton("List", self.get_activity_report, gap=True, 
            gap_height=2)

        # Output
        builder.addLayout([100], True)
        self.activities_table = builder.addTable(
            "max", ["Folder", "File", "User", "Date", "Event"], [], 
            columns=[25, 33, 17, 15, 10])
        builder.addLayout([100])
        self.statusbar = builder.addStatusBar()
        super(ActivityReportView, self).__init__(screen, root_menu, builder)
        self.toggle_csv()

    def get_authors(self):
        """Get the authors from the model.
        
        :return: all authors by their full names
        :rtype: list
        """
        self.authors = [translate("all")]
        self.authors.extend(list(self.data_model.authors.keys()))
        return self.authors

    def toggle_csv(self):
        """Enable/ Disable the input field of the output file according
        to the corresponding tickbox."""
        if self.csv.value:
            self.builder.enable(self.saveto)
        else:
            self.builder.disable(self.saveto)

    def if_empty_return_0(self, widget):
        """Evaluate the input of a widget and set it to 0 if it is 
        empty.

        :param widget: the widget whose value should be evaluated
        :type widget: class `Widget`

        :return: 0 or the the value of the widget
        :rtype: int
        """
        if widget.value.strip() == "":
            widget.value = "0"
            return 0
        else:
            value = int(widget.value.strip())
            return value

    def get_activity_report(self):
        """Get and display the activity report and optionally, save to 
        a csv file.
        """
        path = self.path.value
        try:
            months = self.if_empty_return_0(self.months)
            days = self.if_empty_return_0(self.days)
            hours = self.if_empty_return_0(self.hours)
        except:
            self.activities_table.options = self.builder.zipOfList([])
            self.statusbar.value = translate("The duration is invalid")
            return None
        if exists(path) and not isfile(path):
            self.statusbar.value = ""
            self.data_model.path = path.strip(" /")
            self.data_model.set_date(months, days, hours)
            if self.author.value != 0:
                author = self.authors[self.author.value]
            else:
                author = 0
            self.data_model.author = author
            activities = self.data_model.get_activity_report()
            list_activities = []

            # Prepare the activity report to be able to be displayed
            for folder, files in activities.items():
                entry = [folder]
                for file_data in files:
                    entry.extend(file_data)
                    list_activities.append(entry)
                    entry = [""]
            # Save to csv file
            if self.csv.value:
                csv_file = self.saveto.value
                if exists(csv_file) and isfile(csv_file):
                    self.data_model.save_to_csv(csv_file)
                    self.statusbar.value = translate(
                        "file successfully saved")
                else:
                    self.statusbar.value = translate(
                        "The path to the CSV file is invalid")

            options = self.builder.zipOfList(list_activities)
        else:
            options = self.builder.zipOfList([])
            self.statusbar.value = translate(
                "The path to the folder is invalid")
        self.activities_table.options = options