from c5dec.frontend.tui.foundation.menu import Menu, BaseView, PopUpMenu
from c5dec.frontend.tui.foundation.builder import Builder
from c5dec.frontend.tui.application import Application
from asciimatics.widgets import PopUpDialog
from asciimatics.exceptions import NextScene
from datetime import datetime
import c5dec.settings as c5settings
import c5dec.common as common
import c5dec.core.cct as cct
import doorstop
import os
import logging

MUTABLE_ATTRIBUTES = ["options", "value", "disabled"]

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

logHandler = logging.FileHandler(c5settings.CCTAPP_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)


def auto_cache(func):
    def wrapper(instance, *args, **kwargs):
        widgets = func(instance, *args, **kwargs)

        if not widgets:
            return 

        elif not isinstance(widgets, list):
            widgets = [widgets]

        for widget in widgets:
            name = widget.name
            instance.CACHE[name] = widget

        return widget
    return wrapper

def auto_reload(func):
    def wrapper(instance, *args, **kwargs):

        result = func(instance, *args, **kwargs)

        cache = instance.CACHE
        if not cache:
            return
        
        for name in list(cache.keys()):
            widget = instance.find_widget(name)
            for attrib in MUTABLE_ATTRIBUTES:
                try:
                    attrib_to_set = getattr(cache[name], attrib)
                    setattr(widget, attrib, attrib_to_set)
                except AttributeError:
                    pass
        return result
    return wrapper


class ArtifactModel:
    """Parent class for all artifact related models.
    """
    _index = {}
    def __init__(self):
        """Set up the key attributes for CC toolbox.
        
        """
        self.project_root = c5settings.PROJECT_ROOT
        self.cc_version = c5settings.SELECTED_CC_VERSION
        if not ArtifactModel._index:
            cct.load_cc_xml(version=self.cc_version)
            ArtifactModel._index = cct.Index

    def find(self, value):
        return self._index.get(value)
    
    def yield_obj(self, obj_type):
        return self._index.yield_obj(obj_type)


class CCBrowserModel(ArtifactModel):
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(CCBrowserModel, self).__init__()

        self.selection = []

