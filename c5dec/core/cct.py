from abc import ABC, abstractmethod
from lxml import etree as etree_
import doorstop
import json
import os
import sys
import re
import copy
import c5dec.settings as c5settings
import c5dec.common as common
import c5dec.core.transformer as c5transformer
import time
import pandas as pd
import traceback

log = common.logger(__name__)
log.setLevel(common.logging.DEBUG)

logHandler = common.logging.FileHandler(c5settings.CCT_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

UTF8 = "utf-8"
CP437 = "cp437"
ASCII = "ascii"

BOX = {
    "end": {UTF8: "│   ", CP437: "┬   ", ASCII: "|   "},
    "tee": {UTF8: "├── ", CP437: "├── ", ASCII: "+-- "},
    "bend": {UTF8: "└── ", CP437: "└── ", ASCII: "+-- "},
    "pipe": {UTF8: "│   ", CP437: "│   ", ASCII: "|   "},
    "space": {UTF8: "    ", CP437: "    ", ASCII: "    "},
}
ENCODING = UTF8

"""Start: Helper Functions"""


def clean_string(string):
    clean_newline = string.replace("\n", "").strip()
    clean_string = re.sub(r"\s+", " ", clean_newline).strip()
    return clean_string


class Index:
    """
    Singleton class for managing object indexing by ID.
    """
    _instance = None
    _index = {}
    _cc_tree_root = None

    def __new__(cls):
        """
        Create a new instance of Index or return the existing instance if it exists.

        :returns: The Index instance.
        """
        if cls._instance is None:
            cls._instance = super(Index, cls).__new__(cls)
        return cls._instance

    def __str__(cls):
        return cls._index.__str__()

    @classmethod
    def keys(cls):
        return cls._index.keys()

    @classmethod
    def update(cls, key, value):
        """
        Add a key-value pair to the index. Check for uniqueness and raise
        an error if not unique.

        :param key: The ID of the key.
        :type key: str
        :param value: The object associated with the key.
        :type value: BaseClass or list of BaseClass

        :raises ValueError: If a non-unique ID is encountered or if value
        is not an instance of BaseClass or a list of BaseClass instances.
        """
        if isinstance(value, list):
            for item in value:
                if not isinstance(item, BaseClass):
                    raise common.C5decError(f"Value Type is: {type(value)}, but must be BaseClass or a list of BaseClass")

            # Ensure all items in the list are unique
            unique_items = set(value)
            if len(unique_items) != len(value):
                info_msg = f"Duplicate in {value}!"
                raise common.C5decError(info_msg)

        elif not isinstance(value, BaseClass):
            raise common.C5decError(f"Value Type is: {type(value)}. Expected: BaseClass")

        existing_object = cls._index.get(key.lower())  # get the current value of the key in lower case
        if existing_object:
            # raise exception if the key refers to an object other than 'value'
            if existing_object is not value:
                raise common.C5decError(f"ID '{key}' already exists for the "
                                        f"object {id(existing_object)}: "
                                        f"{existing_object.__repr__()}.\n"
                                        "Cannot be assigned to a different "
                                        f"object: {id(value)}: {value.__repr__()}")
        else:
            cls._index[key.lower()] = value

    @classmethod
    def get(cls, key):
        """
        Returns a a key-value pair.
        :param key: The ID of the key.
        :type key: str

        :raises KeyError: If the ID is not found.
        """
        obj_ = cls._index.get(key.lower())
        if not obj_:
            error_msg = f"Invalid Id {key}!"
            raise KeyError(error_msg)
        return obj_
 
    @classmethod
    def yield_obj(cls, obj_type):
        """
        Yield objects of a given type from the index.

        :param obj_type: The type of objects to retrieve.
        :type obj_type: type
        """
        # Iterate over values in the index
        for value in cls._index.values():
            # If value is a list, check individual objects inside the list
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, obj_type):
                        yield item
            # If value is a single object, check its type
            elif isinstance(value, obj_type):
                yield value

    @classmethod
    def clear(cls):
        """
        Clear the index, removing all entries.
        """
        cls._index.clear()

    @classmethod
    def set_cc_tree(cls, cc_tree):
        cls._cc_tree_root = cc_tree

    @classmethod
    def is_tree_loaded(cls):
        """
        Check if the CC XML tree has been loaded
        """
        if cls._cc_tree_root is None:
            return False
        
        return True 


class UniqueIDManager:
    """
    Singleton class for managing unique IDs.
    The IDs are of the form <prefix><separator><num>
    where 
     - separator is a single character
     - num is a positive integer expressed in
       a fixed length notation.
    """
    _instance = None

    def __new__(cls, separator='-', count_width=1):
        if len(separator) != 1:
            raise common.C5decError("Separator must be a single character.")
        if not isinstance(count_width, int) or count_width <= 0:
            raise common.C5decError("Count width must be a positive integer.")
        if cls._instance is None:
            cls._instance = super(UniqueIDManager, cls).__new__(cls)
            cls._id_counters = {}
        cls._instance._count_width = count_width  # length of the numeric part of an id
        cls._instance._separator = separator 
        return cls._instance

    @classmethod
    def next(cls, prefix):
        """
        Get the next unique ID with a given prefix.

        :param prefix: Prefix for the unique ID.
        :type prefix: str

        :returns: The next unique ID.
        :rtype: str
        """
        count = cls._instance._id_counters.get(prefix, 0) + 1
        cls._instance._id_counters[prefix] = count
        count_str = str(count).zfill(cls._instance._count_width)
        sep = cls._instance._separator
        return f"{prefix}{sep}{count_str}"

    @classmethod
    def reset(cls):
        """
        Reset the UniqueIDManager instance.
        """
        cls._instance = None
        cls._id_counters = {}


"""End: Helper Functions"""
             
"""Start: Super classes"""


class BaseClass(ABC):
    """
    BaseClass with common attributes and methods.
    """

    def __init__(self, _id=None, _name=None):
        """
        Initialize a BaseClass instance.

        :param _id: The ID of the element.
        :type _id: str
        :param _name: The name of the element.
        :type _name: str
        """
        self._id = _id
        self._name = _name
        self.parent = None
        self.children = []
        self.text = ""
        self.container = []

    def __str__(self):
        """
        Return a string representation of the BaseClass instance.

        :returns: The string representation.
        :rtype: str
        """
        sout = (self.get_formatted_text() + "\n\n\n"
                + self.get_item_tree(pretty_print=True))
        return sout

    def __repr__(self):
        """
        Return a representation of the BaseClass instance.

        :returns: The representation.
        :rtype: str
        """
        return f"<class: {self.__class__.__name__} id={self._id}>"

    def clone(self):
        """
        Create a deep copy of the BaseClass instance.

        :returns: A deep copy of the instance.
        :rtype: BaseClass
        """
        return copy.deepcopy(self)

    @property
    def attrib(self):
        """
        Get the attributes of the BaseClass instance.

        :returns: The attributes.
        :rtype: dict
        """
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes

    def collector(self, target, mode="attribute"):
        """
        Collect elements that match a target condition.

        :param target: The target condition (attribute or type).
        :type target: str or Type[BaseClass]
        :param mode: The collection mode ('attribute' or 'type').
        :type mode: str

        :returns: A generator yielding matching elements.
        :rtype: generator
        """
        if mode == "attribute":
            if hasattr(self, target):
                yield getattr(self, target)
        elif mode == "type" and isinstance(self, target):
            yield self

        for child_container in ["children", "container"]:
            if hasattr(self, child_container):
                for child in getattr(self, child_container):
                    if hasattr(child, 'collector'):
                        yield from child.collector(target, mode)

    def get_formatted_text(self, level=1.0):
        """
        Get a formatted text representation of the BaseClass instance.

        :param level: The formatting level.
        :type level: float

        :returns: The formatted text.
        :rtype: str
        """
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n\n"
        for element in self.container:
            if hasattr(element, 'get_formatted_text'):
                formatted_text += element.get_formatted_text(level=(level + 1))
            else:
                raise AttributeError(f"Object {element} does not have a 'get_formatted_text' method.")
        return formatted_text

    def is_empty(self):
        """
        Check if the BaseClass instance is empty.

        :returns: True if the instance is empty, False otherwise.
        :rtype: bool
        """
        return not any([self.text, self.children, self.container])

    def has_valid_id(self):
        """
        Check if the ID is valid.

        :raises ValueError: If the ID is missing or not of type string.
        :returns: True if the ID is valid.
        :rtype: bool
        """
        if not self._id or not isinstance(self._id, str):
            info_msg = f"<{self.__repr__()} at {id(self)}> ID is missing or is not of type string."
            raise common.C5decError(info_msg)
        return True

    def has_valid_name(self):
        """
        Check if the name is valid.

        :raises ValueError: If the name is missing or not of type string.
        :returns: True if the name is valid.
        :rtype: bool
        """
        if not self._name or not isinstance(self._name, str):
            info_msg = f"<{self.__repr__()} at {id(self)}> Name is missing or is not of type string."
            raise common.C5decError(info_msg)
        return True

    # @abstractmethod
    def is_valid(self):
        """
        Check whether the instance is valid according to the CC DTD.
        Since the CC XMLs themselves are not valid, this method 
        only raises info messages.

        Must be implemented for each subclass.
        """
        pass

    def contains(self, element):
        """
        Check if the BaseClass instance contains a specific element.

        :param element: The element to check for.
        :type element: BaseClass

        :returns: True if the element is contained, False otherwise.
        :rtype: bool
        """
        return element in self.children or element in self.container

    def get_children(self):
        """
        Get the children of the BaseClass instance.

        :returns: The children.
        :rtype: list[BaseClass]
        """
        return self.children

    def get_child_by_id(self, child_id):
        """
        Get a child element by ID.

        :param child_id: The ID of the child.
        :type child_id: str

        :returns: The child element or None if not found.
        :rtype: BaseClass or None
        """
        for child in self.children:
            if child._id == child_id.lower():
                return child
        return None

    def get_descendants(self, visited=None):
        """
        Get the descendants of the BaseClass instance.

        :param visited: A set of visited elements (used for cycle detection).
        :type visited: set[BaseClass]

        :returns: The descendants.
        :rtype: list[BaseClass]
        """
        if visited is None:
            visited = set()

        descendants = []
        for child in self.children:
            if child in visited:
                raise common.C5decError(f"Circular reference detected at {child._id} for {self._id}.")
            visited.add(child)
            descendants.append(child)
            descendants.extend(child.get_descendants(visited))
        return descendants

    def get_parent(self):
        """
        Get the parent of the BaseClass instance.

        :returns: The parent element.
        :rtype: BaseClass
        """
        return self.parent

    def get_ancestors(self):
        """
        Get the ancestors of the BaseClass instance.

        :returns: The ancestors.
        :rtype: list[BaseClass]
        """
        ancestors = []
        visited = set()
        current = self.parent

        while current:
            if current in visited:
                info_msg = f"Circular reference detected at {current._id} for {self._id}."
                raise common.C5decError(info_msg)
            visited.add(current)
            ancestors.append(current)
            current = current.parent

        return ancestors

    def get_siblings(self):
        """
        Get the siblings of the BaseClass instance.

        :returns: The siblings.
        :rtype: list[BaseClass]
        """
        if not self.parent:
            return []
        return [child for child in self.parent.children if child != self]

    def _pretty_print_tree(self, tree, prefix="", is_last=True):
        """
        Helper function to pretty-print a tree structure.

        :param tree: The tree structure.
        :type tree: dict
        :param prefix: The prefix for indentation.
        :type prefix: str
        :param is_last: True if the element is the last in its branch.
        :type is_last: bool

        :returns: The lines of the pretty-printed tree.
        :rtype: list[str]
        """
        lines = []

        connector = BOX["bend"][ENCODING] if is_last else BOX["tee"][ENCODING]
        id_name = f"{prefix}{connector}{tree['id'] or ''} {tree['name'] or ''}"
        lines.append(id_name)

        prefix += BOX["space"][ENCODING] if is_last else BOX["pipe"][ENCODING]

        children = tree.get("children", [])
        child_count = len(children)
        for index, child in enumerate(children):
            is_last_child = (index == child_count - 1)
            lines.extend(self._pretty_print_tree(child, prefix, is_last_child))

        return lines

    def get_item_tree(self, pretty_print=False):
        """
        Get the item tree structure of the BaseClass instance.

        :param pretty_print: Whether to pretty-print the tree.
        :type pretty_print: bool

        :returns: The item tree structure.
        :rtype: dict or str
        """
        tree = {"id": self._id, "name": self._name}
        if self.children:
            tree["children"] = [child.get_item_tree(pretty_print=False)
                                 for child in self.children]

        if pretty_print:
            return "\n".join(self._pretty_print_tree(tree))
        return tree


class BaseBuilder(ABC):
    """
    Base class for building instances of BaseClass or its subclasses from XML nodes.
    """

    def __init__(self, instance):
        """
        Initialize a BaseBuilder instance.

        :param instance: The instance to build.
        :type instance: BaseClass
        """
        self.instance = instance

    def _build_attributes(self, node, parent_obj):
        """
        Build attributes (ID and name) of the instance from an XML node.

        :param node: The XML node.
        :type node: Element
        :param parent_obj: The parent object.
        :type parent_obj: BaseClass
        """
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self.instance._id = node.get(attribute)
            if attribute == "name":
                self.instance._name = node.get(attribute)

    @abstractmethod
    def _build_children(self, child):
        """
        Build children of the instance from an XML node.

        :param child: The child XML node.
        :type child: Element
        """
        pass

    def build(self, node, parent_obj=None):
        """
        Build the instance from an XML node and update the index.

        :param node: The XML node.
        :type node: Element
        :param parent_obj: The parent object.
        :type parent_obj: BaseClass or None

        :returns: The built instance.
        :rtype: BaseClass
        """
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        Index.update(self.instance._id, self.instance)
        self.instance.is_valid()
        return self.instance


