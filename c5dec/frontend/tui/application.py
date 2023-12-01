from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
from c5dec.frontend.tui.foundation.menu import Menu, MenuView
from i18n import t as translate
import sys
import i18n
import json
import c5dec.settings as c5settings


class Application(Menu):
    """The primary element of the program.

    The application creates and contains all scenes of the program.
    """
    def __init__(self):
        """Set up the Application, its template and language.
        
        :param app_name: the name of the app and title of the main menu,
            defaults to None
        :type app_name: str, optional 
        :param lang: the language in which the TUI will be displayed,
            defaults to en
        :type lang: str
        """
        app_name = self.get_value_from_json("title", "C5-DEC CAD")
        lang = self.get_value_from_json("language", "en")
        self.setLanguage(lang)
        self.menu_view = None
        super(Application, self).__init__(name=translate(app_name))
        self.data_models = {}

    def get_data_model(self, name):
        return self.data_models.get(name)
    
    def set_data_model(self, name, model):
        self.data_models[name] = model

    def demo(self, screen, scene, menu):
        """Create all the scenes.
        
        :param screen: the screen of the TUI (automatically passed)
        :type screen: class `Screen`
        :param scene: the starting scene of the TUI
        :type scene: class `Scene`
        :param menu: the main menu that is used to build up the program
        :type menu: class `Menu`
        """
        self.menu_view = MenuView(screen, menu)
        main_menu = self.menu_view
        scenes = [Scene([main_menu], -1, name=menu.name)]

        # Add all functions of the main menu to the scenes.
        submenus = menu.get_all_submenus()
        for function_name in list(menu.functions.keys()):
            scenes.append(
                Scene(
                    [menu.functions[function_name](screen, menu)],
                    -1,
                    name=function_name)
                )

        # Add all submenus and all its functions to the scenes
        for submenu in submenus:
            scenes.append(
                Scene(
                    [MenuView(screen, submenu)],
                    -1,
                    name=submenu.name)
                )
            for function_name in list(submenu.functions.keys()):
                function_view = submenu.functions[function_name](screen, submenu, self.get_data_model(function_name))
                scenes.append(
                    Scene(
                        [function_view],
                        -1,
                        name=function_name)
                    )

        # Play the scenes.
        screen.play(scenes, 
                    stop_on_resize=True, 
                    start_scene=scene, 
                    allow_int=True)

    def run(self):
        """Start the application and the tui.
        
        The arguments of the self.demo function are passed by the list
        arguments in the row below. 
        This function displays the scenes, so it starts the TUI
        """
        last_scene = None
        while True:
            try:
                Screen.wrapper(
                    self.demo, 
                    arguments=[last_scene, self],
                    catch_interrupt=False)
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene

    def setLanguage(self, lang):
        """Set the language of the tui.
        
        :param lang: the language in which the TUI should be displayed
        :type lang: str
        """
        lang_dict = {
            "en": {"english", "englisch", "anglais"},
            "de": {"german", "deutsch", "allemand"},
            "fr": {"french", "französisch", "francais"}
            }
        
        # Find the selected language.
        lang = lang.lower()
        for key, value in lang_dict.items():
            if lang == key or lang in value:
                lang = key
                break

        if lang not in lang_dict.keys():
            raise ValueError("Unknown language string")

        # Load the translations and translate.
        # import os
        i18n.load_path.append(c5settings.TRANSLATION_ASSETS_FOLDER_PATH)
        i18n.set('skip_locale_root_data', True)
        i18n.set('file_format', 'json')
        i18n.set('filename_format', '{locale}.{format}')
        i18n.set('locale', lang)

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