class CCBrowserView(BaseView):
    
    CACHE = {}
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation and 
        abstractions over doorstop.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self._screen = screen
        self.data_model = model
        
        app: Application = root_menu.get_ref_to_app()

        max_height = screen.height
        frame_height = max_height - 12
        max_width = screen.width

        builder = Builder("Common Criteria Browser")
        builder.addLayout([13, 7, 10, 10, 10, 50], True)

        builder.add_label("Security Domains", position=0, disabled=True)
        builder.addDivider(draw_line=True, position=0)
        self.domain_list = builder.addListBox("Domain", height=(frame_height-3)//2, 
                                            position=0, on_select=self.load_classes)
        self.domain_list.options = [("Functional Components", 0),
                                    ("Assurance Components", 1)]
        
        builder.addDivider(draw_line=True, position=0)
        builder.add_label("Search Bar", position=0, disabled=True)
        self.search = builder.add_textbox("", "searchbox", height=1, position=0, 
                                          on_change=self.update_suggestion_list)
        self.search_button = builder.addButton("Search", position=0, on_click=self.search_item)
        self.suggestion_list = builder.addListBox("SuggestionBox", height=(frame_height-5)//2, position=0,
                                                    on_select=self.set_search_value)
        
        builder.add_label("Classes", position=1, disabled=True)
        builder.addDivider(draw_line=True, position=1)
        self.class_list = builder.addListBox("Class", height=frame_height-2, 
                                            position=1, on_select=lambda: self.display_selection_data("Class"))

        builder.add_label("Families", position=2, disabled=True)
        builder.addDivider(draw_line=True, position=2)
        self.family_list = builder.addListBox("Family", height=frame_height-2, 
                                            position=2, on_select=lambda: self.display_selection_data("Family"))
        
        builder.add_label("Components", position=3, disabled=True)
        builder.addDivider(draw_line=True, position=3)
        self.component_list = builder.addListBox("Component", height=frame_height-2, 
                                            position=3, on_select=lambda: self.display_selection_data("Component"))
        
        builder.add_label("Elements", position=4, disabled=True)
        builder.addDivider(draw_line=True, position=4)
        self.element_list = builder.addListBox("Element", height=frame_height-2, 
                                            position=4, on_select=lambda: self.display_selection_data("Element"))

        builder.add_label("Item Preview", position=5, disabled=True)
        builder.addDivider(True, position=5)
        self.preview = builder.add_textbox("", "previewbox", height="max", position=5, readonly=True)

        builder.addLayout([50,50])
        builder.addDivider(True)
        self.statusbar = builder.addStatusBar()
        builder.addDivider(True, position=1)
        self.export = builder.addButton("Open Export Menu", on_click=self.open_popup, position=1)

        super(CCBrowserView, self).__init__(screen, root_menu, builder)
        self._reload()
        self.builder = builder
        self.data_model: CCBrowserView = self.data_model

    @auto_reload
    def _reload(self):
        pass

    def update_suggestion_list(self):
        height = self.suggestion_list._h
        query = self.search.value.lower()
        if not query:
            self.suggestion_list.options = []
            return
        partial_matches = []
        for potential_match in list(self.data_model._index.keys()):
            if query in potential_match:
                partial_matches.append(potential_match)
        
        sorted_matches = sorted(partial_matches, key=len)
        suggestions = [(match, idx) for idx, match in enumerate(sorted_matches)]
        self.suggestion_list.options = suggestions[:height]
        

    def set_selection_path(self, selection_path:list, initial_key):
        listbox_dict = {"Class":self.class_list, 
                        "Family":self.family_list, 
                        "Component":self.component_list, 
                        "Element":self.element_list}

        current_key = initial_key
        while selection_path:
            selection = selection_path.pop(0)
            for option, idx in listbox_dict[current_key].options:
                if selection._id == option.lower():
                    listbox_dict[current_key].value = idx
            self.display_selection_data(current_key)
            current_key = self.get_next_key(current_key, listbox_dict)

    def process_match(self, match):
        # get ancestors and delete root object CCDocument
        ancestors = match.get_ancestors()[:-1]
        
        # determine if match is already Class
        if ancestors:
            matched_class = ancestors[-1]
        else:
            matched_class = match
        # determine if match is of domain functional or assurance based on class match
        if isinstance(matched_class, cct.FClass):
            self.domain_list.value = 0 # corresponds to functional
        else:
            self.domain_list.value = 1 # corresponds to assurance
        # load respective classes
        self.load_classes()
        
        # reverse ancestor list to match sequence of listbox (Class, Family, Component, Element)
        selection_path = list(reversed(ancestors))
        selection_path.append(match)
        self.set_selection_path(selection_path, "Class")

    def search_item(self):
        INVALID_MATCH_TYPES = [cct.Package, cct.CCDocument, cct.WorkUnit, cct.Operation]

        query = self.search.value
        try:
            match = self.data_model.find(query)
        except KeyError:
            match = None

        if not match or type(match) in INVALID_MATCH_TYPES:
            self.update_status(f"No matches found for {query}!")
            return
        
        self.process_match(match)
        self.update_status(f"Selection path for {query} opened.")

    def set_search_value(self):
        query, _ = self.suggestion_list.options[self.suggestion_list.value]
        self.search.value = query
        self.search_item()

    def save_selection(self, blacklist=None):
        blacklist = blacklist or list()
        selection = []
        for widget in self.builder.widgets:
            try:
                if isinstance(widget, tuple):
                    widget = widget[0]
                if widget.name != "Domain" and widget.name not in blacklist:
                    is_selectable = widget.options
                    selection.append(widget)
            except AttributeError:
                pass
        self.data_model.selection = selection

    def update_status(self, value):
        self.statusbar.value = value

    def open_popup(self):
        # This will display the CustomPopUp and ask the user for input
        self.save_selection(blacklist=["SuggestionBox"])
        success = self._scene.add_effect(BrowserExportMenu(self._screen, self.data_model,
                                        on_close_callback= self.update_status))
        if success:
            self.update_status("Selection successfully exported.")

    def get_next_key(self, current_key, dictionary):
        keys = iter(dictionary)
        for key in keys:
            if key == current_key:
                return next(keys, None)
        return None

    @auto_cache
    def load_classes(self):
        domain = self.domain_list.value
        if domain == 0:
            get_object = cct.FClass
        if domain == 1:
            get_object = cct.AClass
        classes = self.data_model.yield_obj(get_object)
        class_ids = [CCclass._id.upper() for CCclass in classes]
        self.class_list.options = self.get_display_options(class_ids)
        self._clear_children_tabs("Class")
        #return self.class_list

    def get_children_ids(self, item_obj):
        children_ids = [child._id.upper() for child in item_obj.children]
        return children_ids
    
    def get_display_options(self, options):
        return [(option, i) for i, option in enumerate(options)]

    @auto_cache
    def display_selection_data(self, name):
        listbox_dict = {"Class":self.class_list, 
                        "Family":self.family_list, 
                        "Component":self.component_list, 
                        "Element":self.element_list}

        index = self.data_model
        listbox = listbox_dict[name]
        next_list = self.get_next_key(name, listbox_dict)

        idx = listbox.value
        if idx == None:
            self.statusbar.value = "Empty selection."
            return
        item, _ = listbox.options[idx]
        item_obj = index.find(item)
        self.preview.value = item_obj.get_formatted_text()

        if next_list:
            children = self.get_children_ids(item_obj)
            children_options = self.get_display_options(children)
            listbox_dict[next_list].options = children_options
            log.debug(f"Set options for {next_list}: {children_options}")
            self._clear_children_tabs(next_list)

            #return listbox_dict[next_list]

    # @auto_cache
    def _clear_children_tabs(self,level):
        '''Clears the areas of the CC browser screen
           that are to the right of the given level
           :param level: one of {Class, Familiy, Component, Element}
           :type level: string
        '''
        d_tabs = {"Class":self.class_list, 
                  "Family":self.family_list, 
                  "Component":self.component_list, 
                  "Element":self.element_list}

        while level:=self.get_next_key(level, d_tabs):
            log.debug(f"Cleaning options for {level}")
            d_tabs[level]._options = []