class BaseExporter(ABC):
    """
    To be added in future iterations.
    """
    def __init__(self, instance):
        self.instance = instance

    def _construct_data(self):
        _id = self.instance._id
        if self.instance._name:
            _name = self.instance._name
            header = _id + " " + _name
        else:
            _name = ""
            header = _id

        if self.instance.parent:
            links = self.instance.parent.id.lower()
        else:
            links = []

        text = self.instance.get_formatted.text()

        keys = ["id", "name", "header", "text", "links"]
        values = [_id, _name, header, text, links]

        data = dict(zip(keys, values))
        return data

    @abstractmethod
    def _export_children(self, child, doc, level, index,
                         itemformat="markdown", seperator="-", silence=True):
        pass

    def doorstop_export(self, tree, level, index,
                        itemformat="markdown", seperator="-", silence=True):
        """
        TBA.
        """
        pass


"""End: Super classes"""


"""Start: Common Text Elements"""
# @TST-010

class Text(BaseClass):

    def __init__(self, value=None):
        self.text = value

    def get_formatted_text(self, level=1.0):
        _ = level #just for the linter
        formatted_text = clean_string(self.text)
        return formatted_text

    def set_text(self, value):
        self.text = value

    def empty_text(self):
        self.text = None

    def is_valid(self):
        if self.is_empty():
            raise common.C5decError("'Text' is empty.")
        return True


class Italic(Text):

    def __init__(self, value=None):
        self.text = str(value)

    def get_formatted_text(self, level=1.0):
        formatted_text = " *" + clean_string(self.text) + "* "
        return formatted_text


class Bold(Text):

    def __init__(self, value=None):
        self.text = str(value)

    def get_formatted_text(self, level=1.0):
        formatted_text = " **" + clean_string(self.text) + "** "
        return formatted_text


class Math(Text):
    def __init__(self, value=None):
        self.text = value

    def get_formatted_text(self, level=1.0):
        formatted_text = f" ${self.text}$ "
        return formatted_text


class XRef(BaseClass):

    VALID_SHOW = ["title", "link", "none", "id"]

    def __init__(self, _id=None, tail=None, fake_id=None, show="link"):
        self._id = _id
        self.fakeid = fake_id
        if show not in XRef.VALID_SHOW:
            raise common.C5decError(f"Invalid 'show' attribute {show}. Must be one of {XRef.VALID_SHOW}")
        self.show = show
        self.tail = tail
        self.parent = None
        self.text = ""
        self.container = []

    def __str__(self):
        return self.get_formatted_text()

    def get_formatted_text(self, level=1.0):
        _ = level  # just for the linter
        formatted_text = f" [{self._id}]() "
        return formatted_text

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self._id = node.get(attribute)
            if attribute == "fakeid":
                self.fakeid = node.get(attribute)
            if attribute == "show":
                self.show = node.get(attribute)

    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if self.tail:
            self.tail = node.tail
            self.container.append(Text(node.tail))
        return self


class URL(BaseClass):

    def __init__(self,
                 _id=None,
                 title=None):
        self._id = _id
        self.title = title
        self.parent = None
        self.text = ""

    def __str__(self):
        return self.get_formatted_text()

    @property
    def attrib(self):
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes

    def get_formatted_text(self, level=1.0):
        _ = level  # just for the linter
        formatted_text = f" [{self._id}]({self._id}) "
        return formatted_text

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self._id = node.get(attribute)
            if attribute == "title":
                self.title = node.get(attribute)

    def _build_text(self, node):
        url_text = f"<{node.get('id')}>"
        self.text = url_text

    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        return self


class Item(BaseClass):

    def __init__(self):
        self.parent = None
        self.text = ""
        self.container = []
    
    def __str__(self):
        return self.get_formatted_text()

    def __repr__(self):
        return str(type(self))
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level)
        return formatted_text
            
    def _build_children(self, child):
        node_name = child.tag
        
        if node_name == "para":
            obj_ = Para().build(child, self)
            self.text += obj_.text
            self.container.append(obj_)
        if node_name == "xref":
            obj_ = XRef().build(child, self)
            self.text += obj_.text
            self.container.append(obj_)
            if child.tail:
                self.text += child.tail
                self.container.append(Text(child.tail))
        if node_name == "url":
            obj_ = URL().build(child, self)
            self.text += obj_.text
            self.container.append(obj_)
        if node_name == "list":
            obj_ = List().build(child, self)
            self.text += obj_.text
            self.container.append(obj_)
        if node_name == "bold":
            bold = Bold(child.text)
            self.container.append(bold)
            if child.tail:
                self.text += child.tail
                self.container.append(Text(child.tail))
        if node_name == "italic":
            italic = Italic(child.text)
            self.container.append(italic)
            if child.tail:
                self.text += child.tail
                self.container.append(Text(child.tail))
        if node_name == "sub":
            base = self.text[-1]
            math = f"{base}_{{ {str(child.text)} }}"
            self.text = self.text[:-1]
            if isinstance(self.container[-1], Text):
                base_text = self.container[-1].text
                self.container[-1] = Text(base_text[:-1])
            self.container.append(Math(math))
            if child.tail:
                self.text += child.tail
                self.container.append(Text(child.tail))
        
    def build(self, node, parent_obj=None):
        self.parent = parent_obj
        if node.text:
            self.text += node.text
            self.container.append(Text(node.text))
        for child in node:
            self._build_children(child)     
        return self


class List(BaseClass):

    VALID_TYPE = ["itemized", "enumerated"]

    def __init__(self, ltype="enumerated"):
        self.type = ltype
        self.item = []
        self.parent = None
        self.text = ""
        self.container = []  

    def __str__(self):
        return self.get_formatted_text()
    
    def get_formatted_text(self, level=1.0):
        formatted_text = "\n"
        if self.type == self.VALID_TYPE[0]:
            marker = "- "
            for element in self.item:
                formatted_text += marker + element.get_formatted_text(level=level) + "\n"
                
        if self.type == self.VALID_TYPE[1]:
            enum = 1
            for element in self.item:
                marker = f"{enum}. "
                formatted_text += marker + element.get_formatted_text(level=level) + "\n"
                enum += 1   
        return formatted_text
            
    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "type":
                self.type = node.get(attribute)
                
    def _build_children(self, child):
        node_name = child.tag
        if node_name == "item":
            obj_ = Item().build(child, self)
            self.text += obj_.text
            self.item.append(obj_)
            self.container.append(obj_)
        
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        return self


class Example(BaseClass):

    def __init__(self):
        self.exampleterm = None
        self.exampledef = None

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self._id = node.get(attribute)
    
    def _build_children(self, child):
        if child.tag in ["exampleterm", "exampledef"]:
            obj_ = Para().build(child, self)
            setattr(self, child.tag, obj_)
            self.container.append(obj_)
                
    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        return self


class TEntry(BaseClass):

    def __init__(self):
        self.rowspan = 1
        self.columnspan = 1
        self.width = 100
        self.style = None
        self.align = "left"
        self.container = []

    def get_formatted_text(self):
        column_text = ""
        for element in self.container:
            column_text += element.get_formatted_text()
        formatted_text = " | " + column_text + (" |    | " * (self.columnspan - 1))
        return formatted_text

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "rowspan":
                self.rowspan = int(node.get(attribute))
            if attribute == "columnspan":
                self.columnspan = int(node.get(attribute))
            if attribute == "width":
                self.width = node.get(attribute)
            if attribute == "style":
                self.style = node.get(attribute)
            if attribute == "align":
                self.align = node.get(attribute)
            
    def _build_children(self, child):
        if child.tag == "xref":
            xref = XRef().build(child, self)
            self.container.append(xref)
            if child.tail:
                self.container.append(Text(child.tail))
        if child.tag == "bold":
            bold = Bold(child.text)
            self.container.append(bold)
            if child.tail:
                self.container.append(Text(child.tail))
        if child.tag == "italic":
            italic = Italic(child.text)
            self.container.append(italic)
            if child.tail:
                self.container.append(Text(child.tail))
        if child.tag == "footnote":
            footnote = Para().build(child, self)
            self.container.append(footnote)

    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(node, parent_obj)
        if node.text:
            self.container.append(Text(node.text))
        for child in node:
            self._build_children(child)
        return self

class TRow(BaseClass):

    def __init__(self):
        self.entry = []
    
    def get_formatted_text(self, columns=1):
        row_text = ""
        rowspan = 0
        columnspan = 0
        for entry in self.entry:
            if entry.rowspan > rowspan:
                rowspan = entry.rowspan
            row_text += entry.get_formatted_text()
            columnspan += entry.columnspan
        if columnspan < columns:
            diff = columns - columnspan
            formatted_text =  (" |    | " * diff) + row_text
        else:
            formatted_text = row_text
        if rowspan > 1:
            formatted_text += " |    | " * columns
        return formatted_text 

    def _build_attributes(self, parent_obj=None):
        self.parent = parent_obj
    
    def _build_children(self, child):
        if child.tag == "entry":
            entry = TEntry().build(child)
            self.entry.append(entry)

    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(parent_obj)
        for child in node:
            self._build_children(child)
        return self

class TGroup(BaseClass):

    def __init__(self):
        self.cols = 1
        self.thead = None
        self.tfoot = None
        self.tbody = None

    def get_formatted_text(self):
        #auto fill rows to column specification.
        formatted_text = ""
        if self.thead:
            for row in self.thead:
                formatted_text += row.get_formatted_text(columns=self.cols) + " |\n"
            hdelimiter = ("|----" * self.cols) + "|\n"
            formatted_text += hdelimiter
        for row in self.tbody:
            formatted_text += row.get_formatted_text(columns=self.cols) + " |\n"
        if self.tfoot:
            for row in self.tfoot:
                formatted_text += row.get_formatted_text(columns=self.cols) + " |\n"
        return formatted_text

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "cols":
                self.cols = int(node.get(attribute))
    
    def _build_children(self, child):
        
        if child.tag == "thead":
            thead = []
            for row in child:
                row = TRow().build(row, self)
                thead.append(row)
            self.thead = thead
        if child.tag == "tfoot":
            tfoot = []
            for row in child:
                row = TRow().build(row, self)
                tfoot.append(row)
            self.tfoot = tfoot
        if child.tag == "tbody":
            tbody = []
            for row in child:
                row = TRow().build(row, self)
                tbody.append(row)
            self.tbody = tbody

    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        return self

class Table(BaseClass):

    def __init__(self):
        self.title = None
        self.tgroup = []
        self.container = []

    def __str__(self):
        return self.get_formatted_text()

    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        for element in self.container:
            formatted_text += element.get_formatted_text()
        if self.title:
            formatted_text += f"\n Table: {self.title.text}\n"
        return formatted_text

    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self._id = node.get(attribute)
    
    def _build_children(self, child):
        if child.tag == "tgroup":
            tgroup = TGroup().build(child, self)
            self.tgroup.append(tgroup)
            self.container.append(tgroup)
        if child.tag == "title":
            # don't append to container title == caption
            self.title = Text(str(child.text))

    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        return self


class Para(BaseClass):

    VALID_TYPES = ("normal", "isonote", "ccmbnote")

    def __init__(self,
                 title = None,
                 ptype = "normal",
                 _id = None,
                 level = 1,
                 patch= None):
        self.title = title
        self._id = _id
        self.parent = None
        self.level = str(level)
        self.patch = patch
        if ptype not in Para.VALID_TYPES:
            raise common.C5decError(f"Invalid 'para' type {ptype}. "
                              f"Must be one of {Para.VALID_TYPES}")
        self.type = ptype
        self.text = ""
        self.container = []
      
    def __str__(self):
        return self.get_formatted_text()
    
    @property
    def attrib(self):
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        if self.title:
            formatted_text += f"\n{header_level} {self.title}\n"
            level += 1
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level)
        return formatted_text
    
    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "title":
                self.title = node.get(attribute)
            if attribute == "id":
                self._id = node.get(attribute)
            if attribute == "type":
                self.type = node.get(attribute)
            
    def _build_children(self, node):
        para_text = ""
        if node.text:
            para_text += node.text
            self.container.append(Text(node.text))
        for child in node:
            if child.tag == "xref":
                xref = XRef().build(child, self)
                para_text += xref.text
                self.container.append(xref)
                if child.tail:
                    para_text += child.tail
                    self.container.append(Text(child.tail))
            if child.tag == "url":
                url = URL().build(child, self)
                para_text += url.text
                self.container.append(url)
            if child.tag == "list":
                plist = List().build(child, self)
                para_text += plist.text
                self.container.append(plist)
            if child.tag == "bold":
                bold = Bold(child.text)
                self.container.append(bold)
                if child.tail:
                    self.text += child.tail
                    self.container.append(Text(child.tail))
            if child.tag == "italic":
                italic = Italic(child.text)
                self.container.append(italic)
                if child.tail:
                    para_text += child.tail
                    self.container.append(Text(child.tail))
            if child.tag == "sub":
                base = para_text[-1]
                math = f"{base}_{{{str(child.text)}}}"
                para_text = para_text[:-1]
                if isinstance(self.container[-1], Text):
                    base_text = self.container[-1].text
                    self.container[-1] = Text(base_text[:-1])
                self.container.append(Math(math))
                if child.tail:
                    para_text += child.tail
                    self.container.append(Text(child.tail))

        para_text = para_text.replace("\n", "").strip()
        clean_text = re.sub(r"\s+", " ", para_text).strip()
        self.text = clean_text
        
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        self._build_children(node)
        return self
        

