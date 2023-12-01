from c5dec.frontend.tui.foundation.menu import Menu, BaseView
from c5dec.frontend.tui.foundation.builder import Builder
import c5dec.settings as c5settings
import c5dec.common as common
from c5dec.frontend.tui.application import Application
import c5dec.core.ssdlc as ssdlc
import c5dec.core.transformer as transformer
import doorstop
from i18n import t as translate
from docx.opc.exceptions import PackageNotFoundError

class TransformerModel:
    def __init__(self) -> None:
        pass

class ExportModel(TransformerModel):
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(ExportModel, self).__init__()

class ExportView(BaseView):
    """The view of the data export submodule.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view for the data export submodule.
        
        The view of the data export submodule provides an easy-to-use
        UI for triggering various data export functions.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("SSDLC data export")
        builder.addLayout([100], True)

        # Export which document/repository
        self.target_repository = builder.addDropdownList(
            "Export one document or all", "target_repo", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=2)
        
        self.populate_document_listbox(builder=builder)

        self.export_format = builder.addDropdownList(
            "Export format", "export_format", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=1)
        
        self.export_format.options = builder.zipOfList([".yml", ".csv", ".tsv", ".xlsx"])

        # builder.addLayout([100])
        builder.addButton(
            "Export", self.handle_export_button_press_event, gap=True, gap_height=1)
        
        # builder.addButton("Clear fields", self.clear_fields)
        
        self.statusbar = builder.addStatusBar()
        super(ExportView, self).__init__(screen, root_menu, builder)
        self.builder = builder

    def populate_document_listbox(self, builder):
        documents = ssdlc.get_documents()
        lb_name_list = []
        for d in documents:
            lb_name_list.append(d.prefix)
        lb_name_list.append("all")
        self.target_repository.options = builder.zipOfList(lb_name_list)

    def handle_target_repo_change_event(self):
        pass

    def handle_export_button_press_event(self):
        label = self.target_repository.options[self.target_repository.value][0]
        export_format = self.export_format.options[self.export_format.value][0]
        with common.Capture(catch=True) as success:
            path = transformer.export_ssdlc_document(label=label, format=export_format)
            self.statusbar.value = "Export finished: {}".format(path)
        if not success:
            self.statusbar.value = "Something went wrong..."

    # def clear_fields(self):
    #     pass

class ImportModel(TransformerModel):
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(ImportModel, self).__init__()

class ImportView(BaseView):
    """The view of the data export submodule.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view for the data import submodule.
        
        The view of the data import submodule provides an easy-to-use
        UI for triggering various SSDLC data import functions.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("SSDLC data import")
        builder.addLayout([100], True)

        # Import which document/repository
        self.target_repository = builder.addDropdownList(
            "Import document", "target_repo", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=2)
        
        self.populate_document_listbox(builder=builder)

        self.import_format = builder.addDropdownList(
            "Import format", "export_format", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=1)
        
        self.import_format.options = builder.zipOfList([".yml", ".csv", ".tsv", ".xlsx"])

        self.document_path = builder.addPath("Path to previously exported document:")
        self.document_path.value = "{}/...".format(c5settings.PROJECT_ROOT)

        # builder.addLayout([100])
        builder.addButton(
            "Import", self.handle_import_button_press_event, gap=True, gap_height=1)
        
        # builder.addButton("Clear fields", self.clear_fields)
        
        self.statusbar = builder.addStatusBar()
        super(ImportView, self).__init__(screen, root_menu, builder)
        self.builder = builder

    def populate_document_listbox(self, builder):
        documents = ssdlc.get_documents()
        lb_name_list = []
        for d in documents:
            lb_name_list.append(d.prefix)
        self.target_repository.options = builder.zipOfList(lb_name_list)

    def handle_target_repo_change_event(self):
        pass

    def handle_import_button_press_event(self):
        label = self.target_repository.options[self.target_repository.value][0]
        import_format = self.import_format.options[self.import_format.value][0]
        with common.Capture(catch=True) as success:
            transformer.import_ssdlc_document(path=self.document_path.value, prefix=label, format=import_format)
            self.statusbar.value = "Import finished."
        if not success:
            self.statusbar.value = "Something went wrong..."

    # def clear_fields(self):
    #     pass