class BrowserExportMenu(PopUpMenu): 
    SUPPORTED_EXPORT_FORMATS = (".md")
    def __init__(self, screen, data, on_close_callback=None):

        self._screen = screen
        self.export_data = data
        self._on_close_callback = on_close_callback
        self.empty_selection = False

        max_height = screen.height//2
        frame_height = max_height - 5
        max_width = screen.width//2
        
        builder = Builder("Export Menu")
        builder.addLayout([40, 70])

        selection_options = []
        selection_preview = ""
        for selectable in data.selection:
            selection_options.append(selectable.name)
            log.debug(f"Categories: {selectable.name} - {selectable.value}")
            if selectable.value != None:
                header_level = len(selection_options)
                selection, _ = selectable.options[selectable.value]
                obj_text = data.find(selection).get_formatted_text(header_level)
                selection_preview += "\n" + obj_text

        dropdown_options = []
        for selection in data.selection:
            dropdown_item = f"'{selection.name}' Selection"
            dropdown_options.append(dropdown_item)

        builder.add_label("Export Settings", position=0, gap=True)
        self.dropdown = builder.addDropdownList("", "dlist", options=dropdown_options, position=0,
                                on_change=self.update_settings)

        self.depth = builder.addChoose("exportoptions", position=0, options=["Only selected component", "Include subcomponents"],
                          on_change=self.update_settings)

        builder.add_label("",0,True)

        self.export_path = builder.add_textbox("Filepath", "filepath", height=1, position=0)
        self.validation_info = builder.addText("", "info", position=0, disabled=True)

        builder.add_label("Preview", position=1)
        self.preview = builder.add_textbox("", "previewbox", height=frame_height, position=1)
        self.preview.value = selection_preview

        super(BrowserExportMenu, self).__init__(screen, builder,
                                        on_close_callback=on_close_callback, footer="Export")
        self.builder = builder
        self.initial_selection = selection_preview
        if not selection_preview:
            self.empty_selection = True

    @auto_reload
    def _reload(self):
        pass

    def update_settings(self):
        # if current path is selected set to initial and return
        if self.dropdown.value == 0:
            self.preview.value = self.initial_selection
            return
        
        selection = None
        selected_domain, _ = self.dropdown.options[self.dropdown.value]
        for selectable in self.export_data.selection:
            if selectable.name in selected_domain and selectable.value != None:
                selection, _ = selectable.options[selectable.value]

        if selection:
            data_object = self.export_data.find(selection)
        else:
            self.preview.value = "Selection empty."
            return
        explicit = data_object.get_formatted_text()
        if self.depth.value == 1:
            ancestors = data_object.get_ancestors()
            descendants = data_object.get_descendants()
            for descendant in descendants:
                header_level = (len(descendant.get_ancestors()) - len(ancestors)) + 1
                explicit += descendant.get_formatted_text(header_level)
        self.preview.value = explicit

    def validate_path(self, path):
        directory, filename = os.path.split(path)
        if not directory:
            directory = "."
        if not os.path.exists(directory):
            return False
        if not filename.lower().endswith(self.SUPPORTED_EXPORT_FORMATS):
            return False
        return True

    def _submit(self):
        if self.empty_selection:
            self._on_close_callback("Empty selection.")
            self._close()
            return
        filepath = self.export_path.value.strip()
        if self.validate_path(filepath):
            with open(filepath, "w+") as file:
                file.write(self.preview.value)
            if self._on_close_callback:
                self._on_close_callback(f"Successfully exported to file {filepath}")
            self._close()
        self.validation_info.value = "Invalid filepath."
        

class CreateChecklistModel(ArtifactModel):
    
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(CreateChecklistModel, self).__init__()

        self.selection = []
        