class ParaSequence(BaseClass):

    def __init__(self):
        self.subclause = []
        self.para = []
        self.table = []
        self.example = []
        self.figure = []
        self.acronym = []
        self.biblioentry = []
        self.glossentry = []
        self.parent = None
        self.original_tag = None
        self.text = ""
        self.container = []
    
    def __str__(self):
        return self.get_formatted_text()
    
    @property
    def attrib(self):
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        if self.original_tag:
            formatted_text += "\n\n" + header_level + " " 
            formatted_text +=  self.original_tag.upper() + "\n\n"
            level += 1
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level) + "\n"
        return formatted_text
    
    def _build_attributes(self, node, parent_obj=None):
        """
        Intended to be overridden by subclasses to handle node attributes. 
        Does nothing in the base class.
        """
        pass
    
    def _build_children(self, child):
        if child.tag == "subclause":
            subclause = SubClause().build(child, self)
            self.text += "\n#" + subclause.title + "\n\n" + subclause.text + "\n"
            self.subclause.append(subclause)
            self.container.append(subclause)
        if child.tag == "para":
            para = Para().build(child, self)
            self.text += para.text + "\n"
            self.para.append(para)
            self.container.append(para)
        if child.tag == "example":
            example = Example().build(child, self)
            self.text += example.text + "\n"
            self.example.append(example)
            self.container.append(example)
        if child.tag == "table":
            table = Table().build(child, self)
            self.table.append(table)
            self.container.append(table)
        
    def build(self, node, parent_obj=None):
        self.original_tag = node.tag
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        return self

    
class SubClause(ParaSequence):


    def __init__(self, 
                 title = None, 
                 _id = None,
                 patch= None):
        super().__init__()
        self.title = title
        self._id = _id
        self.patch = patch
        
    def __str__(self):
        return self.get_formatted_text() 
    
    @property
    def attrib(self):
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        if self.title:
            formatted_text += f"\n\n{header_level} {self.title}\n\n"
            level += 1
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level) + "\n"
        return formatted_text
    
    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "title":
                self.title = node.get(attribute)
            if attribute == "id":
                self._id = node.get(attribute)
    
    
class Clause(ParaSequence):

    VALID_TYPES = ["normal", "annex"]
    VALID_CATEGORY = ["normative", "informative"]
    
    def __init__(self,
                 title = None,
                 _id = None,
                 ctype = "normal",
                 category = "normative",
                 patch= None):
        super().__init__()
        self.title = title
        self._id = _id
        if ctype not in Clause.VALID_TYPES:
            raise common.C5decError(f"Invalid 'Clause' type {ctype}.\
                              Must be one of {Clause.VALID_TYPES}")
        self.type = ctype
        if category not in Clause.VALID_CATEGORY:
            raise common.C5decError(f"Invalid 'Clause' type {category}.\
                              Must be one of {Clause.VALID_CATEGORY}")
        self.category = category
        self.patch = patch
    
    def __str__(self):
        return self.get_formatted_text()
    
    @property
    def attrib(self):
        attributes = {}
        for key, value in self.__dict__.items():
            if not callable(value) and not key.startswith("__"):
                attributes[key] = value
        return attributes
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#"
        if self.title:
            formatted_text += f"\n{header_level} {self.title}\n"
            level += 1 
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level)
        return formatted_text
        
    def _build_attributes(self, node, parent_obj=None):
        self.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "title":
                self.title = node.get(attribute)
            if attribute == "id":
                self._id = node.get(attribute)
            if attribute == "type":
                self.type = node.get(attribute)
            if attribute == "category":
                self.category = node.get(attribute)

"""End: Common Text Elements"""  


"""Start: Functional Class Elements"""


class Operation(BaseClass):
    """
    Represents an Element Operation in the context of CC. It is not differentiated between
    functional and assurance operations. The distinction is handled via the object's parent
    object. 

    :param _id: The ID of the operation.
    :type _id: str
    :param op_type: The type of the operation ("selection" or "assignment").
    :type op_type: str
    :param exclusive: Whether the operation is exclusive ("YES" or "NO").
    :type exclusive: str
    """

    VALID_TYPES = ["selection", "assignment"]

    def __init__(self, _id=None, op_type=None, exclusive="NO"):
        super().__init__(_id=_id, _name=None)
        self.type = op_type
        self.exclusive = exclusive
        self.note = None
        self.item = []
    
    def get_formatted_text(self, level=1.0):
        formatted_text = f" [_{self.type}_: "
        for element in self.container:
            # ParaSequences are Operation Notes. These are handled in FElement and AElement.
            if not isinstance(element, ParaSequence):
                formatted_text += element.get_formatted_text(level=level) + ", "
        formatted_text = formatted_text[:-2]
        formatted_text += "] "
        return formatted_text
    
    def is_valid(self):
        if self.type not in self.VALID_TYPES:
            # not explicit requiremnt in CC DTD, but given the implementation it must be checked
            # if operations are of valid type.
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> invalid.\
                  \nOperation must be one of type {self.VALID_TYPES}. Is {self.type}"
            # raise common.C5decError(info_msg)
            log.error(info_msg)
        if not self.item and not hasattr(self.parent, "type"):
            # Only Assurance Elements (AElement) are allowed to not contain operation items (FEItem)
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> invalid.\
                    \nOperation must contain {self.type}item/s."
            log.error(info_msg)
            # raise common.C5decError(info_msg)
        return True


class OperationBuilder(BaseBuilder):
    """
    Builder class for creating Operation instances.

    :param instance: An instance of Operation to build upon.
    :type instance: Operation
    """

    def __init__(self, instance):
        """
        Initialize an OperationBuilder instance.

        :param instance: An instance of Operation to build upon.
        :type instance: Operation
        :raises ValueError: If the provided instance is not an Operation object.
        """
        if not isinstance(instance, Operation):
            info_msg = f"Object must be {Operation}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self.instance._id = node.get(attribute)
            if attribute == "exclusive":
                self.instance.exclusive = node.get(attribute)

    def _build_children(self, child):
        node_name = child.tag
        if node_name in ["fe-assignmentitem", "fe-selectionitem"]:
            item = FEItem()
            obj_ = FEItemBuilder(item).build(child, self.instance)
            self.instance.item.append(obj_)
            self.instance.container.append(obj_)   
        if node_name in ["fe-assignmentnotes", "fe-selectionnotes"]:
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.note = obj_
            self.instance.container.append(obj_) 
        if node_name == "fe-list":
            flist = FEList()
            obj_ = FEListBuilder(flist).build(child, self.instance)
            self.instance.container.append(obj_)
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        self.instance.is_valid()
        return self.instance
    

class OperationBuilder2022(BaseBuilder):
    """
    Builder class for creating Operation instances.

    :param instance: An instance of Operation to build upon.
    :type instance: Operation
    """

    def __init__(self, instance):
        """
        Initialize an OperationBuilder instance.

        :param instance: An instance of Operation to build upon.
        :type instance: Operation
        :raises ValueError: If the provided instance is not an Operation object.
        """
        if not isinstance(instance, Operation):
            info_msg = f"Object must be {Operation}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self.instance._id = node.get(attribute)
            if attribute == "exclusive":
                self.instance.exclusive = node.get(attribute)

    def _build_children(self, child):
        node_name = child.tag
        if node_name in ["assignmentitem", "selectionitem"]:
            item = FEItem()
            obj_ = FEItemBuilder2022(item).build(child, self.instance)
            self.instance.item.append(obj_)
            self.instance.container.append(obj_)   
        if node_name in ["assignmentnotes", "selectionnotes"]:
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.note = obj_
            self.instance.container.append(obj_) 
        if node_name == "list":
            flist = FEList()
            obj_ = FEListBuilder2022(flist).build(child, self.instance)
            self.instance.container.append(obj_)
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        self.instance.is_valid()
        return self.instance

class FEItem(BaseClass):
    """
    In the context of CC this class represents either a fe-assignmentitem, fe-selectionitem,
    or a fe-item. The distinction is made via the parent object. 

    Inherits from `BaseClass` and adds attributes:
        - `list` (list): A list of FEList objects
        - `operation` (list): A list of Operation objects.
    """
    def __init__(self):
        super().__init__(_id=None, _name=None)
        self.list = []
        self.operation = []

    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        for element in self.container:
            formatted_text += element.get_formatted_text(level=level)
        return formatted_text

    def is_valid(self):
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> cannot be empty."
            raise common.C5decError(info_msg)
        return True


class FEItemBuilder(BaseBuilder):
    """
    Builder class for creating FEItem instances.

    :param instance: An instance of FEItem to build upon.
    :type instance: Operation
    """

    def __init__(self, instance):
        """
        Initialize an FEItemBuilder instance.

        :param instance: An instance of FEItem to build upon.
        :type instance: FEItem
        :raises ValueError: If the provided instance is not an FEItem object.
        """
        if not isinstance(instance, FEItem):
            info_msg = f"Object must be {FEItem}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_children(self, child):
        
        node_name = child.tag
        if child.text:
            self.instance.container.append(Text(child.text))
        if child.tail:
            self.instance.container.append(Text(child.tail))
        if node_name == "fe-list":
            flist = FEList()
            obj_ = FEListBuilder(flist).build(child, self.instance)
            self.instance.list.append(obj_)
            self.instance.container.append(obj_)
        else:
            op_type = re.sub(r"fe-(.*?)", r"\1", node_name)
            operation = Operation(op_type=op_type)
            obj_ = OperationBuilder(operation).build(child, self.instance)
            self.instance.operation.append(obj_)
            self.instance.container.append(obj_)  
        
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if node.text:
            self.instance.container.append(Text(node.text))
        if len(node):
            for child in node:
                self._build_children(child)
        self.instance.is_valid()        
        return self.instance
    

class FEItemBuilder2022(BaseBuilder):
    """
    Builder class for creating FEItem instances.

    :param instance: An instance of FEItem to build upon.
    :type instance: Operation
    """

    def __init__(self, instance):
        """
        Initialize an FEItemBuilder instance.

        :param instance: An instance of FEItem to build upon.
        :type instance: FEItem
        :raises ValueError: If the provided instance is not an FEItem object.
        """
        if not isinstance(instance, FEItem):
            info_msg = f"Object must be {FEItem}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_children(self, child):
        
        node_name = child.tag
        if child.text:
            self.instance.container.append(Text(child.text))
        if child.tail:
            self.instance.container.append(Text(child.tail))
        if node_name == "list":
            flist = FEList()
            obj_ = FEListBuilder2022(flist).build(child, self.instance)
            self.instance.list.append(obj_)
            self.instance.container.append(obj_)
        else:
            op_type = re.sub(r"(.*?)", r"\1", node_name)
            operation = Operation(op_type=op_type)
            obj_ = OperationBuilder2022(operation).build(child, self.instance)
            self.instance.operation.append(obj_)
            self.instance.container.append(obj_)  
        
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if node.text:
            self.instance.container.append(Text(node.text))
        if len(node):
            for child in node:
                self._build_children(child)
        self.instance.is_valid()        
        return self.instance

class FEList(BaseClass):
    """
    Class representing a Functional Element (FE) List in the context of CC.

    Inherits from `BaseClass` and adds the following attribute:
        - `item` (list): A list of FEItem.
    """

    def __init__(self):
        super().__init__(_id=None, _name=None)
        self.item = []
    
    def get_formatted_text(self, level=1.0):
        formatted_text = "\n"
        marker = "- "
        for element in self.container:
            formatted_text += marker + element.get_formatted_text(level=level) + "\n"
        return formatted_text

    def is_valid(self):
        if not self.item:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain items."
            raise common.C5decError(info_msg)
        return True


class FEListBuilder(BaseBuilder):
    """
    Builder class for creating FEList instances.

    :param instance: An instance of FEList to build upon.
    :type instance: FEList
    """

    def __init__(self, instance):
        """
        Initialize an FEListBuilder instance.

        :param instance: An instance of FEList to build upon.
        :type instance: FEList
        :raises ValueError: If the provided instance is not an FEList object.
        """
        if not isinstance(instance, FEList):
            info_msg = f"Object must be {FEList}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        
    def _build_children(self, child):
        node_name = child.tag
        if node_name == "fe-item":
            item = FEItem()
            obj_ = FEItemBuilder(item).build(child, self.instance)
            self.instance.container.append(obj_)
            self.instance.item.append(obj_)
            
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        self.instance.is_valid()
        return self.instance

class FEListBuilder2022(BaseBuilder):
    """
    Builder class for creating FEList instances.

    :param instance: An instance of FEList to build upon.
    :type instance: FEList
    """

    def __init__(self, instance):
        """
        Initialize an FEListBuilder instance.

        :param instance: An instance of FEList to build upon.
        :type instance: FEList
        :raises ValueError: If the provided instance is not an FEList object.
        """
        if not isinstance(instance, FEList):
            info_msg = f"Object must be {FEList}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        
    def _build_children(self, child):
        node_name = child.tag
        if node_name == "item":
            item = FEItem()
            obj_ = FEItemBuilder2022(item).build(child, self.instance)
            self.instance.container.append(obj_)
            self.instance.item.append(obj_)
            
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        for child in node:
            self._build_children(child)
        self.instance.is_valid()
        return self.instance