class PublisherModel(TransformerModel):
    def __init__(self):
        """Set up the key attributes needed for the publisher model.
        """
        super(PublisherModel, self).__init__()

class PublisherView(BaseView):
    """The view of the publisher submodule.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view for the data import submodule.
        
        The view of the data import submodule provides an easy-to-use
        UI for triggering various SSDLC data import functions.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("SSDLC publishing")
        builder.addLayout([100], True)

        # Import which document/repository
        self.target_repository = builder.addDropdownList(
            "Document to publish", "target_repo", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=2)
        
        self.populate_document_listbox(builder=builder)

        self.publish_format = builder.addDropdownList(
            "Publishing format", "export_format", on_change=self.handle_target_repo_change_event, 
            gap=True, gap_height=1)
        
        self.publish_format.options = builder.zipOfList([".txt", ".md", ".html", ".tex"])

        self.document_path = builder.addPath("Path to file or directory:")
        # self.document_path.value = "{}/...".format(c5settings.PROJECT_ROOT)

        # builder.addLayout([100])
        builder.addButton(
            "Publish", self.handle_publish_button_press_event, gap=True, gap_height=1)
        
        # builder.addButton("Clear fields", self.clear_fields)
        
        self.statusbar = builder.addStatusBar()
        super(PublisherView, self).__init__(screen, root_menu, builder)
        self.builder = builder

    def populate_document_listbox(self, builder):
        documents = ssdlc.get_documents()
        lb_name_list = []
        for d in documents:
            lb_name_list.append(d.prefix)
        lb_name_list.append("all")
        self.target_repository.options = builder.zipOfList(lb_name_list)

    def handle_target_repo_change_event(self):
        pass

    def handle_publish_button_press_event(self):
        label = self.target_repository.options[self.target_repository.value][0]
        publish_format = self.publish_format.options[self.publish_format.value][0]
        publish_path = None
        if self.document_path.value != "":
            publish_path = self.document_path.value
        with common.Capture(catch=True) as success:
            transformer.publish_ssdlc_document(label, path=publish_path, format=publish_format)
            self.statusbar.value = "Publish finished."
        if not success:
            self.statusbar.value = "Something went wrong..."

class ConverterModel(TransformerModel):
    def __init__(self) -> None:
        super().__init__()

class ConverterView(BaseView):
    """The view of the converter submodule.
    
    This is the view part of the MVC structure.
    """
    def __init__(self, screen, root_menu, model):
        """Set up the view for the converter submodule.
        
        The view of the converter submodule provides an easy-to-use
        UI for triggering various data conversion functions.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self.data_model = model
        builder = Builder("Data converter")
        builder.addLayout([100], True)

        # Input
        self.input_file_path = builder.addPath("Path to file you wish to convert:")

        # Convert from what
        self.source_type = builder.addDropdownList(
            "Source type", "source_type", on_change=self.generate_source_type_change_event, 
            gap=True, gap_height=2)
        self.source_type.options = builder.zipOfList(["Markdown", "YAML", "LaTeX", "docx"])

         # Convert to what
        self.target_type = builder.addDropdownList(
            "Target type", "target_type", on_change=self.generate_target_type_change_event, 
            gap=True, gap_height=2)
        self.target_type.options = builder.zipOfList(["Markdown", "YAML", "LaTeX", "docx"])

        # builder.addLayout([100])
        builder.addButton(
            "Convert", self.generate_converter_press_event, gap=True, gap_height=1)
        
        builder.addButton("Clear fields", self.clear_fields)
        
        super(ConverterView, self).__init__(screen, root_menu, builder)
        self.builder = builder

    def generate_source_type_change_event(self):
        pass

    def generate_target_type_change_event(self):
        pass

    def generate_converter_press_event(self):
        """Trigger controller function for handling an import
        button press event.
        """
        pass

    def clear_fields(self):
        self.input_file_path.value = ""