class CreateChecklistView(BaseView):
    CACHE = {}

    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation and 
        abstractions over doorstop.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self._screen = screen
        self.data_model = model

        app: Application = root_menu.get_ref_to_app()

        max_height = screen.height
        frame_height = max_height - 9
        max_width = screen.width

        builder = Builder("Evaluation Checklist - Creation")
        builder.addLayout([20, 10, 10, 60], True)

        # Input
        
        builder.add_label("Packages", position=0, disabled=True)
        builder.addDivider(True, position=0)
        self.package_list = builder.addListBox("Package", height=(frame_height//2)-2, position=0, 
                                                on_select=lambda: self.toggle_selection("Package"))
        self.package_list.options = self.get_packages()
        builder.addDivider(True, position=0)

        builder.add_label("Search Bar", position=0, disabled=True)
        self.search = builder.add_textbox("", "searchbox", height=1, position=0)
        self.search.value = "Search"
        self.search_button = builder.addButton("Search", position=0, on_click=self.search_item)

        builder.addDivider(True, position=0)
        builder.add_label("Actions", position=0, disabled=True)
        self.validate_button = builder.addButton("Validate Selection", position=0,
                                                 on_click=self.validate)
        self.auto_button = builder.addButton("Auto Complete Selection", position=0,
                                             on_click=self.auto_complete_selection)
        self.create_button = builder.addButton("Create Evaluation Checklist", position=0,
                                               on_click=self.open_form, name="Create")
        self.create_button.disabled = True

        builder.add_label("Select Item(s)", position=1, disabled=True)
        builder.addDivider(True, position=1)
        self.component_list = builder.addListBox("Component", height=frame_height-5, position=1, 
                                          on_select=lambda: self.toggle_selection("Component"))
        self.component_list.options = self.get_components()

        builder.add_label("Current Selection", position=2, disabled=True)
        builder.addDivider(True, position=2)
        self.selection_list = builder.addListBox("Selection", height=frame_height-4, position=2,
                                                on_select=lambda: self.display_selection("Selection"))
        self.deselect_button = builder.addButton("Deselect", position=2, on_click=self.deselect_option)
        self.clear_button = builder.addButton("Clear", position=2, on_click=self.clear_selection)

        builder.add_label("Item Preview", position=3, disabled=True)
        builder.addDivider(True, position=3)
        self.preview = builder.add_textbox("", "previewbox", height="max", position=3, readonly=True)

        # Output
        builder.addLayout([50,50])
        builder.addDivider(True)
        self.statusbar = builder.addStatusBar()
        builder.addDivider(True, position=1)
        self.export = builder.addButton("Open Export Menu", on_click=self.open_popup, position=1)

        super(CreateChecklistView, self).__init__(screen, root_menu, builder)
        self._reload()
        self.builder = builder
        self.data_model: CreateChecklistView = self.data_model

    @auto_reload
    def _reload(self):
        pass

    def get_display_options(self, options):
        return [(f"{state} {name}", i) for i, (name, state) in enumerate(options)]

    def get_packages(self):
        packages = self.data_model.yield_obj(cct.Package)
        package_options = [(package._id.upper(), '[ ]') for package in packages]
        options = self.get_display_options(package_options)
        return options
    
    def get_components_for_package(self, package):
        index = self.data_model
        package = index.find(package)
        package_components = [comp._id.upper() for comp in package.components]
        return package_components
    
    def get_components(self):
        components = self.data_model.yield_obj(cct.AComponent)
        component_options = [(component._id.upper(), '[ ]') for component in components]
        options = self.get_display_options(component_options)
        return options 

    def generate_preview(self, item):
        index = self.data_model
        item_obj = index.find(item)
        self.preview.value = item_obj.get_formatted_text()

    def clear_component_selection(self):
        listbox = self.component_list
        for option, idx in listbox.options:
            if '[X]' in option:
                toggle = option.replace('[X]', '[ ]')
                listbox.options[idx] = (toggle, idx)
        self.component_list.options = listbox.options
    
    def clear_package_selection(self):
        listbox = self.package_list
        for option, idx in listbox.options:
            if '[X]' in option:
                toggle = option.replace('[X]', '[ ]')
                listbox.options[idx] = (toggle, idx)
        self.package_list.options = listbox.options

    def deselect_option(self):
        if not self.selection_list.options:
            return
        idx = self.selection_list.value
        item, _ = self.selection_list.options[idx]
        listbox_options = self.component_list.options
        for option, idx in listbox_options:
            if item in option:
                listbox_options[idx] = ('[ ] ' + item, idx)
        self.component_list.options = listbox_options
        self.update_selection_list()
        self.validate()

    @auto_cache
    def update_component_selection(self, selection, mode="add"):
        listbox = self.component_list
        if mode == "add":
            for item in selection:
                for option, idx in listbox.options:
                    if item.upper() in option and '[ ]' in option:
                        toggle = option.replace('[ ]', '[X]')
                        listbox.options[idx] = (toggle, idx)
        elif mode == "delete":
            for item in selection:
                for option, idx in listbox.options:
                    if item.upper() in option and '[X]' in option:
                        toggle = option.replace('[X]', '[ ]')
                        listbox.options[idx] = (toggle, idx)

        self.component_list.options = listbox.options
        self.update_selection_list()
        return self.component_list

    @auto_cache
    def update_selection_list(self):
        selection_list = []
        selection_idx = 0
        for option, idx in self.component_list.options:
            if '[X]' in option:
                selection_list.append([option.split(' ')[-1], selection_idx])
                selection_idx += 1
        self.selection_list.options = selection_list
        return self.selection_list

    def auto_complete_selection(self):
        selected_components = [component for component, idx in self.selection_list.options]
        _, valid_set = cct.validate_dependencies(selected_components)
        self.clear_component_selection()
        self.update_component_selection(valid_set)
        self.validate()

    def clear_selection(self):
        self.clear_component_selection()
        self.clear_package_selection()
        self.update_selection_list()
        self.statusbar.value = "Selection cleared."
        self.validate()

    @auto_cache
    def toggle_selection(self, name):
        listbox_dict = {"Package":self.package_list, 
                        "Component":self.component_list, 
                        "Selection":self.selection_list}
        listbox = listbox_dict[name]
        idx = listbox.value
        option, _ = listbox.options[idx]

        if '[ ]' in option:
            toggle = option.replace('[ ]', '[X]')
            listbox.options[idx] = (toggle, idx)
            self.generate_preview(toggle.split(' ')[-1])

        else:
            toggle = option.replace('[X]', '[ ]')
            listbox.options[idx] = (toggle, idx)
            self.preview.value = ""

        if name == "Package":
            self.clear_component_selection()
            for package, _ in self.package_list.options:
                if '[X]' in package:
                    package_id = package.split(' ')[-1]
                    components = self.get_components_for_package(package_id)
                    self.update_component_selection(components, mode="add")
                    
        listbox_dict[name] = listbox
        self.update_selection_list()
        self.validate()
    
        return listbox_dict[name]

    def display_selection(self, name):
        listbox = self.find_widget(name)
        idx = listbox.value
        item, _ = listbox.options[idx]
        self.generate_preview(item.split(' ')[-1])

    def validate_package_selection(self):
        index = self.data_model
        selected_package = 0
        listbox = self.package_list
        for option in listbox.options:
            if '[X]' in option[0]:
                selected_package += 1
        if selected_package > 1:
            self.statusbar.value = "Only one Package can be selected."
            self.create_button.disabled = True
            return False
        elif selected_package == 0:
            self.statusbar.value = "Empty Selection."
            self.create_button.disabled = True
            return False
        else:
            self.statusbar.value = "Selection valid!"
            self.create_button.disabled = False
            return True

    @auto_cache
    def validate(self):
        selected_components = []
        listbox = self.selection_list
        for option, _ in listbox.options:
            selected_components.append(option.lower())
        is_valid, valid_set = cct.validate_dependencies(selected_components)
        if not is_valid:
            self.statusbar.value = f"Selection Invalid! Valid set based on your selection {valid_set}"
            self.create_button.disabled = True
        elif len(selected_components) == 0:
            self.statusbar.value = "Empty Selection."
            self.create_button.disabled = True
        else:
            self.statusbar.value = "Selection valid!"
            self.create_button.disabled = False
        
        return [self.statusbar, self.create_button]

    def save_selection(self, blacklist=None):
        blacklist = blacklist or list()
        selection = []
        for widget in self.builder.widgets:
            try:
                if isinstance(widget, tuple):
                    widget = widget[0]
                if widget.name != "Domain" and widget.name not in blacklist:
                    is_selectable = widget.options
                    selection.append(widget)
            except AttributeError:
                pass
        self.data_model.selection = selection

    def update_status(self, value):
        self.statusbar.value = value

    def open_popup(self):
        # This will display the CustomPopUp and ask the user for input
        self.save_selection(blacklist=["Selection"])
        success = self._scene.add_effect(CreationExportMenu(self._screen, self.data_model,
                                        on_close_callback=self.update_status))
        if success:
            self.update_status("Selection successfully exported.")

    def search_request_handler(self, query, matching_components, selection=2):
        if selection == 2:
            query_obj = self.data_model.find(query)
            self.update_component_selection(matching_components, mode="add")
            self.preview.value = query_obj.get_formatted_text()
            self.statusbar.value = f"{query} found and added to Selection."
        elif selection == 0:
            first_query_obj = self.data_model.find(matching_components[0])
            self.update_component_selection(matching_components, mode="add")
            self.preview.value = first_query_obj.get_formatted_text()
            self.statusbar.value = f"{query} Class/Family Components added to Selection."
        else:
            self.statusbar.value = f"{query} not found!"

    def search_item(self):
        query = self.search.value.upper()

        class_match = False
        family_match = False
        component_match = False

        matching_components = []

        for item, idx in self.component_list.options:
            pruned_item = item.split(' ')[-1]
            if query == pruned_item:
                component_match = True
                matching_components.append(pruned_item)

            elif pruned_item.startswith(query):
                matching_components.append(pruned_item)
                if "_" not in query:
                    class_match = True
                else:
                    family_match = True
            
        if component_match:
            self.search_request_handler(query, matching_components)
            return
        elif family_match or class_match:
            self._scene.add_effect(
            PopUpDialog(self._screen, "Select Class/Family Components?", ["Yes", "No"],
                        on_close=lambda selection: self.search_request_handler(query, 
                        matching_components, selection)))
            return
        self.statusbar.value = f"{query} not found!"

    def create_request_handler(self, selection):
        if selection == 0:
            raise NextScene("Evaluation Checklist")
        
    def open_form(self):
        # This will display the CustomPopUp and ask the user for input
        self._scene.add_effect(FormView(self._screen, 
        on_close_callback=self.create_evaluation_checklist))

    def create_evaluation_checklist(self, info):
        gen_info = {"GeneralInfo" : {**{"CCVersion": self.data_model.cc_version}, **info}}
        index = self.data_model
        components = [index.find(component) for component, _ in self.selection_list.options]
        usr_prefix = info["identifier"]

        try:
            log.debug(f"save in : {self.data_model.project_root} - with prefix: {usr_prefix}")
               # abort if a doorstop document with the same prefix exists
            if(doorstop.find_document(usr_prefix)):
                self.statusbar.value = f"ERROR: The selected prefix '{usr_prefix}' is already in use in your repository."
                
        except doorstop.common.DoorstopError as x:
            log.debug(f"Doorstop error: {x}")
            try:
                cct.create_evaluation_checklist(components, gen_info, 
                                        export_path=self.data_model.project_root, 
                                        doc_prefix=usr_prefix)
                self._scene.add_effect(PopUpDialog(self._screen, 
                                        "Proceed to Evaluation Checklist?", ["Yes", "No"],
                                        on_close=self.create_request_handler,
                                        theme="bright"))
                self.statusbar.value = "Evaluation Checklist successfully created!"
            except doorstop.common.DoorstopError as e:
                self.statusbar.value = f"{e}"
            

class FormView(PopUpMenu):

    def __init__(self, screen, on_close_callback):

        builder = Builder("Enter Details")
        builder.addLayout([100], True)

        self.identifier = builder.addText("Evaluation Identifier", "labelx")
        self.creator = builder.addText("Creator","label1")
        self.date = builder.addText("Creation Date", "label2")
        builder.addButton("Today", on_click=self.get_date)
        
        super(FormView, self).__init__(screen, builder, 
        on_close_callback=on_close_callback, footer="Create")
        self.builder = builder

    @auto_reload
    def _reload(self):
        pass
    
    def get_date(self):
        date = datetime.now().date()
        self.date.value = str(date)

    def get_attribute_dict(self):
        keys = ["identifier", "creator", "date"]
        _attributes = {}
        for key in keys:
            _attributes[key] = getattr(self, key).value
        return _attributes

    def _submit(self):
        if self._on_close_callback:
            attributes = self.get_attribute_dict()
            self._on_close_callback(attributes)
        self._close()

class CreationExportMenu(PopUpMenu): 
    SUPPORTED_EXPORT_FORMATS = (".md")
    def __init__(self, screen, data, on_close_callback=None):

        self._screen = screen
        self.export_data = data
        self._on_close_callback = on_close_callback
        self.empty_selection = False

        max_height = screen.height//2
        frame_height = max_height - 5
        max_width = screen.width//2

        builder = Builder("Export Menu")
        builder.addLayout([30, 70])

        dropdown_options = ["Current Selection"]
        for selection in data.selection:
            dropdown_item = f"'{selection.name}' Selection"
            dropdown_options.append(dropdown_item)

        builder.add_label("Export Settings", position=0)
        self.dropdown = builder.addDropdownList("", "dlist", options=dropdown_options, position=0,
                                on_change=self.update_settings)

        self.depth = builder.addChoose("exportoptions", position=0, options=["Only selected component", "Include subcomponents"],
                          on_change=self.update_settings)
        self.export_path = builder.add_textbox("Filepath", "filepath", height=1, position=0)
        self.validation_info = builder.addText("", "info", position=0, disabled=True)
                          
        builder.add_label("Preview", position=1)
        self.preview = builder.add_textbox("", "previewbox", height=frame_height, position=1)
        self.preview.value = self.load_initial_selection()

        super(CreationExportMenu, self).__init__(screen, builder,
                                        on_close_callback=on_close_callback, footer="Export")
        self.builder = builder
        

    @auto_reload
    def _reload(self):
        pass

    def get_text(self, obj_, level=1.0):
        obj_text = obj_.get_formatted_text(level)
        level += 1
        if self.depth.value == 1:
            for child in obj_.children:
                obj_text += self.get_text(child, level=level)
        return obj_text

    def prune_list(self, original_list, remove_list):
        pruned_list = list(filter(lambda elem: elem not in remove_list, original_list))
        return pruned_list

    def load_initial_selection(self):

        selected_packages = []
        selected_components = []
        for selectable in self.export_data.selection:
            for option, _ in selectable.options:
                if '[X]' in option:
                    selection = option.split(' ')[-1]
                    if selectable.name == "Package":
                        selected_packages.append(selection)
                    else:
                        selected_components.append(selection)
        preview = ""
        if selected_packages:
            for package in selected_packages:
                pkg_obj = self.export_data.find(package)
                components = pkg_obj.components
                component_ids = [comp._id.upper() for comp in components]
                pkg_text = pkg_obj.get_formatted_text()
                components_text = ""
                for component in components:
                    components_text += self.get_text(component, level=2)
                preview += pkg_text + components_text
                selected_components = self.prune_list(selected_components, component_ids)

        if selected_components:
            # additional components were selected -> augmentation
            header_level = 1
            if selected_packages:
                preview += "\n# Augmentations\n"
                header_level = 2
            for component in selected_components:
                component_obj = self.export_data.find(component)
                preview += self.get_text(component_obj, level=header_level)

        if not any([selected_packages, selected_components]):
            self.empty_selection = True
            return
        return preview


    def update_settings(self):
        # if current path is selected set to initial and return
        if self.dropdown.value == 0:
            preview = self.load_initial_selection()
            self.preview.value = preview
            return
        else:
            selection = []
            selected_domain, _ = self.dropdown.options[self.dropdown.value]
            for selectable in self.export_data.selection:
                if selectable.name in selected_domain and selectable.value != None:
                    for option, _ in selectable.options:
                        if '[X]' in option:
                            selection.append(option.split(' ')[-1])
        preview = ""
        if not selection:
            self.preview.value = ""
            return

        for _id in selection:
            data_object = self.export_data.find(_id)
            preview += self.get_text(data_object)

        self.preview.value = preview

    def validate_path(self, path):
        directory, filename = os.path.split(path)
        if not directory:
            directory = "."
        if not os.path.exists(directory):
            return False
        if not filename.lower().endswith(self.SUPPORTED_EXPORT_FORMATS):
            return False
        return True

    def _submit(self):
        if self.empty_selection:
            self._on_close_callback("Empty selection.")
            self._close()
            return
        filepath = self.export_path.value.strip()
        if self.validate_path(filepath):
            with open(filepath, "w+") as file:
                file.write(self.preview.value)
            if self._on_close_callback:
                self._on_close_callback("Export successful!")
            self._close()
        self.validation_info.value = "Invalid filepath."
        


class WorkUnitModel(ArtifactModel):
    def __init__(self):
        """Set up the key attributes needed for requirements management.
        """
        super(WorkUnitModel, self).__init__()
        self.doc = None
        self.d_index = {}
        self.current_item = None
        self.current_unit = None

    def find_key_in_dict(self, d, target_key):
        if target_key in d.keys():  # base case
            return d[target_key]
        for key, value in d.items():
            if isinstance(value, dict):  # if value is a dictionary, recurse
                result = self.find_key_in_dict(value, target_key)
                if result:  # if found in the nested dictionary
                    return result
        return None  # not found

    def set_current(self, item):
        self.current_item = item
        self.current_unit = item._data["header"].upper()

    def get_item(self, item_id):
        log.debug(f"Search for: {item_id}")
        uid = self.find_key_in_dict(self.d_index, item_id.lower())["UID"]
        item = self.doc.find_item(uid)
        self.set_current(item)
        return item
    
    def update_item(self, item, _data):
        item._data = _data
        item.review()

    def get_item_status(self, item_id):
        item = self.get_item(item_id)
        status = item._data["verdict"]
        return status

    def update_index(self, item):
        index_entry = self.find_key_in_dict(self.d_index, item._data["header"].lower())
        index_entry["verdict"] = item._data["verdict"]
        index_entry["hash"] = item._data["reviewed"].value
        cct.save_index(self.d_index, self.doc.path)

    def update_item(self, data):
        """
        Update Work Unit with provided evaluation evidence and verdict.
        """
        item = self.current_item
        for key in list(data.keys()):
            item._data[key] = data[key]
        item.review()
        self.update_index(item)

class WorkUnitView(BaseView):
    CACHE = {}

    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        The REM module provides automation and 
        abstractions over doorstop.

        :param screen: the screen that displays this function
        :type screen: class `Screen`
        :param root_menu: the menu that owns this function
        :type root_menu: class `Menu`
        """
        self._screen = screen
        self.data_model = model
        app: Application = root_menu.get_ref_to_app()

        max_height = screen.height
        frame_height = max_height - 8
        max_width = screen.width
        narrow = max_width//10
        wide = (max_width*2)//5

        builder = Builder("Evaluation Checklist")
        builder.addLayout([narrow, narrow, wide, wide])

        builder.add_label("Checklist(s)", position=0, disabled=True)
        self.project_listbox = builder.addListBox("checklist", height=frame_height-3, options=[], 
                               position=0, on_select=self.load_units)
        self.load = builder.addButton("Load Evaluation Checklist(s)", position=0,
                                       on_click=self.load_evaluation_checklists)

        builder.add_label("Evaluation Items", position=1, disabled=True)
        self.unit_listbox = builder.addListBox("workunitlist", height=frame_height-2, options=[], 
                            position=1, on_select=self.load_item)

        builder.add_label("Evaluation Evidence", position=2, disabled=True)
        self.eval_evidence = builder.add_textbox("", "evalevidence", height=frame_height-5, position=2,
                                                on_change=self.toggle_verdict)
        self.pass_button = builder.addButton("Pass", position=2,
                                            on_click=lambda: self.update_item("pass"))
        self.pass_button.disabled = True
        self.fail_button = builder.addButton("Fail", position=2,
                                            on_click=lambda: self.update_item("fail"))
        self.fail_button.disabled = True
        self.inconclusive_button = builder.addButton("Inconclusive", position=2,
                                            on_click=lambda: self.update_item("inconclusive"))
        self.inconclusive_button.disabled = True
        
        builder.add_label("Work Unit", position=3, disabled=True)
        self.task_box = builder.add_textbox("", "taskbox", position=3, height=frame_height-2, readonly=True)
        
        # Output
        builder.addLayout([50, 20, 30])
        builder.addDivider(draw_line=True, position=0)
        self.statusbar = builder.addStatusBar()
        builder.addDivider(True, position=1)
        builder.addDivider(draw_line=True, position=2)
        self.progress = builder.addText("Evaluation Progress", "Test", position=2, disabled=True)
        
        super(WorkUnitView, self).__init__(screen, root_menu, builder)
        self._reload()
        self.builder = builder

    @auto_reload
    def _reload(self):
        pass

    @auto_cache
    def toggle_verdict(self, toggle=False):
        if not self.data_model.current_unit:
            return
        self.pass_button.disabled = toggle
        self.fail_button.disabled = toggle
        self.inconclusive_button.disabled = toggle
        return [self.pass_button, self.fail_button, self.inconclusive_button]

    @auto_cache
    def update_item(self, verdict):
        """
        Update Work Unit with provided evaluation evidence and verdict.
        """
        if not self.data_model.current_unit:
            return
        data = {}
        data["evidence"] = self.eval_evidence.value
        data["verdict"] = verdict
        log.debug(f"New data = {data}")
        self.data_model.update_item(data)
        self.statusbar.value = self.data_model.current_unit + " updated."
        self.get_evaluation_progress()
        self.display_workunits()
        return self.statusbar

    @auto_cache
    def load_evaluation_checklists(self):
        documents = cct.get_evaluation_documents(self.data_model.project_root)
        project_prefix = [doc.prefix for doc in documents]
        self.project_listbox.options = self.to_options(project_prefix)
        if project_prefix:
            self.statusbar.value = f" {len(project_prefix)} Evaluation Project/s found!"
        else:
            self.statusbar.value = "No Evaluation Project found! Please create Evaluation Checklist."
        return [self.project_listbox, self.statusbar]

    @auto_cache
    def load_units(self):
        with common.Capture(catch=True) as success:
            idx = self.project_listbox.value
            project_prefix, _ = self.project_listbox.options[idx]
            self.data_model.doc = cct.get_doorstop_document(self.data_model.project_root, project_prefix)
            log.debug(f"Load eval list in document: {self.data_model.doc.path}")
            index = cct.load_index(self.data_model.doc.path)
            cct.validate_index(index)
            self.data_model.d_index = index
            self.display_workunits()
            self.get_evaluation_progress()
            self.statusbar.value = f"Project {project_prefix} successfully loaded and validated!"
        if not success:
            self.statusbar.value = "An error occur when loading and validating the project."
        return self.statusbar

    def to_options(self, options: list) -> list:
        option_list = []
        for idx, option in enumerate(options):
            option_list.append((option, idx))
        return option_list

    def get_workunits_from_index(self, index):
        workunits = {}
        for _, data in index["Components"].items():
            comp_units = data["workunit"]
            for unit, data in comp_units.items():
                workunits[unit] = data
        return workunits

    @auto_cache
    def display_workunits(self):
        index = self.data_model.d_index
        log.debug(f"INDX: {index}")
        units = self.get_workunits_from_index(index)
        workunits = []
        for unit, data in units.items():
            if data["verdict"] != "inconclusive":
                unit_string = unit.upper() + "\t" + data["verdict"]
            else:
                unit_string = unit.upper()
            workunits.append(unit_string)
        workunit_options = self.to_options(workunits)
        self.unit_listbox.options = workunit_options
        log.debug(f"Workunits: {self.unit_listbox.options}")
        return self.unit_listbox
        
    def format_data(self, data, section_dict, delimiter, width):
        delimiter = delimiter * width
        display_lines = []
        for section in section_dict.values():
            # Add formatted header
            padding = " " * ((width - len(section["header"]))//2)
            padded_header = padding + section["header"] + padding
            display_lines.append(padded_header)
            display_lines.append(delimiter)
            # Add content based on keys
            for key, desc in section["keys"]:
                if desc:
                    if isinstance(data[key], list):
                        for k, d in zip(data[key], data[desc]):
                            display_lines.extend([d[2:], delimiter])
                    else:
                        display_lines.extend([data[desc][2:], delimiter])
                else:
                    display_lines.append(data[key])
                    display_lines.append(delimiter)
        return "\n".join(display_lines)

    def display_item_data(self, item_data: dict):
        if item_data["evidence"]:
            self.eval_evidence.value = item_data["evidence"]
        else: 
            self.eval_evidence.value = "Insert Evaluation Evidence."
        sections = {
            "evaluation": {
                "header": "EVALUATOR ACTION ELEMENT",
                "keys": [("element", "element_description")]
            },
            "content": {
                "header": "CONTENT OR DEVELOPER ELEMENT",
                "keys": [("dc_element", "dc_element_description")]
            },
            "work_unit": {
                "header": "WORK UNIT TASK",
                "keys": [("text", None)]
            }
        }
        width = self.task_box.width
        delimiter = "-"
        self.task_box.value = self.format_data(item_data, sections, delimiter, width)

    def extract_wu_id(self, displayed_workunit):
        # extract an evaluation item's id from a string
        # formatted by display_workunits()
        return displayed_workunit.split('\t')[0]

    def load_item(self):
        ''' Load an item into memory
        '''
        data = self.data_model
        # get the ListBox tuple for the currently selected value
        workunit, _ = self.unit_listbox.options[self.unit_listbox.value]
        log.debug(f"Displayed workunit = {workunit}")
        workunit = self.extract_wu_id(workunit)
        log.debug(f"Clean workunit ID = {workunit}")
        item = data.get_item(workunit)
        data = item._data
        self.display_item_data(data)
        self.toggle_verdict(True)
        
    def extract_verdicts(self):
        index = self.data_model.d_index
        for component in index["Components"].values():
            for workunit in component["workunit"].values():
               yield workunit["verdict"]
    
    def get_evaluation_progress(self):
        verdicts = list(self.extract_verdicts())
        total = len(verdicts)
        if total == 0:
            progress = None
        passed = 0
        for verdict in verdicts:
            if verdict == "pass":
                passed += 1
        progress = (passed/total)*100
        self.display_evaluation_progress(progress)
    
    @auto_cache
    def display_evaluation_progress(self, progress):
        progress_string = str(int(progress)) + "%"
        width = self.progress.width
        pad = " " * ((width - len(progress_string))//2)
        self.progress.value = pad + progress_string + pad
        return self.progress

    def update_status(self, value):
        self.statusbar.value = value

    