class FElement(BaseClass):
    """
    This class represents a functional element in the context of CC.

    :param _id: The ID of the FElement.
    :type _id: str
    :param _name: The name of the FElement.
    :type _name: str

    Inherits from `BaseClass` and adds the following attribute:
        - `list` (list): A list of FEList objects
        - `operation` (list): A list of Operation objects.
        - `requirement` (str): The requirement stated by the FElement. 
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.list = None
        self.operation = []
        self.requirement = ""
        
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n\n"
        for element in self.container:
            formatted_text += element.get_formatted_text(level=(level+1))
        
        formatted_text += "\n\n"
        notes = self.collector("note")
        for note in notes:
            if note is not None:
                formatted_text += note.get_formatted_text(level=(level+1)) + "\n"
        
        return formatted_text
    
    def is_valid(self):
        self.has_valid_id()
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> cannot be empty."
            raise common.C5decError(info_msg)
        return True


class FElementBuilder(BaseBuilder):
    """
    Builder class for creating FElement instances.

    :param instance: An instance of FElement to build upon.
    :type instance: FElement
    """

    def __init__(self, instance):
        """
        Initialize an FElementBuilder instance.

        :param instance: An instance of FElement to build upon.
        :type instance: FElement
        :raises ValueError: If the provided instance is not an FElement object.
        """
        if not isinstance(instance, FElement):
            info_msg = f"Object must be {FElement}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

        
    def _build_requirement(self):
        requirement = ""
        for element in self.instance.container:
            requirement += element.text
        self.instance.requirement = clean_string(requirement)
                
    def _build_children(self, child):
        node_name = child.tag
        if node_name != "fe-list":
            if child.text:
                self.instance.container.append(Text(child.text))
                
            op_type = re.sub(r"fe-(.*?)", r"\1", node_name)
            operation = Operation(op_type=op_type)
            obj_ = OperationBuilder(operation).build(child, self.instance)
            self.instance.operation.append(obj_)
            self.instance.container.append(obj_)
            
            if child.tail:
                self.instance.container.append(Text(child.tail))
        else:
            flist = FEList()
            obj_ = FEListBuilder(flist).build(child, self.instance)
            self.instance.container.append(obj_)
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if node.text:
            self.instance.container.append(Text(node.text))
        for child in node:
            self._build_children(child)
        if node.tail:
            self.instance.container.append(Text(node.tail))
        self._build_requirement()
        Index.update(self.instance._id, self.instance)
        self.instance.is_valid()
        return self.instance

class FElementBuilder2022(BaseBuilder):
    """
    Builder class for creating FElement instances.

    :param instance: An instance of FElement to build upon.
    :type instance: FElement
    """

    def __init__(self, instance):
        """
        Initialize an FElementBuilder instance.

        :param instance: An instance of FElement to build upon.
        :type instance: FElement
        :raises ValueError: If the provided instance is not an FElement object.
        """
        if not isinstance(instance, FElement):
            info_msg = f"Object must be {FElement}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

        
    def _build_requirement(self):
        requirement = ""
        for element in self.instance.container:
            requirement += element.text
        self.instance.requirement = clean_string(requirement)
                
    def _build_children(self, child):
        node_name = child.tag
        if node_name != "list":
            if child.text:
                self.instance.container.append(Text(child.text))
                
            op_type = re.sub(r"(.*?)", r"\1", node_name)
            operation = Operation(op_type=op_type)
            obj_ = OperationBuilder2022(operation).build(child, self.instance)
            self.instance.operation.append(obj_)
            self.instance.container.append(obj_)
            
            if child.tail:
                self.instance.container.append(Text(child.tail))
        else:
            flist = FEList()
            obj_ = FEListBuilder2022(flist).build(child, self.instance)
            self.instance.container.append(obj_)
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if node.text:
            self.instance.container.append(Text(node.text))
        for child in node:
            self._build_children(child)
        if node.tail:
            self.instance.container.append(Text(node.tail))
        self._build_requirement()
        Index.update(self.instance._id, self.instance)
        self.instance.is_valid()
        return self.instance

class FCoAudit(BaseClass):
    """
    Class representing a functional component audit in the context of CC.

    :param level: The level of the Combined Audit ("minimal", "basic", or "detailed").
    :type level: str
    :raises ValueError: If the provided `level` is not one of the valid levels ("minimal", "basic", or "detailed").
    """

    VALID_LEVEL = ["minimal", "basic", "detailed"]

    def __init__(self, level="minimal"):
        super().__init__(_id=None, _name=None)
        self.level = level
        self.isequal = None
        self.text = ""

    def is_valid(self):
        if self.level not in self.VALID_LEVEL:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> Level missing or not valid level. {self.level}"
            raise common.C5decError(info_msg)
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> cannot be empty."
            raise common.C5decError(info_msg)
        return True
            
    def get_formatted_text(self, level=1.0):
        header_level = "#" * int(level)
        formatted_text = f"\n{header_level} Audit: " + self.text + "\n"
        return formatted_text
    

class FCoAuditBuilder(BaseBuilder):
    """
    Builder class for creating FCoAudit instances.

    :param instance: An instance of FCoAudit to build upon.
    :type instance: FCoAudit
    """

    def __init__(self, instance):
        """
        Initialize an FCoAuditBuilder instance.

        :param instance: An instance of FCoAudit to build upon.
        :type instance: FCoAudit
        :raises ValueError: If the provided instance is not an FCoAudit object.
        """
        if not isinstance(instance, FCoAudit):
            info_msg = f"Object must be {FCoAudit}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "level":
                self.instance.level = node.get(attribute)
            if attribute == "equal":
                self.instance.isequal = node.get(attribute)
                
    def _build_children(self, child):
        """
        FCoAudit does not contain any child items. 
        Method implemented since enforced by abstractclass defined in BaseBuilder.
        """
        pass
       
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if self.instance.isequal:
            self.instance.text += "Equal to " + self.instance.isequal
        else: 
            self.instance.text += node.text
        self.instance.text = clean_string(self.instance.text)
        self.instance.is_valid()
        return self.instance


class FCoManagement(BaseClass):
    """
    Class representing functional component management in the context of CC.

    :param _id: The ID of the FCoManagement element.
    :type _id: str or None
    :param _name: The name of the FCoManagement element.
    :type _name: str or None
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.isequal = None
        self.text = ""

    
    def get_formatted_text(self, level=1.0):
        header_level = "#" * int(level)
        formatted_text = f"\n{header_level} Management: " + self.text + "\n"
        return formatted_text
    
    def is_valid(self):
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> cannot be empty."
            raise common.C5decError(info_msg)
        return True


class FCoManagementBuilder(BaseBuilder):
    """
    Builder class for creating FCoManagement instances.

    :param instance: An instance of FCoManagement to build upon.
    :type instance: FCoManagement
    """

    def __init__(self, instance):
        """
        Initialize an FCoManagementBuilder instance.

        :param instance: An instance of FCoManagement to build upon.
        :type instance: FCoManagement
        :raises ValueError: If the provided instance is not an FCoManagement object.
        """
        if not isinstance(instance, FCoManagement):
            info_msg = f"Object must be {FCoManagement}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)


    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "equal":
                self.instance.isequal = node.get(attribute)
    
    def _build_children(self, child):
        """
        FCoManagement does not contain any child items. 
        Method implemented since enforced by abstractclass defined in BaseBuilder.
        """
        pass
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if self.instance.isequal:
            self.instance.text += "Equal to " + self.instance.isequal
        else: 
            self.instance.text += node.text
        self.instance.text = clean_string(self.instance.text)
        self.instance.is_valid()
        return self.instance


class FComponent(BaseClass):
    """
    Class representing a Functional Component in the context of CC:

    :param _id: The ID of the FComponent.
    :type _id: str, optional
    :param _name: The name of the FComponent.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attribute:
        - `hierarchical` (list): list of Ids
        - `dependencies` (list): list of Ids
        - `management` (FCoManagement): the component management
        - `audit`(FCoAudit): the component audit
        - `fco_rationale` (ParaSequence): the component rationale
        - `fco_user_notes` (ParaSequence): component user notes
        - `fco_evaluator_notes` (ParaSequence): component evaluator notes
        - `fco_levelling` (ParaSequence): componente levelling
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.hierarchical = []
        self.dependencies = []
        self.management = None
        self.audit = None
        self.fco_rationale = None
        self.fco_user_notes = None
        self.fco_evaluator_notes = None
        self.fco_levelling = None

    @property
    def element(self):
        return self.children

    def get_hierarchical_tree(self, h_tree=None, visited=None):
        if h_tree is None:
            h_tree = set()
        if visited is None:
            visited = set()
        if self in visited:
            return h_tree
        visited.add(self)
        h_components = self.hierarchical
        if not h_components:
            return h_tree
        else:
            h_tree.update(h_components)
            for h_component in h_components:
                h_obj = Index.get(h_component)
                h_obj.get_hierarchical_tree(h_tree=h_tree, visited=visited)
        return h_tree

    def get_dependency_pool(self, d_pool=None, visited=None):
        if d_pool is None:
            d_pool = set()
        if visited is None:
            visited = set()
        if self in visited:
            return d_pool
        visited.add(self)
        d_components = self.dependencies

        for d_component in d_components:
            # check if d_component is list and hence OR dependencies
            if isinstance(d_component, list):
                # add the OR tuple to the set
                d_pool.add(tuple(d_component))
                # iterate through or_components
                for or_component in d_component:
                    if or_component not in visited:
                        d_obj = Index.get(or_component)
                        d_obj.get_dependency_pool(d_pool=d_pool, visited=visited)
            else:
                d_pool.add(d_component)
                if d_component not in visited:
                    d_obj = Index.get(d_component)
                    d_obj.get_dependency_pool(d_pool=d_pool, visited=visited)
        return d_pool

    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n"

        if self.hierarchical:
            formatted_text += f"\nHierarchical to: {''.join(self.hierarchical[0])}\n"
        
        if self.dependencies:
            formatted_text += "\nDependencies: "
            for component in self.dependencies:
                # check if "or" dependency
                if len(component) > 1 and not isinstance(component, str):
                    formatted_text += f"[{' or '.join(component)}] "
                else:
                    # if no "or" dependency
                    formatted_text += f"{component} "
        for element in self.container:
            formatted_text += element.get_formatted_text(level=(level+1))
        return formatted_text

    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.fco_levelling\
              or self.fco_levelling.original_tag != "fco-levelling":
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> is missing component levelling."
            raise common.C5decError(info_msg)
        if not self.children \
            or not all(isinstance(child, FElement) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain child elements of type {FElement}."
            raise common.C5decError(info_msg)
        return True
    

class FComponentBuilder(BaseBuilder):
    """
    Builder class for creating FComponent instances.

    :param instance: An instance of FComponent to build upon.
    :type instance: FComponent
    """

    def __init__(self, instance):
        """
        Initialize an FComponentBuilder instance.

        :param instance: An instance of FComponent to build upon.
        :type instance: FComponent
        :raises ValueError: If the provided instance is not an FComponent object.
        """
        if not isinstance(instance, FComponent):
            info_msg = f"Object must be {FComponent}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

        
    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["fco-rationale",
                                "fco-user-notes",
                                "fco-evaluator-notes",
                                "fco-levelling"]
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == "fco-management":
            mgmt = FCoManagement()
            obj_ = FCoManagementBuilder(mgmt).build(child, self.instance)
            self.instance.management = obj_
            self.instance.container.append(obj_)
        if node_name == "fco-audit":
            audit = FCoAudit()
            obj_ = FCoAuditBuilder(audit).build(child, self.instance)
            self.instance.audit = obj_
            self.instance.container.append(obj_)
        if node_name == "f-element":
            element = FElement()
            if c5settings.SELECTED_CC_VERSION == "3R5":
                obj_ = FElementBuilder(element).build(child, self.instance)
            else:
                obj_ = FElementBuilder2022(element).build(child, self.instance)
            self.instance.children.append(obj_)
        if node_name == "fco-hierarchical":
            self.instance.hierarchical = [child.get("fcomponent")]
        if node_name == "fco-dependencies":
            for grandchild in child:
                if grandchild.tag == "fco-or":
                    component_list = []
                    for component in grandchild:
                        component_list.append(component.get("fcomponent"))
                    self.instance.dependencies.append(component_list)
                else:
                    if(grandchild.get("fcomponent") == None):
                        # no component
                        pass
                    else:
                        self.instance.dependencies.append(grandchild.get("fcomponent"))
              
        
class FFamily(BaseClass):
    """
    Class representing a Functional Family in the context of CC:

    :param _id: The ID of the FFamily.
    :type _id: str, optional
    :param _name: The name of the FFamily.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `ff_behaviour` (str): The behavior of the Functional Family.
        - `ff_application_notes` (ParaSequence): Application notes for the Functional Family.
        - `ff_user_notes` (ParaSequence): User notes for the Functional Family.
        - `ff_evaluator_notes` (ParaSequence): Evaluator notes for the Functional Family.
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.ff_behaviour = None
        self.ff_application_notes = None
        self.ff_user_notes = None
        self.ff_evaluator_notes = None

    @property
    def component(self):
        return self.children
        
    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.ff_behaviour\
              or self.ff_behaviour.original_tag != "ff-behaviour":
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> is missing family behaviour."
            raise common.C5decError(info_msg)
        if not self.children \
            or not all(isinstance(child, FComponent) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain child elements of type {FComponent}."
            raise common.C5decError(info_msg)
        return True

    
class FFamilyBuilder(BaseBuilder):
    """
    Builder class for creating FFamily instances.

    :param instance: An instance of FFamily to build upon.
    :type instance: FFamily
    """

    def __init__(self, instance):
        """
        Initialize an FFamilyBuilder instance.

        :param instance: An instance of FFamily to build upon.
        :type instance: FFamily
        :raises ValueError: If the provided instance is not an FFamily object.
        """
        if not isinstance(instance, FFamily):
            info_msg = f"Object must be {FFamily}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["ff-behaviour",
                                "ff-application-notes",
                                "ff-user-notes",
                                "ff-evaluator-notes"]
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == "f-component":
            component = FComponent()
            obj_ = FComponentBuilder(component).build(child, self.instance)
            self.instance.children.append(obj_)
    

