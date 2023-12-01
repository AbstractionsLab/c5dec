from asciimatics.widgets import Layout, Button, Divider, Frame
from asciimatics.screen import Screen
from asciimatics.exceptions import NextScene, StopApplication
from c5dec.frontend.tui.foundation.builder import Builder
import c5dec.settings as c5settings
import c5dec.frontend.tui.application as app_mod
from c5dec import common
import json
from i18n import t as translate
from abc import ABC, abstractmethod


class Menu:
    """The model of the menu.
    
    As everything should be in a MVC model, this class is the 'model'
    of the menus.
    """

    def __init__(self, name):
        """Set up the key attributes of a menu.
        
        It has a name, functions, submenus and if applicable a 
        root menu.

        :param name: name of the menu
        :type name: str
        """
        self.name = translate(name)
        self.functions = {}
        self.submenus = {}
        self.root_menu = None

    def add_function(self, name, classtype, data_model=None):
        """Add a function to the menu.
        
        :param name: the name of the function
        :type name: str
        :param classtype: the function type (App type)
        :type classtype: class
        """
        name = translate(name)
        self.functions.update({name: classtype})

        app: app_mod.Application = self.get_ref_to_app()
        app.set_data_model(name, data_model)

    def add_menu(self, name):
        """Add a submenu to the menu.
        
        :param name: name of the menu that is added
        :type name: str
        """
        name = translate(name)
        self.submenus.update({name : Menu(name)})
        self.get_submenu(name).root_menu = self
    
    def get_ref_to_app(self):
        root_menu_type = type(self.root_menu)
        if root_menu_type is app_mod.Application:
            return self.root_menu
        
        parent = None
        while root_menu_type is not app_mod.Application:
            parent = self.root_menu.root_menu
            root_menu_type = type(parent)
        
        return parent
    
    def get_submenu(self, name):
        """Return a submenu by taking its name.
        
        :param name: the name of the requested menu
        :type name: str

        :return: The requested menu 
        :rtype: class `Menu`
        """
        name = translate(name)
        return self.submenus[name]

    def get_nested_submenu(self, list):
        """Return a nested submenu with a list of names to the menu.
        
        :param list: list of the root menus' names of the requested menu
        :type list: list
        
        :return: The requested menu
        :rtype: class `Menu`
        """
        menu = self
        for i in list:
            menu = menu.get_submenu(i)
        return menu

    def get_path(self):
        """Get the path to get to the current menu.
        
        :return: The list of menus to get to the current menu
        :rtype: list
        """
        root = self.root_menu
        if not root:
            return []
        else:
            path = [root]
        while root.root_menu:
            root = root.root_menu
            path.append(root)
        path.reverse()
        path_with_names = [i.name for i in path]
        return path_with_names

    def get_all_submenus(self):
        """Get all submenus (also nested) of a menu as objects.
        
        :return: List of all submenus (and its submenus) in a menu
        :rtype: list
        """
        all_submenus = list(self.submenus.values())
        index = 0
        while index < len(all_submenus):
            cur_menu = all_submenus[index]
            cur_submenus = list(cur_menu.submenus.values())
            all_submenus.extend(cur_submenus)
            index += 1
        return all_submenus
    
    def get_submenus(self):
        """Get a list of submenus of a menu.
        
        :return: List of submenu names
        :rtype: list
        """
        return list(self.submenus.keys())

    def get_functions(self):
        """Get a list of functions of a menu.
        
        :return: List of functions of the menu
        :rtype: list
        """
        return list(self.functions.keys())

