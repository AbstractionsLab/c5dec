from c5dec.frontend.tui.foundation.menu import Menu, BaseView, PopUpMenu
from c5dec.frontend.tui.foundation.builder import Builder
from c5dec.frontend.tui.application import Application
from asciimatics.widgets import PopUpDialog
from asciimatics.exceptions import NextScene
from datetime import datetime
import c5dec.settings as c5settings
import c5dec.common as common
import doorstop
import os
import logging

MUTABLE_ATTRIBUTES = ["options", "value", "disabled"]

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

logHandler = logging.FileHandler("baseapp.log", mode='w')
formatter = logging.Formatter("%(levelname)s - %(funcName)s() : %(message)s")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)


class MiniAppPlaceholderModel:
    def __init__(self):
        pass

class MiniAppPlaceholderView(BaseView):
    
    def __init__(self, screen, root_menu: Menu, model):
        """Set up the view.

        Explanation goes here...

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

        builder = Builder("Planned for future release")
        builder.addLayout([13, 7, 10, 10, 10, 50], True)

        super(MiniAppPlaceholderView, self).__init__(screen, root_menu, builder)
        self.builder = builder
        self.data_model: MiniAppPlaceholderModel = self.data_model