class FClass(BaseClass):
    """
    Class representing a Functional Class in the context of CC.

    :param _id: The ID of the Functional Class.
    :type _id: str, optional
    :param _name: The name of the Functional Class.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `fc_introduction` (str): Introduction of the Functional Class.
        - `fc_informative_notes` (str): Informative notes related to the Functional Class.
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.fc_introduction = None
        self.fc_informative_notes = None
        
    @property
    def family(self):
        return self.children
    
    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.fc_introduction\
              or self.fc_introduction.original_tag != "fc-introduction":
            info_msg = f"<{self.__class__} at {hex(id(self))}>\
                  Must contain fc-introduction."
            raise common.C5decError(info_msg)
        if not self.fc_informative_notes\
              or self.fc_informative_notes.original_tag != "fc-informative-notes":
            info_msg = f"<{self.__class__} at {hex(id(self))}>\
                  Must contain fc-informative-notes."
            raise common.C5decError(info_msg)
        if not self.children \
            or not all(isinstance(child, FFamily) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain child elements of type {FFamily}."
            raise common.C5decError(info_msg)
        return True
        

class FClassBuilder(BaseBuilder):
    """
    Builder class for creating FClass instances.

    :param instance: An instance of FClass to build upon.
    :type instance: FClass
    """

    def __init__(self, instance):
        """
        Initialize an FClassBuilder instance.

        :param instance: An instance of FClass to build upon.
        :type instance: FClass
        :raises ValueError: If the provided instance is not an FClass object.
        """
        if not isinstance(instance, FClass):
            info_msg = f"Object must be {FClass}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["fc-introduction",
                                "fc-informative-notes"]
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == "f-family":
            family = FFamily()
            obj_ = FFamilyBuilder(family).build(child, self.instance)
            self.instance.children.append(obj_)


"""End: Functional Class Elements"""

"""Start: Assurance Class Elements"""


class DCElement:
    """
    Class representing a ae-dc-element in the context of CC. 
    This class is a child object of a WorkUnit and only contains 
    an Id referring to an existing AElement of type `developer` or `content`.
    """
    def __init__(self, _id=None):
        self._id = _id


class WorkUnit(BaseClass):
    """
    Class representing a work unit in the context of CC.

    :param _id: The ID of the work unit.
    :type _id: str, optional
    :param _name: The name of the work unit.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attribute:
        - `dc_element` (list): List of DC elements.
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.dc_element = []

    def is_valid(self):
        self.has_valid_id()
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> cannot be empty."
            raise common.C5decError(info_msg)
        return True
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"{header_level} {self._id.upper()} {self._name or ''}\n"
        for element in self.container:
            if isinstance(element, DCElement):
                continue
            formatted_text += element.get_formatted_text(level=(level+1))
        return formatted_text


class WorkUnitBuilder(BaseBuilder):
    """
    Builder class for creating WorkUnit instances.

    :param instance: An instance of WorkUnit to build upon.
    :type instance: WorkUnit
    """

    def __init__(self, instance):
        """
        Initialize a WorkUnitBuilder instance.

        :param instance: An instance of WorkUnit to build upon.
        :type instance: WorkUnit
        :raises ValueError: If the provided instance is not a WorkUnit object.
        """
        if not isinstance(instance, WorkUnit):
            info_msg = f"Object must be {WorkUnit}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        parent_id = parent_obj._id.rsplit(".", 1)[0]
        unit_id = UniqueIDManager().next(parent_id)
        if node.get("id"):
            assigned_id = node.get("id")
            if unit_id != assigned_id:
                unit_id = assigned_id
                info_msg = f"Derived Id for <{self.__repr__()} at {id(self)}> does not match\
                     assigned Id. Derived Id {unit_id} is overwritten with assigned Id {assigned_id}."
                log.info(info_msg)
        self.instance._id = unit_id
  
    def _build_children(self, child):
        node_name = child.tag
        if node_name == "ae-dc-element":
            elem_id = child.get("id")
            self.instance.dc_element.append(DCElement(elem_id))
            self.instance.container.append(DCElement(elem_id))
        if node_name == "para":
            obj_ = Para().build(child, self.instance)
            self.instance.container.append(obj_)
        if node_name == "subclause":
            obj_ = SubClause().build(child, self.instance)

            self.instance.container.append(obj_)

         
class AElement(BaseClass):
    """
    Class representing an assurance element in the context of CC. To differentiate 
    between the element type the AElement is assigned one of the valid types
    ("developer", "content", "evaluator").

    :param _id: The ID of the AElement.
    :type _id: str, optional
    :param el_type: The type of the AElement ("developer", "content", "evaluator").
    :type el_type: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `type` (str): The type of the AElement.
        - `list` (list): A List. 
        - `operation` (list): A list of Operation associated with the AElement.
        - `requirement` (str): the requirement stated by the AElement.
    """

    VALID_TYPES = ["developer", "content", "evaluator"]

    def __init__(self, _id=None, el_type=None):
        super().__init__(_id, None)
        self.type = el_type
        self.list = []
        self.operation = []
        self.requirement = ""

    def is_valid(self):
        self.has_valid_id()
        if self.type not in self.VALID_TYPES:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}>\
                  type must be one of {self.VALID_TYPES}, but is {self.type}."
            raise common.C5decError(info_msg)
        if self.is_empty():
            info_msg = f"<{self.__repr__()} at {hex(id(self))}>\ cannot be empty."
            raise common.C5decError(info_msg)
        return True
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n\n"
        for element in self.container:
            if hasattr(element, 'get_formatted_text'):
                formatted_text += element.get_formatted_text(level=(level + 1))
            else:
                raise common.C5decError(f"AttributeError: Object {element} does\
                                         not have a 'get_formatted_text' method.")
        return formatted_text


class AElementBuilder(BaseBuilder):
    """
    Builder class for creating AElement instances.

    :param instance: An instance of AElement to build upon.
    :type instance: AElement
    """

    def __init__(self, instance):
        """
        Initialize an AElementBuilder instance.

        :param instance: An instance of AElement to build upon.
        :type instance: AElement
        :raises ValueError: If the provided instance is not an AElement object.
        """
        if not isinstance(instance, AElement):
            info_msg = f"Object must be {AElement}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

    def _build_attributes(self, node, parent_obj=None):
        self.instance.parent = parent_obj
        for attribute in node.attrib:
            if attribute == "id":
                self.instance._id = node.get("id")
                
    def _build_children(self, child):
        node_name = child.tag
        if node_name == "list":
            obj_ = List().build(child, self.instance)
            self.instance.list.append(obj_)
            self.instance.container.append(obj_)
        if node_name in ["assignment", "selection"]:
            operation = Operation(op_type=node_name)
            obj_ = OperationBuilder(operation).build(child, self.instance)
            self.instance.operation.append(obj_)
            self.instance.container.append(obj_)
        if node_name == "xref":
            obj_ = XRef().build(child, self.instance)
            self.instance.container.append(obj_)
        if node_name == "m-workunit":
            unit = WorkUnit()
            obj_ = WorkUnitBuilder(unit).build(child, self.instance)
            self.instance.children.append(obj_)
                
    def build(self, node, parent_obj=None):
        self._build_attributes(node, parent_obj)
        if node.text:
            text = clean_string(node.text) + "\n"
            self.instance.requirement += text
            self.instance.container.append(Text(text))
            
        for child in node:
            self._build_children(child)
        Index.update(self.instance._id, self.instance)
        self.instance.is_valid()
        return self.instance
        
        
class AComponent(BaseClass):
    """
    Class representing an Assurance Component in the context of CC.

    :param _id: The ID of the AComponent.
    :type _id: str, optional
    :param _name: The name of the AComponent.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `hierarchical` (list): list of Ids
        - `dependencies` (list): list of Ids
        - `aco_objectives` (ParaSequence): component objectives
        - `aco_application_notes` (ParaSequence): component application notes
        - `msa_objectives` (ParaSequence): objective of the associated 
        evaluation sub-activity
        - `msa_application_notes` (ParaSequence): application notes of the
        associated evaluation sub-activity
        - `msa_input` (ParaSequence): required input of the associated evaluation 
        sub-activity
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.hierarchical = []
        self.dependencies = []
        self.aco_objectives = None
        self.aco_application_notes = None
        self.msa_objectives = None
        self.msa_application_notes = None
        self.msa_input = None

    @property
    def elements(self):
        return self.children
    
    @property
    def input(self):
        if self.msa_input:
            collection = self.msa_input.collector(Item, "type")
        else:
            collection = []
        input_items = []
        for item in collection:
            input_items.append(clean_string(item.text)[:-1])
        return input_items

    def get_hierarchical_tree(self, h_tree=None, visited=None):
        if h_tree is None:
            h_tree = set()
        if visited is None:
            visited = set()
        if self in visited:
            return h_tree
        visited.add(self)
        h_components = self.hierarchical
        if not h_components:
            return h_tree
        else:
            h_tree.update(h_components)
            for h_component in h_components:
                h_obj = Index.get(h_component)
                h_obj.get_hierarchical_tree(h_tree=h_tree, visited=visited)
        return h_tree

    def get_dependency_pool(self, d_pool=None, visited=None):
        if d_pool is None:
            d_pool = set()
        if visited is None:
            visited = set()
        if self in visited:
            return d_pool
        visited.add(self)
        d_components = self.dependencies
        if not d_components:
            return d_pool
        else:
            d_pool.update(d_components)
            for d_component in d_components:
                if d_component not in visited:
                    d_obj = Index.get(d_component)
                    d_obj.get_dependency_pool(d_pool=d_pool, visited=visited)
        return d_pool

    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n"

        if self.hierarchical:
            formatted_text += f"\nHierarchical to: {''.join(self.hierarchical[0])}\n"
        
        if self.dependencies:
            formatted_text += "\nDependencies: "
            for component in self.dependencies:
                # check if "or" dependency
                if len(component) > 1 and not isinstance(component, str):
                    comp_set = [comp for comp in component]
                    formatted_text += f"[{','.join(component)}], or\n"
                else:
                    # if no "or" dependency
                    formatted_text += f"{component}\n"
        for element in self.container:
            formatted_text += element.get_formatted_text(level=(level+1))
        return formatted_text
    
    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.children \
            or not all(isinstance(child, AElement) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}>\
                  must (only) contain child elements of type {AElement}."
            if self._id in ["ace_spd.1", "ace_obj.1"]: 
                # ace_spd.1 and ace_obj.1 refer to respective APE components.
                log.info(info_msg)
            else:
                raise common.C5decError(info_msg)
        return True


class AComponentBuilder(BaseBuilder):
    """
    Builder class for creating AComponent instances.

    :param instance: An instance of AComponent to build upon.
    :type instance: AComponent
    """

    def __init__(self, instance):
        """
        Initialize an AComponentBuilder instance.

        :param instance: An instance of AComponent to build upon.
        :type instance: AComponent
        :raises ValueError: If the provided instance is not an AComponent object.
        """
        if not isinstance(instance, AComponent):
            info_msg = f"Object must be {AComponent}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["aco-objectives",
                                "aco-application-notes",
                                "msa-objectives",
                                "msa-application-notes",
                                "msa-input"]
        AELEMENT = ["ae-developer", "ae-content", "ae-evaluator"]

        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name in AELEMENT:
            el_type = node_name.split("-")[1]
            element = AElement(el_type=el_type)
            obj_ = AElementBuilder(element).build(child, self.instance)
            self.instance.children.append(obj_)
        if node_name == "aco-hierarchical":
            self.instance.hierarchical.append(child.get("acomponent"))
        if node_name == "aco-dependsoncomponent":
            self.instance.dependencies.append(child.get("acomponent"))


class AFamily(BaseClass):
    """
    Class representing an Assurance Family in the context of CC.

    :param _id: The ID of the AFamily.
    :type _id: str, optional
    :param _name: The name of the AFamily.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `af_objectives` (ParaSequence): family objectives
        - `af_overview` (ParaSequence): family overview
        - `af_levelling_criteria` (ParaSequence): family levelling criteria
        - `af_application_notes` (ParaSequence): family application notes
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.af_objectives = None
        self.af_overview = None
        self.af_levelling_criteria = None
        self.af_application_notes = None

    @property
    def component(self):
        return self.children

    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.children \
            or not all(isinstance(child, AComponent) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must (only) contain child elements of type {AComponent}."
            raise common.C5decError(info_msg)
        return True


class AFamilyBuilder(BaseBuilder):
    """
    Builder class for creating AFamily instances.

    :param instance: An instance of AFamily to build upon.
    :type instance: AFamily
    """

    def __init__(self, instance):
        """
        Initialize an AFamilyBuilder instance.

        :param instance: An instance of AFamily to build upon.
        :type instance: AFamily
        :raises ValueError: If the provided instance is not an AFamily object.
        """
        if not isinstance(instance, AFamily):
            info_msg = f"Object must be {AFamily}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["af-objectives",
                                "af-overview", 
                                "af-levelling-criteria",
                                "af-application-notes"]
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == "a-component":
            component = AComponent()
            obj_ = AComponentBuilder(component).build(child, self.instance)
            self.instance.children.append(obj_)
        
        