class BaseView(Frame):
    """The template for all scenes created in this program.

    The 'Template' class is an asciimatics Frame on which all other
    scenes can be built on using additionally the 'Builder'. 
    """
    def __init__(self, screen, root_menu, builder=None):
        """Set up the basic elements of a scene.

        These elements are the size of the screen and the footer. This
        footer contains the 'back' and the 'quit' button. In addition,
        add the builder to enable to build on this basic template.

        :param screen: the screen on which the Frame should be shown
        :type screen: class `Screen`
        :param root_menu: the root menu of the assigned menu
        :type root_menu: class `Menu`
        :param builder: the builder who adds the content of the frame,
            defaults to None
        :type builder: class `Builder`, optional
        """
        self.root_menu = root_menu
        self.menu_title = "Default title"
        self.builder = builder

        # Configure the title.
        if builder:
            title = builder.title
        else:
            title = "Template"

        width = common.get_value_from_json("width", 90)
        height = common.get_value_from_json("height", 90)

        # Initialize the screen.
        super(BaseView, self).__init__(
            screen,
            screen.height*height // 100,
            screen.width*width // 100,
            hover_focus=True,
            can_scroll=True,
            title=translate(title),
            has_border=True
            )
        
        self.assemble()

        self.fix()

    def back(self):
        """Get back to the previous menu."""
        scene = self.root_menu.name
        raise NextScene(scene)

    @staticmethod
    def quit():
        """Quit the application."""
        raise StopApplication("User pressed quit")

    def assemble(self):
        # Insert the builder and its configuration.
        builder = self.builder
        if builder:
            widgets = builder.build()
            for element in widgets:
                if isinstance(element, Layout):
                    layout = element
                    self.add_layout(layout)
                else:
                    widget = element[0]
                    position = element[1]
                    layout.add_widget(widget, position)
        else:
            layout = Layout([100], fill_frame=True)
            self.add_layout(layout)

        # Add the footer, containing the 'back' and 'quit' button.
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout = Layout([1, 1, 1, 1])
        self.add_layout(layout)
        back_button = Button(translate("Back"), self.back)
        layout.add_widget(back_button, 0)
        if not self.root_menu:
            back_button.disabled = True
        layout.add_widget(Button(translate("Quit"), self.quit), 3)

    def get_value_from_json(self, key, default_value):
        """Returns the corresponding value to a key in the config.json
        file.

        :param key: the setting whose value is searched
        :type key: str
        :param default_value: the value that will be used if the file 
            cannot be loaded
        :type default_value: str or int

        :return: the value that belongs to the entered key
        :rtype: str or int
        """
        try:
            with open(c5settings.STARTUP_CONFIG_JSON_PATH) as f:
                dictionary = json.load(f)
                value = dictionary[key]
        except:
            value = default_value
        
        return value
    
    def clear_text_fields(self, field_list):
        for fl in field_list:
            fl.value = ""

    def setController(self, controller):
        """Assign a controller to the view.

        :param controller: the controller that is assigned to the view
        :type controller: class `Controller`
        """
        self.controller = controller

    def set_data_model(self, model):
        self.data_model = model

    def get_data_model(self):
        return self.data_model
    
    def get_menu_title(self):
        return self.menu_title
    
    def set_menu_title(self, title):
        self.menu_title = title

