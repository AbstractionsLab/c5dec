"""Package for c5dec."""

from pprint import pprint
import sys, os

from pkg_resources import DistributionNotFound, get_distribution
from doorstop import DoorstopError, DoorstopInfo, DoorstopWarning
from c5dec.core import (
    cpssa,
    ssdlc,
    cryptography,
    cct,
    isms,
    pm,
    transformer
)

__project__ = "C5-DEC"


script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, '.')
sys.path.append(mymodule_dir)
# pprint(sys.path)

try:
    __version__ = get_distribution(__project__).version
except DistributionNotFound:
    __version__ = "(local)"

CLI = "c5dec"
TUI = "c5dec-tui"
VERSION = "{0} v{1}".format(__project__, __version__)
DESCRIPTION = "C5-DEC CAD for Computer-Assisted Design and Development."