class AClass(BaseClass):
    """
    Class representing an Assurance Class in the context of CC.

    :param _id: The ID of the Assurance Class.
    :type _id: str, optional
    :param _name: The name of the Assurance Class.
    :type _name: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `ac_introduction` (str): assurance class introduction.
        - `ac_overview` (str): assurance class overview.
        - `ac_application_notes` (ParaSequence): assurance class
          application note.
        - `ma_introduction` (str): introduction of associated 
        evaluation activity
        - `ma_objectives` (ParaSequence): objectives of associated
          evaluation activity
        - `ma_application_note` (ParaSequence): application note of
          associated evaluation activity
    """

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.ac_introduction = None
        self.ac_overview = None
        self.ac_application_notes = None
        self.ma_introduction = None
        self.ma_objectives = None
        self.ma_application_note = None

    @property
    def family(self):
        return self.children
        
    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.ac_introduction\
              or self.ac_introduction.original_tag != "ac-introduction":
            info_msg = f"<{self.__repr__()} at {hex(id(self))}>\
                  Must contain ac-introduction."
            raise common.C5decError(info_msg)
        if not self.children \
            or not all(isinstance(child, AFamily) for child in self.children):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must (only) contain child elements of type {AFamily}."
            raise common.C5decError(info_msg)
        return True
        

class AClassBuilder(BaseBuilder):
    """
    Builder class for creating AClass instances.

    :param instance: An instance of AClass to build upon.
    :type instance: AClass
    """

    def __init__(self, instance):
        """
        Initialize an AClassBuilder instance.

        :param instance: An instance of AClass to build upon.
        :type instance: AClass
        :raises ValueError: If the provided instance is not an AClass object.
        """
        if not isinstance(instance, AClass):
            info_msg = f"Object must be {AClass}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

        
    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = ["ac-introduction",
                                "ac-overview",
                                "ac-application-notes",
                                "ma-introduction",
                                "ma-objectives",
                                "ma-application-notes"]
        
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == "a-family":
            afamily = AFamily()
            obj_ = AFamilyBuilder(afamily).build(child, self.instance)
            self.instance.children.append(obj_)


"""End: Assurance Class Elements"""

"""Start: Evaluataion Assurance Levels"""

class Package(BaseClass):

    def __init__(self, _id=None, _name=None):
        super().__init__(_id, _name)
        self.acronym = None
        self.type = "assurance"
        self.objectives = None
        self.assurance_components = None
    
    def __str__(self):
        return self.get_formatted_text()
    
    def get_formatted_text(self, level=1.0):
        formatted_text = ""
        header_level = "#" * int(level)
        formatted_text += f"\n{header_level} {self._id.upper()} {self._name or ''}\n"
        for element in self.container:
            formatted_text += element.get_formatted_text(level=(level+1))
        formatted_text += "\nComponent List:\n\n"
        formatted_text += "ID        |     Name \n"
        formatted_text += "----------|---------------\n"
        for child in self.children:
            formatted_text += f"{child._id} | {child._name}\n"
        return formatted_text
    
    @property
    def components(self):
        return self.children

    def link_components(self):
        # method to call after CCDocument was build to replace component str with respectice objects
        if not all(isinstance(child, str) for child in self.children) and self.is_valid():
            return
        components = []
        for child in self.children:
            component = Index.get(child)
            components.append(component)
        self.children = components

    def is_valid(self):
        self.has_valid_id()
        self.has_valid_name()
        if not self.objectives:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain an objective."
            raise common.C5decError(info_msg)
        if not self.assurance_components:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain Assurance Components."
            raise common.C5decError(info_msg)
        if not self.children:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> must contain components."
            raise common.C5decError(info_msg)

        types = set([type(child) for child in self.children])
        if len(types) > 1:
            # check if children are all of same type:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> components are of different types {types}."
            raise common.C5decError(info_msg)
        if all(isinstance(child, str) for child in self.children):
            # is valid is called after build and component Ids not yet linked to object
            try:
                if not all(isinstance(Index.get(child), (AComponent, FComponent)) for child in self.children):
                    info_msg = f"<{self.__repr__()} at {hex(id(self))}> component IDs must correspond to assurance of functional components." 
                    raise common.C5decError(info_msg)
            except KeyError:
                info_msg = f"Components of <{self.__repr__()} at {hex(id(self))}> not in Index."
                raise common.C5decError(info_msg)
            child_0 = Index.get(self.children[0])
            if not all(isinstance(Index.get(child), type(child_0)) for child in self.children):
                info_msg = f"<{self.__repr__()} at {hex(id(self))}> component IDs must all correspond to same component type. "
                raise common.C5decError(info_msg)
            return True
        if all(isinstance(child, BaseClass) for child in self.children):
            # is_valid called after linking Ids to objects or when manually defining Packages and assigning Component Objects.
            if not all(child._id.lower() in Index._index for child in self.children):
                info_msg = f"Components of <{self.__repr__()} at {hex(id(self))}> not in Index."
                raise common.C5decError(info_msg)
            if not all(isinstance(child, (AComponent, FComponent)) for child in self.children):
                info_msg = f"Components of <{self.__repr__()} at {hex(id(self))}> must be of type {AComponent} or {FComponent}."
                raise common.C5decError(info_msg)
            if not all(isinstance(child, type(self.children[0])) for child in self.children):
                info_msg = f"Components of <{self.__repr__()} at {hex(id(self))}> must be of same type!"
                raise common.C5decError(info_msg)
            return True

    def get_descendants(self, visited=None):
        self.link_components()
        super().get_descendants(visited=visited)

class PackageBuilder(BaseBuilder):

    def __init__(self, instance):
        if not isinstance(instance, Package):
            info_msg = f"Object must be {Package}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)

    def _build_attributes(self, node, parent_obj):
        self.instance.parent = parent_obj
        self.instance.acronym = node.tag
        for attribute in node.attrib:
            if attribute == "id":
                self.instance._id = node.get(attribute)
            if attribute == "name":
                self.instance._name = node.get(attribute)

    def _build_children(self, child):
        PARASEQUENCE_OBJECTS = [f"{self.instance.acronym}-objectives",
                                f"{self.instance.acronym}-assurance-components"]
        
        node_name = child.tag
        if node_name in PARASEQUENCE_OBJECTS:
            str_to_attrib = node_name.split('-', 1)[-1].replace("-", "_")
            obj_ = ParaSequence().build(child, self.instance)
            self.instance.container.append(obj_)
            setattr(self.instance, str_to_attrib, obj_)
        if node_name == f"{self.instance.acronym}-component":
            acomponent = child.get("acomponent")
            self.instance.children.append(acomponent)
        

"""End: Evaluation Assurance Levels"""

"""Start: CC Document Class"""


class CCDocument(BaseClass):
    """
    The CCDocument class serves as the root class for initializing and representing 
    a Common Criteria document.

    :param version: Version of the Common Criteria document, defaults to None
    :type version: str, optional
    :param revision: Revision number of the Common Criteria document, defaults to None
    :type revision: str, optional
    :param lang: Language in which the document is written, defaults to "EN"
    :type lang: str, optional

    Inherits from `BaseClass` and adds the following attributes:
        - `clause` (list): List of clauses.
        - `f_class` (list): List of Functional Classes.
        - `a_class` (list): List of Assurance Classes.
        - `eal` (list): List of Evaluation Assurance Levels.
        - `cap` (list): List of Composed Assurance Package.
    """

    def __init__(self, version=None, revision=None, lang="EN"):
        super().__init__()
        self.version = version
        self.revision = revision
        self.lang = lang
        self.clause = []
        self.f_class = []
        self.a_class = []
        self.eal = []
        self.cap = []

    def __str__(self):
        """
        Returns a formatted string representation of the CCDocument object.
        
        :return: Formatted string
        :rtype: str
        """
        """sout = f"This is version {self.version}{self.revision} of the Common Criteria.\n"
        sout += "The document is outlined as follows:\n"
        sout += "Index\t Clause title\t Clause type\n"
        index = 0
        for clause in self.clause:
            sout += f"{index}\t {clause.title}\t {clause.type}\n"
            index += 1
        return sout"""
        sout = ""
        for container in self.container:
            sout += container.get_formatted_text()
        return sout
    
    def is_valid(self):
        if not self.version:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> Version is missing."
            raise common.C5decError(info_msg)
        if not self.revision:
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> Revision is missing"
            log.error(info_msg)
            # raise common.C5decError(info_msg)
        if not all([self.clause, self.f_class, self.a_class, self.eal, self.cap]):
            info_msg = f"<{self.__repr__()} at {hex(id(self))}> Incomplete."
            log.error(info_msg)
            # raise common.C5decWarning(info_msg)
        for element in self.container:
            element.is_valid()
        return True
        
    
class CCDocumentBuilder(BaseBuilder):
    """
    Builder class for creating CCDocument instances.

    :param instance: An instance of CCDocument to build upon.
    :type instance: CCDocument
    """

    def __init__(self, instance):
        """
        Initialize a CCDocumentBuilder instance.

        :param instance: An instance of CCDocument to build upon.
        :type instance: CCDocument
        :raises ValueError: If the provided instance is not a CCDocument object.
        """
        if not isinstance(instance, CCDocument):
            info_msg = f"Object must be {CCDocument}, but is {type(instance)}."
            raise common.C5decError(info_msg)
        super().__init__(instance)
        
    def _build_attributes(self, node, parent_obj=None):
        self.instance._original_tagname = node.tag
        for attribute in node.attrib:
            if attribute == "version":
                self.instance.version = node.get(attribute)
            if attribute == "revision":
                revision = node.get(attribute)
                try:
                    self.instance.revision = int(float(revision))
                except ValueError:
                    match = re.search(r"(\d+)", revision)
                    self.instance.revision = int(match.group(1)) if match else 1
            if attribute == "lang":
                self.instance.lang = node.get(attribute)
        if c5settings.SELECTED_CC_VERSION == "3R5":
            self.instance._id = "CCv" + str(int(float(self.instance.version))) + \
                "R" + str(int(float(self.instance.revision)))
        else:
            self.instance._id = "CCv2022R1"
    
    def _build_children(self, child):
        UniqueIDManager()
        node_name = child.tag
        if node_name == "clause":
            obj_ = Clause().build(child, self.instance)
            obj_.original_tagname_ = node_name
            self.instance.clause.append(obj_)
            self.instance.container.append(obj_)
        if node_name == "f-class":
            fclass = FClass()
            obj_ = FClassBuilder(fclass).build(child, self.instance)
            obj_.original_tagname_ = node_name
            self.instance.f_class.append(obj_)
            self.instance.container.append(obj_)
        if node_name == "a-class":
            aclass = AClass()
            obj_ = AClassBuilder(aclass).build(child, self.instance)
            self.instance.a_class.append(obj_)
            self.instance.container.append(obj_)
        if node_name in ["eal", "cap"]:
            package = Package()
            obj_ = PackageBuilder(package).build(child, self.instance)
            getattr(self.instance, obj_.acronym).append(obj_)
            self.instance.container.append(obj_)
    
    def build(self, node, parent_obj=None):
        self._build_attributes(node)
        for child in node:
            self._build_children(child)
        Index.update(self.instance._id, self.instance)
        packages = list(Index.yield_obj(Package))
        for package in packages:
            package.link_components()
        self.instance.is_valid()
        return self.instance

"""End: CC Document Class"""



"""Start: Read XML"""

def parsexml_(file_path, parser=None, **kwargs):
    """
    Parse an XML file using the specified parser or a default parser.

    :param inFilePath: The path to the XML file to be parsed.
    :type inFilePath: str or os.PathLike
    :param parser: The XML parser to use (optional). If not provided, a default parser is used.
    :type parser: lxml.etree.XMLParser, optional
    :param **kwargs: Additional keyword arguments to pass to the XML parser.

    :return: The parsed XML document.
    :rtype: lxml.etree.ElementTree

    This function reads and parses an XML file located at the specified path.
    It allows you to specify a custom XML parser (such as one with specific options)
    or use the default lxml ElementTree compatible parser. Any additional keyword
    arguments provided are passed to the XML parser.

    Example usage:
    ```
    parsed_doc = parsexml_("/path/to/myfile.xml")
    ```
    """
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g., comments are ignored.
        try:
            parser = etree_.ETCompactXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(file_path, os.PathLike):
            file_path = os.path.join(file_path)
    except AttributeError:
        pass
    doc = etree_.parse(file_path, parser=parser, **kwargs)
    return doc

def load_cc_xml(version="3R5", parser=None, silence=False):
    """
    Load a Common Criteria XML document based on the specified version.

    :param version: The Common Criteria version to load (e.g., "3R5").
    :type version: str
    :param parser: The XML parser to use (optional). If not provided, a default parser is used.
    :type parser: lxml.etree.XMLParser, optional
    :param silence: Whether to suppress standard output messages (default is False).
    :type silence: bool

    :return: The root object representing the loaded Common Criteria document.
    :rtype: CCDocument

    This function loads a Common Criteria XML document based on the specified version.
    It reads the XML file associated with the version and constructs a Python object
    representing the Common Criteria document. You can optionally provide a custom
    XML parser (such as one with specific options) or use the default parser. The
    function also allows you to silence standard output messages.

    Example usage:
    ```
    root_object = load_cc_xml("3R5", parser=None, silence=True)
    ```
    """
    xml_version_path = c5settings.CC_VERSION_TO_PATH.get(version)

    doc = parsexml_(xml_version_path, parser)
    root_node = doc.getroot()

    if root_node.tag == "cc":
        root_class = CCDocument()
    else:
        info_msg = f"Root element is {root_node.tag}. Root element must be 'cc'."
        raise common.C5decError(info_msg)
    
    root_obj = CCDocumentBuilder(root_class).build(root_node)
    
    info_msg = "XML successfully parsed. "
    info_msg += f"CC version {root_obj.version} Revision {root_obj.revision} loaded.\n"
    log.info(info_msg)

    if not silence:
        sys.stdout.write(info_msg)

    Index().set_cc_tree(root_obj)

    return root_obj