class PopUpMenu(Frame, ABC):
    """The template for all PopUp Menus created in this program.

    The 'PopUpMenu Template' class is a modal asciimatics Frame that
    creates an overlay over the invoking Frame. 
    """
    # Default Frame pattern
    _default_popup = {
        "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_CYAN),
        "shadow": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLACK),
        "disabled": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "invalid": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "borders": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_CYAN),
        "scroll": (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "title": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_CYAN),
        "focus_edit_text": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_WHITE),
        "readonly": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_readonly": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_WHITE),
        "control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_CYAN),
        "selected_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "focus_control": (Screen.COLOUR_YELLOW, Screen.A_NORMAL, Screen.COLOUR_WHITE),
        "selected_focus_control": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_WHITE),
        "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_CYAN),
        "selected_field": (Screen.COLOUR_CYAN, Screen.A_BOLD, Screen.COLOUR_WHITE),
        "focus_field": (Screen.COLOUR_CYAN, Screen.A_NORMAL, Screen.COLOUR_WHITE),
        "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_WHITE),
    }

    def __init__(self, screen, builder=None, on_close_callback=None, footer=None, palette=None):
        """Set up the PopUp Menu.
        
        :para, screen: the screen on which the Frame should be shown
        :type screen: class 'Screen'
        :param builder: the builder who adds the content of the frame,
            defaults to None
        :type builder: class 'Builder', optional
        :param on_close_callback: the function to catch the return of
            PopUpMenu
        :type on_close_callback: class 'function'
        :param footer: footer labels, defaults to 'Submit' and 'Cancel'
            only 'Submit' can be 'changed'.
        :type footer: string
        """
        self._screen = screen
        self.builder = builder
        self._on_close_callback=on_close_callback
        self._footer = footer
        # Configure the title.
        if builder:
            title = builder.title
        else:
            title = "PopUpTemplate"

        super(PopUpMenu, self).__init__(screen,
                                          screen.height // 2,
                                          screen.width // 2,
                                          has_border=True,
                                          can_scroll=False,
                                          is_modal=False,
                                          hover_focus=True,
                                          title=translate(title))

        if not palette:
            self.palette = self._default_popup

        self.assemble()
        self.fix()

    def _close(self):
        """Close the Popup Menu"""
        self._scene.remove_effect(self)
    
    @abstractmethod
    def _submit(self):
        pass

    def assemble(self):
        # Insert the builder and its configuration.
        builder = self.builder
        if builder:
            widgets = builder.build()
            for element in widgets:
                if isinstance(element, Layout):
                    layout = element
                    self.add_layout(layout)
                else:
                    widget = element[0]
                    position = element[1]
                    layout.add_widget(widget, position)
        else:
            layout = Layout([100], fill_frame=True)
            self.add_layout(layout)

        # Add the footer, containing the 'back' and 'quit' button.
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Divider())
        layout = Layout([1, 1, 1, 1])
        self.add_layout(layout)
        if self._footer:
            proceed = self._footer
        else:
            proceed = "Submit"
        layout.add_widget(Button(translate(proceed), self._submit), 0)
        layout.add_widget(Button(translate("Close"), self._close), 3)

class MenuView(BaseView):
    """The 'view' of the menu.

    As everything should be in a MVC model, this class is the 'view'
    for the presentation of the menus.
    """
    def __init__(self, screen, menu):
        """Set up the view for the menus.

        The menus are displayed by showing their submenus and their 
        functions in two ListBoxes side by side. It is build on the
        universal template with the builder.

        :param screen: the screen the Frame should be displayed on
        :type screen: class: `Screen`
        :param menu: the menu the frame is assigned to
        :type menu: class: `Menu`
        """
        self.model = menu

        builder = Builder(menu.name)
        builder.addLayout([1,1], True)

        # Add the left ListBox with the submenus.
        self.listbox_submenus = builder.addListBox(
            "submenus", "max", on_select=self.launch_submenu, position=0
            )

        # Add the right ListBox with the functions.
        self.listbox_functions = builder.addListBox(
            "functions", "max", on_select=self.launch_function, position=1
            )

        # Build on the template.
        super(MenuView, self).__init__(screen, menu.root_menu, builder)

        self.builder = builder
        self.set_options()

    def set_options(self):
        """Get and insert the options of the ListBoxes."""
        self.submenus = self.model.get_submenus()
        self.insert(self.listbox_submenus, self.submenus)

        self.functions = self.model.get_functions()
        self.insert(self.listbox_functions, self.functions)

    def insert(self, widget, options):
        """Insert the options into the widget or disable the widget.

        :param widget: the widget whose options will be changed
        :type widget: class `Widget` 
        :param options: the options that will set to the widget
        :type options: list
        """
        if options:
            widget.options = self.builder.zipOfList(options)
        else:
            widget.disabled = True

    def launch_scene(self, widget_name, scene_list):
        """Launch the selected scene in a list of scenes.

        :param widget_name: the widget whose selected item
            should be received
        :type widget_name: str
        :param scene_list: the list of scenes you can choose
        :type scene_list: list
        """
        self.save()
        index = int(self.data[widget_name])
        next_scene = scene_list[index]
        raise NextScene(next_scene)

    def launch_function(self):
        """Launch the selected function."""
        self.launch_scene("functions", self.functions)

    def launch_submenu(self):
        """Launch the selected submenu."""
        self.launch_scene("submenus", self.submenus)