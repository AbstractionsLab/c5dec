"""Common exceptions, classes, and functions for C5-DEC."""

import argparse
import logging
import os
import json
import functools

import c5dec.settings as c5settings
import doorstop

verbosity = 0  # global verbosity setting for controlling string formatting
PRINT_VERBOSITY = 0  # minimum verbosity to using `print`
STR_VERBOSITY = 3  # minimum verbosity to use verbose `__str__`
MAX_VERBOSITY = 4  # maximum verbosity level implemented


def _trace(self, message, *args, **kws):
    if self.isEnabledFor(logging.DEBUG - 1):
        self._log(logging.DEBUG - 1, message, args, **kws)  # pylint: disable=W0212


logging.addLevelName(logging.DEBUG - 1, "TRACE")  # add new logging level
logging.Logger.trace = _trace  # type: ignore
# logging.basicConfig(filename='error.log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger
log = logger(__name__)


class HelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Command-line help text formatter with wider help text."""

    def __init__(self, *args, **kwargs):
        kwargs["max_help_position"] = 40
        super().__init__(*args, **kwargs)

def read_line_from_file(path):
    first_line = ""
    with open(path, "r") as f:
        first_line = f.readline()
    return first_line

def get_value_from_json(key, default_value):
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

def feature_flag(flag):
    def decorator_feature_flag(func):
        @functools.wraps(func)
        def wrapper_decorator_feature_flag(*args, **kwargs):
            if flag == "ON":
                func(*args, **kwargs)

        return wrapper_decorator_feature_flag

    return decorator_feature_flag

def create_dirname(path):
    """Ensure a parent directory exists for a path."""
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.isdir(dirpath):
        log.info("creating directory {}...".format(dirpath))
        os.makedirs(dirpath)

# exception classes ##########################################################


class C5decError(Exception):
    """Generic c5dec error."""

class C5decWarning(C5decError, Warning):
    """Generic c5dec warning."""

class C5decInfo(C5decWarning, Warning):
    """Generic c5dec info."""

class Capture:  # pylint: disable=R0903
    """Context manager to catch :class:`~doorstop.common.DoorstopError` and
    :class:`~c5dec.common.C5decError`."""

    def __init__(self, catch=True):
        self.catch = catch
        self._success = True

    def __bool__(self):
        return self._success

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and (issubclass(exc_type, doorstop.DoorstopError) or issubclass(exc_type, C5decError)):
            self._success = False
            if self.catch:
                log.error(exc_value)
                return True
        return False


# Logging classes #################

class WarningFormatter(logging.Formatter):
    """Logging formatter that displays verbose formatting for WARNING+."""

    def __init__(self, default_format, verbose_format, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_format = default_format
        self.verbose_format = verbose_format

    def format(self, record):
        """Python 3 hack to change the formatting style dynamically."""
        if record.levelno > logging.INFO:
            self._style._fmt = self.verbose_format  # pylint: disable=W0212
        else:
            self._style._fmt = self.default_format  # pylint: disable=W0212
        return super().format(record)