"""End: Read XML"""

"""Start: dependency validation methods"""

def check_hierarchical(component, components_set, inverted=False):
    if not inverted:
        component_obj = Index.get(component)
        h_tree = component_obj.get_hierarchical_tree()
        if h_tree and any([h_comp in components_set for h_comp in h_tree]):
            components_set -= set(h_tree)
            return True
    else:
        for comp in components_set:
            comp_obj = Index.get(comp)
            h_tree = comp_obj.get_hierarchical_tree()
            if component in h_tree:
                return True
    return False

def check_dependencies(component, components_set):
    component_obj = Index.get(component)
    dependency_pool = component_obj.get_dependency_pool()
    
    added = False
    for dep in dependency_pool:
        # check if OR dependency
        if isinstance(dep, tuple):
            # check if any OR component exists or any hierarchical components.
            if not any(component in components_set for component in dep)\
            and not any(check_hierarchical(component, components_set, inverted=True) for component in dep):
                components_set.add(dep[0])
                added = True
        else:
            if dep not in components_set\
            and not check_hierarchical(dep, components_set, inverted=True):
                components_set.add(dep)
                added = True
    return added

def validate_dependencies(component_ids):
    """
    Validate dependencies and identify redundant or missing components in a components set.

    This function checks the dependencies of components to identify any missing
    dependencies and redundant components. It returns a boolean value indicating the validaty
    of the provided set and a potential valid set in case the provided set is invalid.

    :param components: A list of components to validate.
    :type components: list/set of BaseClass (FComponent | AComponent)
    :return: A tuple containing sets of redundant components and missing dependencies.
    :rtype: tuple of (set, set)
    """
    components = [comp_id.lower() for comp_id in component_ids]
    components_set = set(components)
    processed = set()
    component_queue = components.copy()
    
    changed = set()
    while component_queue:
        component = component_queue.pop(0)
        processed.add(component)
        # Checking for hierarchical components that supersede others
        removed_superseded = check_hierarchical(component, components_set)
        changed.add(removed_superseded)
        # Checking for missing dependencies
        added_missing = check_dependencies(component, components_set)
        changed.add(added_missing)
        # add components that were not processed to component_queue
        to_visit = components_set - processed
        component_queue.extend(to_visit)

    selection_is_valid = not any(changed)


    return selection_is_valid, components_set


"""End: dependency validation methods"""

"""Start: Doorstop Index"""


def save_index(index, filepath):
    filepath += "/index.json"
    with open(filepath, 'w') as file:
        json.dump(index, file, indent=4)


def load_index(filepath) -> None:
    filepath += "/index.json"
    with open(filepath, 'r') as file:
        index = json.load(file)
    return index


def update_index(prefix):
    """method to update the doorstop index in case changes where made manually."""
    doc = get_evaluation_documents(doc_prefix=prefix)
    index = load_index(doc.path)

    components = index.get("Components")
    for component, details in components.items():
        for workunit, udetails in details.get("workunit").items():
            item = doc.find_item(udetails["UID"])
            item.review()
            if udetails["hash"] != item._data["reviewed"]:
                udetails["verdict"] = item._data["verdict"]
                udetails["hash"] = str(item._data["reviewed"])
    save_index(index, doc.path)


def validate_index(index) -> bool:
    """called when loading index to validate that index """
    try:
        root = index["DoorstopInfo"]["root"]
        path = index["DoorstopInfo"]["path"]
        prefix = index["DoorstopInfo"]["prefix"]
        tree = doorstop.build(cwd=path, root=root)
        doc = tree.find_document(prefix)
    except doorstop.common.DoorstopError:
        info_msg = f"Index Document with Prefix {prefix} does not exist."
        raise common.C5decError(info_msg)

    components = index["Components"]

    units_validated = 0
    for data in components.values():
        workunits = data["workunit"]
        for unit in workunits:
            uid = workunits[unit]["UID"]
        # check that item exists
            try:
                item = doc.find_item(uid)
                # check that item does contain correct Work Unit
                if item._data["header"].lower() != unit:
                    info_msg = f"Mismatch: Doorstop Item {uid} does not contain Work Unit {unit}"
                    raise common.C5decError(info_msg)
            except doorstop.common.DoorstopError:
                info_msg = f"Work Unit {unit} missing!"
                raise common.C5decError(info_msg)

            # check that index does refer to the latest version of item
            item.review()
            if workunits[unit]["hash"] != item._data["reviewed"].value:
                info_msg = f"Discrepancy between Index and doorstop document at {uid}!"
                raise common.C5decError(info_msg)
            units_validated += 1
    # check that Doorstop Document does not contain additional Work units
    if units_validated != len(doc._items):
        info_msg = "Additional Work Units detected!"
        raise common.C5decError(info_msg)
    return True


def create_index(eval_index: dict, workunits: dict, gen_info: dict, filepath) -> dict:
    """
    implement checks for input. Document what gen_info should include
    """
    component_dict = {"Components" : {key : {'input': eval_index[key],
                                    'workunit': workunits[key]
                                    } for key in eval_index}}

    index = {**gen_info, **component_dict}
    save_index(index, filepath)
    return index


"""End: Doorstop Index"""

"""Start: Evaluation Checklist"""


def save_document_config(doc):
    data = {}
    sets = {}
    for key, value in doc._data.items():
        if key == "prefix":
            sets[key] = str(value)
        elif key == "parent":
            if value:
                sets[key] = value
        else:
            sets[key] = value
    data["settings"] = sets

    attributes = {}
    attributes["defaults"] = c5settings.DEFAULT_EVALUATION_ATTRIBUTES
    attributes["publish"] = c5settings.DEFAULT_PUBLISH_ATTRIBUTES
    attributes["reviewed"] = c5settings.DEFAULT_EVALUATION_REVIEWED
    data["attributes"] = attributes
    text = doc._dump(data)
    doc._write(text, doc.config)


def create_evaluation_document(rootpath=None, doc_prefix=None):
    if rootpath == None:
        root = c5settings.PROJECT_ROOT
    else:
        root = rootpath
    if doc_prefix == None:
        doc_prefix = "EVAL"
    path = root + "/evaluation/" + doc_prefix.lower()

    tree = doorstop.build(cwd=path, root=root)
    doc = doorstop.Document.new(tree, path, root=rootpath, prefix=doc_prefix,
                                sep=c5settings.DEFAULT_SEPARATOR, 
                                digits=c5settings.DEFAULT_DIGITS,
                                parent=c5settings.DOORSTOP_ROOT,
                                itemformat=c5settings.DEFAULT_ITEMFORMAT,
                                auto=False)
    save_document_config(doc)
    doc.load(reload=True)
    log.info(f"Doorstop was initialized at {path}")
    return doc


def get_evaluation_documents(rootpath=None, doc_prefix=None):
    index = "index.json"
    if rootpath == None:
        root = c5settings.PROJECT_ROOT
    else:
        root = rootpath
    tree = doorstop.build(cwd=".", root=root)

    if doc_prefix:
        document = tree.find_document(doc_prefix)
        index_path = os.path.join(document.path, index)
        if os.path.isfile(index_path):
            return document

    evaluation_documents = []
    for document in tree.documents:
        index_path = os.path.join(document.path, index)
        if os.path.isfile(index_path):
            evaluation_documents.append(document)
    return evaluation_documents


def get_doorstop_document(rootpath=None, doc_prefix=None):
    if rootpath == None:
        root = c5settings.PROJECT_ROOT
    else:
        root = rootpath
    if doc_prefix == None:
        doc_prefix = "EVAL"
    path = root + "/evaluation/" + doc_prefix.lower()
    tree = doorstop.build(cwd=path, root=root)
    doc = tree.find_document(doc_prefix)
    return doc


def get_checklist_items(prefix):
    try:
        doc = get_evaluation_documents(doc_prefix=prefix)
    except doorstop.common.DoorstopError:
        docs = get_evaluation_documents()
        docs_prefix = [str(doc.prefix) for doc in docs]
        options = ('\n').join(docs_prefix)
        raise common.C5decError(f"No Evaluation Checklist found for {prefix}. \nPlease select from: \n{options}")
    
    index = load_index(doc.path)
    components = index.get("Components")

    units = []
    for component, details in components.items():
        for workunit in details.get("workunit"):
            uid = components[component]["workunit"][workunit]["UID"]
            item = doc.find_item(uid)
            units.append((workunit.upper(), item))
    return units


def get_workunits_for_components(components: [AComponent]) -> dict:
    if not all(isinstance(component, AComponent) for component in components):
        info_msg = "Input components must be of type AComponent."
        raise common.C5decError(info_msg)

    component_dict = {}
    for component in components:
        workunits = component.collector(WorkUnit, mode="type")
        component_dict[component._id] = {unit._id: {"UID":"",
                                                    "hash":""
                                                    } for unit in workunits}
    return component_dict


def get_input_for_components(components: [AComponent]) -> dict:
    if not all(isinstance(component, AComponent) for component in components):
        info_msg = "Input components must be of type AComponent."
        raise common.C5decError(info_msg)
    
    component_dict = {}
    for component in components:
        inputs = component.input
        component_dict[component._id] = inputs
    return component_dict


def create_eval_item_dict(workunit: WorkUnit) -> dict:
    def get_info(obj):
        return {
            'id': getattr(obj, '_id', None),
            'text': obj.get_formatted_text() if hasattr(obj, 'get_formatted_text') else None
        }
    
    workunit_info = get_info(workunit)
    workunit_id = workunit_info['id'].upper()
    workunit_text = ('\n').join(workunit_info['text'].split('\n')[1:])
    element = workunit.parent
    element_info = get_info(element)
    component = element.parent
    component_info = get_info(component)
    dc_elements = workunit.dc_element if isinstance(workunit.dc_element, list) else [workunit.dc_element]
    dc_elements_info = [get_info(Index.get(dc_elem._id)) for dc_elem in dc_elements]

    eval_item_dict = {
        'component': component_info['id'],
        'element': element_info['id'],
        'element_description': element_info['text'],
        'dc_element': [],
        'dc_element_description': [],
        'header': workunit_id,
        'text': workunit_text,
        'evidence': '',
        'verdict': 'inconclusive'
    }

    for info in dc_elements_info:
        eval_item_dict['dc_element'].append(info['id'])
        eval_item_dict['dc_element_description'].append(info['text'])
    return eval_item_dict


def create_evaluation_checklist(components: [AComponent], gen_info: dict, export_path=None, doc_prefix=None) -> None:
    eval_input = get_input_for_components(components)
    # If component set is valid retrieve component - workunits dict
    workunit_dict = get_workunits_for_components(components)
    doc = create_evaluation_document(export_path, doc_prefix)
    
    doorstop_info = {"DoorstopInfo": {"root": doc.root,
                                      "path": doc.path,
                                      "prefix": doc.prefix}}
    index_info = {**doorstop_info, **gen_info}

    for component in components:
        units = workunit_dict[component._id]
        for unit in list(units.keys()):
            unit_object = Index.get(unit)
            defaults = create_eval_item_dict(unit_object)
            item = doc.add_item()
            item.set_attributes(defaults)
            item.review()
            units[unit]["UID"] = str(item.uid)
            units[unit]["verdict"] = "inconclusive"
            units[unit]["hash"] = item._data["reviewed"].value

    create_index(eval_input, workunit_dict, index_info, filepath=doc.path)
    return doc

class ChecklistBuilder:

    def __init__(self, cc_version="3R5", checklist_name="chklist", silence=True):
        self.checklist_name = checklist_name
        self.cc_version = cc_version
        if not Index().is_tree_loaded():
            try:
                load_cc_xml(cc_version, silence=silence)
            except Exception as e:
                info_msg = f"The provided CC version {cc_version} does not exist."
                raise common.C5decError(info_msg)
        self.cc_index = Index

    def build_component_id_vector_for_classes(self, class_id_vector):
        cc_index = self.cc_index
        component_id_vector = []
        for cc_class_id in class_id_vector:
                cc_class = cc_index.get(cc_class_id)
                for family in cc_class.get_children():
                    for component in family.get_children():
                        component_id_vector.append(component._id.upper())
        
        return component_id_vector

    def export_eval_checklist(self, class_id_vector=None, component_id_vector=None):
        """
        Creates an evaluation checklist and exports it to a spreadsheet (xlsx)
        """
        checklist_name = self.checklist_name
        cc_version = self.cc_version
        cc_index = self.cc_index

        if component_id_vector is None:
            if class_id_vector is None:
                cc_object = AClass
                cc_classes = cc_index.yield_obj(cc_object)
                class_id_vector = [cc_class._id.upper() for cc_class in cc_classes]
                component_id_vector = self.build_component_id_vector_for_classes(class_id_vector)
            else:
                component_id_vector = self.build_component_id_vector_for_classes(class_id_vector)

        current_time = time.strftime("%Y%m%d-%H%M%S")
        info = dict({"identifier": "{}-{}".format(checklist_name,current_time), "Timestamp": current_time})
        gen_info = {"GeneralInfo" : {**{"CCVersion": cc_version}, **info}}

        components = [cc_index.get(component) for component in component_id_vector]
        usr_prefix = info["identifier"]

        try:
            log.debug(f"save in : {c5settings.PROJECT_ROOT} - with prefix: {usr_prefix}")
                # abort if a doorstop document with the same prefix exists
            if(doorstop.find_document(usr_prefix)):
                print("ERROR: The selected prefix '{usr_prefix}' is already in use in your repository.")
                
        except doorstop.common.DoorstopError as x:
            log.debug(f"Doorstop error: {x}")
            try:
                create_evaluation_checklist(components, gen_info, 
                                        export_path=c5settings.PROJECT_ROOT, 
                                        doc_prefix=usr_prefix)
                
                export_format = ".xlsx"
                export_file_name = usr_prefix+export_format
                export_path = os.path.join(c5settings.EXPORT_FOLDER, export_file_name)
                c5transformer.export_ssdlc_document(usr_prefix, path=export_path, format=export_format)

                # Rename first sheet from Sheet to the EVAL WU sheet name 
                exported_checklist_df = pd.read_excel(export_path)
                writer = pd.ExcelWriter(export_path)
                exported_checklist_df.to_excel(writer, sheet_name=c5settings.ETR_EVAL_WU_SHEET_NAME, index=False)

                # Add AWI sheet and populate it using the default etr-eval-checklist.xlsx file
                default_etr_checklist_file_name = c5settings.ETR_EVAL_CHECKLIST_DEFAULT_FILE_NAME+".xlsx"
                awi_df = pd.read_excel(os.path.join(c5settings.ASSETS_FOLDER_NAME, c5settings.ETR_FOLDER_NAME, default_etr_checklist_file_name), sheet_name=c5settings.ETR_EVAL_AWI_SHEET_NAME)

                awi_df.to_excel(writer, sheet_name=c5settings.ETR_EVAL_AWI_SHEET_NAME, index=False)
                writer.close()


                print("Evaluation checklist created and exported to: {}".format(export_path))
            except doorstop.common.DoorstopError as e:
                print(e)

