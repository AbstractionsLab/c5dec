from asciimatics.widgets import Button, Layout, CheckBox, MultiColumnListBox,\
    RadioButtons, Divider, Text, TextBox, DropdownList, Widget, ListBox, Label, DatePicker
from asciimatics.parsers import AsciimaticsParser
from i18n import t as translate
import pyperclip as pc


class Builder:
    """The Builder is used to build a frame layout on the template.
    
    The builder can be passed to the template to set up new frame 
    layouts on the same template more efficiently. The footer can be
    spared and the builder provides several, more efficient ways to add
    widgets.
    """
    def __init__(self, title):
        """Set up the builder with the frame's title.
        
        :param title: the title for the menu
        :type title: str
        """
        self.title = title
        self.widgets = []

    def addLayout(self, list, fill_frame=False):
        """Add a layout.
        
        :param list: list of columns and relational widths, eg. [1,1,1]
        :type list: list
        :param fill_frame if the layout fills out the rest of the 
            frame, defaults to False
        :type fill_frame: bool
        """
        widget = Layout(list, fill_frame=fill_frame)
        self.widgets.append(widget)
        return widget

    def addWidget(self, widget, position=0, span=1):
        """Add a widget to a optionally specified column.
        
        :param widget: the widget that should be added to the layout
        :type widget: class `Widget`
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position:, int

        :return: The widget that is added
        :rtype: class `Widget`
        """
        self.widgets.append((widget, position, span))
        return widget
    
    def add_label(self, label, position=0, 
                gap=False, gap_height=1, disabled=False):
        """Add a label with an optional gap.
        
        :param label: the string in front of the input field
        :type label: str 
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param on_change: function that is called when the input 
            changes, defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int
        :param validator: a statement to check if the value of the text
            corresponds the wanted input restriction, defaults to None
        :type validator: function or regex, optional
        :param gap: whether there should be a gap after the text field,
            defaults to False
        :type gap: bool
        :param gap_height: the height of the gap, defaults to 1
        :type gap_height: int
        :param disabled: whether the text field should be disabled or 
            not, defaults to False
        :type disabled: bool

        :return: The text widget that is added
        :rtype: class `Text`
        """
        widget = Label(
            translate(label), 
            height=1,
            align="^")
        self.addWidget(widget, position=position)
        if gap:
            self.addDivider(height=gap_height)
        if disabled:
            widget.disabled = True
        return widget
    
    def addText(self, label, name, on_change=None, position=0, 
                validator=None, gap=False, gap_height=1, disabled=False):
        """Add a text field with an optional gap.
        
        :param label: the string in front of the input field
        :type label: str 
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param on_change: function that is called when the input 
            changes, defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int
        :param validator: a statement to check if the value of the text
            corresponds the wanted input restriction, defaults to None
        :type validator: function or regex, optional
        :param gap: whether there should be a gap after the text field,
            defaults to False
        :type gap: bool
        :param gap_height: the height of the gap, defaults to 1
        :type gap_height: int
        :param disabled: whether the text field should be disabled or 
            not, defaults to False
        :type disabled: bool

        :return: The text widget that is added
        :rtype: class `Text`
        """
        widget = Text(
            translate(label), 
            name, 
            on_change=on_change, 
            validator=validator)
        self.addWidget(widget, position=position)
        if gap:
            self.addDivider(height=gap_height)
        if disabled:
            widget.disabled = True
        return widget
    
    def add_textbox(self, label, name, height=5, on_change=None, position=0, 
                gap=False, gap_height=1, readonly=False, disabled=False):
        """Add a text box with an optional gap.
        
        :param label: the string in front of the input field
        :type label: str 
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param on_change: function that is called when the input 
            changes, defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int
        :param validator: a statement to check if the value of the text
            corresponds the wanted input restriction, defaults to None
        :type validator: function or regex, optional
        :param gap: whether there should be a gap after the text field,
            defaults to False
        :type gap: bool
        :param gap_height: the height of the gap, defaults to 1
        :type gap_height: int
        :param disabled: whether the text field should be disabled or 
            not, defaults to False
        :type disabled: bool

        :return: The textbox widget that is added
        :rtype: class `Text`
        """
        if height == "max":
            height=Widget.FILL_FRAME
        widget = TextBox(height, 
            translate(label), 
            name, 
            as_string=True,
            line_wrap=True,
            on_change=on_change,
            readonly=readonly
            )
        widget.auto_scroll = True
        self.addWidget(widget, position=position)
        if gap:
            self.addDivider(height=gap_height)
        if disabled:
            widget.disabled = True
        return widget

    def addPath(self, label="filepath", name="filepath", position=0):
        """Add a text field for a filepath and a divider.
        
        :param label: the string in front of the input field,
            defaults to filepath
        :type label: str
        :param name: the name of the widget, useful for data[name],
            defaults to filepath
        :type name: str
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int

        :return: The text widget that is added as path input field
        :rtype: class `Text`
        """
        path_widget = Text(translate(label), name)
        self.addWidget(path_widget, position=position)
        self.addDivider()
        return path_widget

    def addButton(self, text, on_click, position=0, gap=False, gap_height=1, name=None):
        """Add a button.
        
        :param text: The text for the button
        :type text: str
        :param on_click: function that is called when the button is 
            pressed
        :type on_click: function
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int

        :return: The button that is added.
        :rtype: class `Button`
        """
        button = Button(text=translate(text), on_click=on_click, name=name)
        self.addWidget(button, position=position)
        if gap:
            self.addDivider(height=gap_height)
        return button

    def addDivider(self, draw_line=False, height=1, position=0):
        """Add a divider.
        
        :param draw_line: if the divider is invisible or contains a 
            line, defaults to False
        :type draw_line: bool
        :param height: the height of the divider in rows,
            defaults to 0
        :type height: int
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int
        """
        if height == "max":
            height=Widget.FILL_FRAME
        divider = Divider(draw_line=draw_line, height=height)
        self.addWidget(divider, position=position)

    def addCopyButton(self, text_field, position=0):
        """Add a button to copy a widget's content to the clipboard.
        
        :param text_field: the text field whose content will be copied 
            by the button
        :type text_field: class `Text`
        :param position: which column the widger should be assigned to,
            defaults to 0
        :type position: int, optional
        """
        def copyFieldToClipboard():
            self.copyToClipboard(text_field)
        button = Button(translate("copy to clipboard"), copyFieldToClipboard)
        self.addWidget(button, position)

    def copyToClipboard(self, text):
        """Copy the content of a text field to the clipboard.
        
        :param text: the widget whose content should be copied
        :type text: class `Text`
        """
        if text.value:
            string = str(text.value)
            pc.copy(string)
        else:
            pass

    def addChoose(self, name, options, on_change=None, position=0, 
                  gap=False, gap_height=1):
        """Add radiobuttons to choose between options.
        
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param options: a list of options to choose from
        :type options: list
        :param on_change: function that is called when the input 
            changes, defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int
        :param gap: whether there should be a gap after the text field,
            defaults to False
        :type gap: bool
        :param gap_height: the height of the gap, defaults to 1
        :type gap_height: int

        :return: The radiobuttons that are added.
        :rtype: class `RadioButtons`
        """
        options = [translate(i) for i in options]
        options = self.zipOfList(options)
        radiobuttons = RadioButtons(
            options, 
            name=name, 
            on_change=on_change
        )
        self.addWidget(radiobuttons, position=position)
        if gap:
            self.addDivider(height=gap_height)
        return radiobuttons

    def addResult(self, label="Result", name="result", copyButton=False):
        """Add a result field with a 'copy to clipboard' button.
        
        :param label: the string in front of the input field,
            defaults to Result
        :type label: str
        :param name: the name of the widget, useful for data[name],
            defaults to result
        :type name: str
        :param copyButton: if a button to copy the content should be 
            added, defaults to False
        :type copyButton: bool

        :return: The text widget for the result.
        :rtype: class `Text`
        """
        result = Text(translate(label), name)
        result.disabled = True
        self.addWidget(result, 0)
        if copyButton:
            self.addCopyButton(result)
        self.addDivider()
        return result 

    def addDropdownList(self, label, name, options=[], on_change=None, 
                        position=0, gap=False, gap_height=1):
        """Add a dropdownlist.
        
        :param label: the string in front of the input field
        :type label: str
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param options: a list of options to choose from,
            defaults to []
        :type options: list
        :param on_change: function that is called when the input 
            changes, defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to
        :type position: int
        :param gap: whether there should be a gap after the 
            dropdownList, defaults to False
        :type gap: bool
        :param gap_height: the height of the gap, defaults to 1
        :type gap_height: int


        :return: The DropdownList that is added.
        :rtype: class `DropdownList`
        """
        if options:
            options = self.zipOfList(options)
        else:
            options = [(translate("no entries found"), 0)]
        ddlist = DropdownList(
            label=translate(label),
            name=name,
            options=options,
            on_change=on_change
        )
        self.addWidget(ddlist, position=position)
        if gap:
            self.addDivider(height=gap_height)
        return ddlist

    def add_date_picker(self, name, label, on_change=None):
        date_picker = DatePicker(
            label=label,
            name=name,
            on_change=on_change,
        )
        self.addWidget(date_picker)
        return date_picker 

    def addListBox(
            self, name, height, options=[], parser=False,
            on_change=None, on_select=None, position=0):
        """Add a listbox.
        
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param height: the height of the ListBox in rows
        :type height: int
        :param options: a list of options to choose from, 
            defaults to []
        :type options: list
        :param parser: if a parser should be added to color text, 
            defaults to False
        :type parser: bool
        :param on_change: function that is called when selection 
            changes, defaults to None
        :type on_change: function, optional
        :param on_select: function called when an entry is selected,
            defaults to None
        :type on_select: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int

        :return: The ListBox that is added.
        :rtype: class `ListBox`
        """
        if height == "max":
            height=Widget.FILL_FRAME
        if parser:
            parser = AsciimaticsParser()
        else:
            parser = None
        listbox = ListBox(
            height=height,
            options=options,
            name=name,
            parser=parser,
            add_scroll_bar=True,
            on_change=on_change,
            on_select=on_select
        )
        self.addWidget(listbox, position=position)
        return listbox

    def addTable(self, height, titles, options, columns=2, position=0, name="table"):
        """Add a table.
        
        :param height: the height of the table in rows
        :type height: int
        :param titles: the title for each column
        :type titles: list
        :param options: a list of list of options to choose from
        :type options: list
        :param columns: number or structure of columns of the table,
            defaults to 2
        :type columns: int, list
        :param name: the name of the widget, useful for data[name],
            defaults to table
        :type name: str

        :return: The table/ MultiColumnListBox that is added.
        :rtype: class `MultiColumnListBox`
        """
        if height == "max":
            height=Widget.FILL_FRAME

        columnsList = []
        if isinstance(columns, list):
            for i in columns:
                i = str(i)
                column = "<" + i + "%"
                columnsList.append(column)
        else:
            for i in range(columns):
                width = str(100 // columns)
                column = "<" + width + "%"
                columnsList.append(column)

        titles = [translate(i) for i in titles]
        # The options structure is [[1.1, 1.2], [2.1, 2.2]].
        options = self.zipOfList(options)
        table = MultiColumnListBox(
            height=height,
            titles=titles,
            columns=columnsList,
            options=options,
            add_scroll_bar=True,
            name=name
        )
        self.addWidget(table, position=position)
        return table

    def addStatusBar(self, span=1, **kwargs):
        """Add a status bar.
        
        :return: The status bar that is added.
        :rtype: class `Text`
        """
        statusBar = Text(
            label=translate("Status bar: "),
            name="Statusbar"
        )
        self.disable(statusBar)
        self.addWidget(statusBar, position=0, span=span, **kwargs)
        return statusBar

    def addTickBox(self, label, name, on_change=None, position=0):
        """Add a tickbox.
        
        :param label: the text of the tickbox (to describe its effect)
        :type label: str
        :param name: the name of the widget, useful for data[name]
        :type name: str
        :param on_change: function called when the state is changed,
            defaults to None
        :type on_change: function, optional
        :param position: which column the widget should be assigned to,
            defaults to 0
        :type position: int

        :return: the added tickbox
        :rtype: class `CheckBox` 
        """
        tickbox = CheckBox(
            text=translate(label),
            name=name, 
            on_change=on_change
            )
        self.addWidget(tickbox, position=position)
        return tickbox

    def disable(self, widget):
        """Disable a widget.
        
        :param widget: the widget that should be disabled
        :type widget: class `Widget`
        """
        widget.disabled = True

    def enable(self, widget):
        """Enable a widget.
        
        :param widget: the widget that should be enabled
        :type widget: class `Widget`
        """
        widget.disabled = False

    def zipOfList(self, options):
        """Create a zip object with the list and a counter.
        
        This structure is often used in asciimatics elements where you
        can choose an element from a list. 
        Structure: [(a,1), (b,2), ...]

        :param options: list of options to choose from
        :type options: list

        :return: List of tuples of options and increasing numbers.
        :rtype: list
        """
        return list(zip(options, range(len(options))))

    def update(self, frame):
        self.widgets = frame._layouts

    def build(self):
        """Pass the widgets to the Frame.
        
        :return: All the widgets that were added
        :rtype: list
        """
        return self.widgets