"""End: Evaluation Checklist"""

"""Start: CLI methods"""


def get_item(item_id, version, silence=True):
    load_cc_xml(version, silence=silence)
    item = Index.get(item_id)
    print(item)


def validate(item_ids, version, mode="dep", silence=True):
    """
    Validate components in a Common Criteria document.

    This function validates components in a Common Criteria document based on the specified mode.

    :param item_ids: A list of item IDs to validate.
    :type item_ids: list of str
    :param version: The version of the Common Criteria document.
    :type version: str
    :param mode: The validation mode ('dep' for dependency validation), defaults to "dep".
    :type mode: str, optional
    :param silence: If True, suppresses printing validation messages, defaults to True.
    :type silence: bool, optional
    """
    if mode == "dep":
        load_cc_xml(version, silence=silence)
        is_valid, valid_set = validate_dependencies(item_ids)

        if is_valid:
            print("Selection valid!")
        else:
            print(f"Selection invalid!\n Potential valid set based on your selection {valid_set}")
    else:
        print("Validation mode currently not supported")


class CLIChecklistHandler:

    def __init__(self):
        # maybe add a path at some point and default to root if not specified.
        pass

    def create(self, version, item_ids, prefix, info=None, silence=True):
        load_cc_xml(version, silence=silence)
        is_valid, valid_set = validate_dependencies(item_ids)
        if not is_valid:
            print(f"Component selection not valid. Potential valid set: {valid_set}")
            # return
            log.info("Component selection not valid. Potential valid set: {valid_set}")
        components = [Index.get(_id) for _id in item_ids]
        create_evaluation_checklist(components, info, doc_prefix=prefix)

    def list(self, prefix):
        items = get_checklist_items(prefix)
        output = "Work Unit ID\tUID\t\tVerdict\n"
        for workunit, item in items:
            output += f"{workunit.upper()}\t{str(item.uid)}\t{item._data['verdict']}\n"
        print(output)

    def update(self, prefix):
        update_index(prefix)

    def validate(self, prefix):
        """
        Method to validate Checklist. For now only validates that index corresponds to current doc
        In the future this will be the wrapper for all relevant validations.
        """
        doc = get_evaluation_documents(doc_prefix=prefix)
        index = load_index(doc.path)
        if validate_index(index):
            print(f"{prefix} is valid.")

    def _extract_verdicts(self, index):
        for component in index["Components"].values():
            for workunit in component["workunit"].values():
                yield workunit["verdict"]

    def status(self, prefix):
        doc = get_evaluation_documents(doc_prefix=prefix)
        index = load_index(doc.path)
        verdicts = list(self._extract_verdicts(index))
        total = len(verdicts)
        if total == 0:
            status = f"No Work Units for {prefix}."
            print(status)
            return 
        passed = 0
        failed = 0
        for verdict in verdicts:
            if verdict == "pass":
                passed += 1
            if verdict == "fail":
                failed += 1
        status = f" Passed: {passed}, Failed: {failed}, Total: {total}"
        print(status)

    def edit(self, prefix, _id):
        doc = get_evaluation_documents(doc_prefix=prefix)
        _id = _id.lower()
        try:
            # assuming that _id is UID
            item = doc.find_item(_id)
        except doorstop.common.DoorstopError:
            # not an UID or does not exist, try converting _id to UID
            index = load_index(doc.path)
            uid = None
            for _, details in index.get("Components", {}).items():
                if _id in details.get("workunit", {}):
                    uid = details["workunit"][_id]["UID"]
            if not uid:
                print(f"No item found for {prefix} and {_id}.")
                return
            item = doc.find_item(uid)
        return item.path

    def publish(self, prefix, path, template=None):
        tree = doorstop.build()
        doc = tree.find_document(prefix)
        doorstop.core.publisher.publish(doc, path, template=template)


class ETR:

    def __init__(self, checklist_name=c5settings.ETR_EVAL_CHECKLIST_FILE_NAME, checklist_type = "xlsx", silence=True):
        self.checklist_file_name = checklist_name + "." + checklist_type
        
        self.output_folder_name = c5settings.ETR_OUTPUT_FOLDER_NAME
        self.output_folder_path = os.path.join(c5settings.ASSETS_FOLDER_NAME, c5settings.ETR_FOLDER_NAME, self.output_folder_name)

        if not os.path.exists(self.output_folder_path):
            os.makedirs(self.output_folder_path)

        self.input_file_path = os.path.join(c5settings.ASSETS_FOLDER_NAME, c5settings.ETR_FOLDER_NAME, self.checklist_file_name)
        self.etr_partial_export_file_name = "analysis.qmd"
        self.etr_table_export_file_name = "table.md"

    def read_csv_to_df(self, csv_path) -> pd.DataFrame:
        return pd.read_csv(csv_path)

    def get_wu_awi(self, df, wu_id):
        for index, row in df.iterrows():
            if row[c5settings.ETR_EVAL_WU_ID_COL] == wu_id:
                print(row)

    def filter_wu_df_by_family(self, df, family_name):
        filtered_df = df.loc[df[c5settings.ETR_EVAL_WU_ID_COL].str.contains(family_name)]
        return filtered_df

    def filter_awi_df_by_wu_id(self, df, wu_id):
        filtered_awi_df = df.loc[df[c5settings.ETR_EVAL_WU_ID_COL] == wu_id]
        return filtered_awi_df

    def family_wu_to_etr(self, family_name):
        output_file_name = os.path.join(self.output_folder_path, family_name + "-" + self.etr_partial_export_file_name)
        writer = open(output_file_name, 'w+')
        wu_df = pd.read_excel(self.input_file_path, sheet_name=c5settings.ETR_EVAL_WU_SHEET_NAME)
        awi_df = pd.read_excel(self.input_file_path, sheet_name=c5settings.ETR_EVAL_AWI_SHEET_NAME)

        f_wu_df = self.filter_wu_df_by_family(wu_df, family_name)
        etr_content = list()
        for index, row in f_wu_df.iterrows():
            f_awi_df = self.filter_awi_df_by_wu_id(awi_df, row[c5settings.ETR_EVAL_WU_ID_COL])

            line = "### " + str(row[c5settings.ETR_EVAL_WU_ID_COL]) + "\n"
            etr_content.append(line)

            line = self.make_markdown_line(row[c5settings.ETR_EVAL_WU_DESCRIPTION_COL])
            etr_content.append(line)

            for awi_index, awi_row in f_awi_df.iterrows():
                heading_line = self.make_markdown_heading(4, "Audit action " + str(awi_row[c5settings.ETR_EVAL_AWI_ID_COL]) + " in category " + awi_row[c5settings.ETR_EVAL_AWI_CATEGORY_COL])
                etr_content.append(heading_line)
                line = self.make_markdown_line(awi_row[c5settings.ETR_EVAL_AWI_DESCRIPTION_COL])
                etr_content.append(line)
                # line = make_markdown_line(awi_row['AWI-Cat'])
                # etr_content.append(line)

                heading_line = self.make_markdown_heading(5, "Evaluation scope and evidence")
                etr_content.append(heading_line)
                line = self.make_markdown_line("Scope of evaluation: **{0}**".format(awi_row[c5settings.ETR_EVAL_AWI_EVAL_OBJECT_COL]))
                etr_content.append(line)

                heading_line = self.make_markdown_heading(6, "Evidence required from developer or sponsor")
                etr_content.append(heading_line)
                line = self.make_markdown_line("The following pieces of evidence are required from the developer or sponsor:")
                etr_content.append(line)
                line = self.make_markdown_line(awi_row[c5settings.ETR_EVAL_AWI_REQUIRED_INPUT_COL])
                etr_content.append(line)

                heading_line = self.make_markdown_heading(6, "Input provided by the developer")
                etr_content.append(heading_line)
                # line = make_markdown_line("Input provided by the developer: \n")
                # INI-ivs: append text to the output
                # etr_content.append(line)
                # FIN-ivs
                line = self.make_markdown_line(awi_row[c5settings.ETR_EVAL_AWI_DEV_INPUT_COL])
                etr_content.append(line)

                heading_line = self.make_markdown_heading(5, "Analysis and assessment outcome")
                etr_content.append(heading_line)
                line = self.make_markdown_line(awi_row[c5settings.ETR_EVAL_AWI_ANALYSIS_COL])
                etr_content.append(line)

                # INI-ivs: modify text
                # heading_line = self.make_markdown_heading(5, "Assessment outcome")
                # FIN-ivs
                # etr_content.append(heading_line)
                line = self.make_markdown_line(awi_row[c5settings.ETR_EVAL_AWI_VERDICT_COL])
                etr_content = self.add_markdown_verdict("Audit action verdict", awi_row[c5settings.ETR_EVAL_AWI_VERDICT_COL], etr_content)

            heading_line = self.make_markdown_heading(4, "Verdict")
            etr_content.append(heading_line)
            etr_content = self.add_markdown_verdict("Work unit verdict", row[c5settings.ETR_EVAL_WU_VERDICT_COL], etr_content)

        for r in etr_content:
            writer.write(r)

        writer.close()

    def make_markdown_heading(self, heading_lvl=2, txt=""):
        # INI-ivs: add newline
        line = str("#"*heading_lvl) + " " + str(txt) + "\n\n"
        # FIN-ivs
        return line

    def make_markdown_line(self, content):
        # INI-ivs: add newline
        line = str(content) + "\n\n"
        # FIN-ivs
        return line

    def add_markdown_verdict(self, title, content, original_text_list):
        verdict_content = original_text_list
        
        # INI-ivs: remove one newline at the beginning
        line = "\n" + ':::{{.callout-note title=\"{0}\"}}'.format(title) + "\n"
        # FIN-ivs
        verdict_content.append(line)
        color = "black"
        if content == "Pass":
            color = "pass"
        elif content == "Fail":
            color = "fail"
        elif content == "Inconclusive":
            color = "inclsv"
        # color_attrib = "{{style=\"color:{0};\"}}".format(color)
        # line = "[{0}]{1}".format(content,color_attrib) + "\n"
        line = '\\{0}{1}{2}{3}'.format(color,"{",content,"}") + "\n"
        verdict_content.append(line)
        line = ":::" + "\n\n"
        verdict_content.append(line)

        return verdict_content

    def dataframe_to_markdown(self, df):
        markdown = df.to_markdown(index=False)
        return markdown

    def dataframe_to_markdown_file(self, df, output_name):
        df_in_markdown = self.dataframe_to_markdown(df)

        output_file_path = os.path.join(self.output_folder_path, output_name + "-" + self.etr_table_export_file_name)
        table_writer = open(output_file_path, 'w+')
        table_writer.write(df_in_markdown)
        table_writer.close()

    def spreadsheet_table_to_markdown_table(self, input_file_path, sheet_number, output_name):
        df = pd.read_excel(input_file_path, sheet_name=sheet_number)
        self.dataframe_to_markdown_file(df, output_name)

    def generate_etr(self, family_list=["CMC"], tables_list=["DocStruct"]):
        if family_list is None:
            family_list = ["CMC"]
        for cc_family in family_list:
            try:
                self.family_wu_to_etr(cc_family)
                print("ETR parts created in: {}".format(os.path.join(c5settings.ASSETS_FOLDER_NAME, c5settings.ETR_FOLDER_NAME, c5settings.ETR_OUTPUT_FOLDER_NAME)))
            except Exception as e:
                print(e)
        
        tables_input_file_path = os.path.join(c5settings.ASSETS_FOLDER_NAME, c5settings.ETR_FOLDER_NAME, c5settings.ETR_TABLES_FILE_NAME)
        if tables_list is None:
            tables_list = ["DocStruct", "Acronyms", "Glossary"]

        for table in tables_list:
            try:
                self.spreadsheet_table_to_markdown_table(tables_input_file_path, table, table)
            except Exception as e:
                print(e)

"""End: CLI methods"""
