# CLI design is based on that of Doorstop

import argparse
import os
import sys
import doorstop

from c5dec import common, settings
from c5dec.frontend.cli import commands
from c5dec.frontend.cli import utils

log = common.logger(__name__)


def run(args=None):
    """Process command-line arguments and run the program."""
    from c5dec import CLI, DESCRIPTION, VERSION

    # Shared options
    project = argparse.ArgumentParser(add_help=False)
    try:
        root = doorstop.builder.vcs.find_root(os.getcwd())
    except doorstop.common.DoorstopError:
        root = None
    project.add_argument(
        "-j",
        "--project",
        metavar="PATH",
        help="set the path to the root of the project",
        default=root,
    )
    settings.PROJECT_ROOT = root

    debug = argparse.ArgumentParser(add_help=False)
    debug.add_argument("-V", "--version", action="version", version=VERSION)
    group = debug.add_mutually_exclusive_group()
    group.add_argument(
        "-v", "--verbose", action="count", default=0, help="enable verbose logging"
    )

    shared = {
        "formatter_class": common.HelpFormatter,
        "parents": [project, debug],
    }

    # Build main parser
    parser = argparse.ArgumentParser(
        prog=CLI, description=DESCRIPTION, **shared)
    
    parser.add_argument(
        "-t",
        "--tui",
        action="store_true",
        help="run the textual user interface",
    )
    
    # Build sub-parsers
    subs = parser.add_subparsers(help="", dest="command", metavar="<command>")
    _transformrep(subs)
    _consolidate(subs)
    _retrieveattr(subs)
    _view(subs)
    _validate(subs)
    _checklist(subs)

    # Parse arguments
    args = parser.parse_args(args=args)

    # Configure logging
    utils.configure_logging(args.verbose)

     # Run the program
    function = commands.get(args.command)
    try:
        success = function(args, os.getcwd(), parser.error)
    except common.C5decError as exc:
        log.error(exc)
        success = False
    except KeyboardInterrupt:
        log.debug("command cancelled")
        success = False
    if success:
        log.debug("command succeeded")
    else:
        log.debug("command failed")
        sys.exit(1)

@common.feature_flag("ON")
def _transformrep(subs):
    info = "Invoke the OpenProject time report conversion command"
    sub = subs.add_parser(
        "transformrep", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("path", help="path to OpenProject time report")

@common.feature_flag("ON")
def _consolidate(subs):
    info = "Invoke the time report consolidation command"
    sub = subs.add_parser(
        "consolidate", description=info.capitalize() + ".", help=info
    )
    sub.add_argument("path", help="path to directory containing time reports")
    sub.add_argument("-l", "--filter", help="apply filters to the consolidated report")
    sub.add_argument("-f", "--fromdate", help="starting from date, i.e., entries having date after this input")
    sub.add_argument("-t", "--to", help="up to date, i.e., entries having date before this input")
    sub.add_argument("-d", "--field", help="Field name to filter for, e.g., Domain")
    sub.add_argument("-v", "--value", help="Field value to filter for, e.g., RD")

@common.feature_flag("OFF")
def _retrieveattr(subs):
    """Configure the `c5dec attribute retrieval` subparser."""
    info = "Invoke the attributes retrieval command from the SSDLC module"
    sub = subs.add_parser(
        "retrieveattr", description=info.capitalize() + ".", help=info)
    sub.add_argument("prefix", help="prefix of artifact repository")

def add_common_args(sub):
    versions_supported = ["3R1", "3R2", "3R3", "3R4", "3R5"]
    sub.add_argument("-v", "--verbose", action="store_true")
    sub.add_argument("--version",
                     help=f"Specify the Common Criteria (CC) version: {versions_supported}")

def _view(subs):
    info = "Retrieve CC item with id or name."
    sub = subs.add_parser(
        "view", description=info.capitalize() + ".", help=info)
    sub.add_argument("id", help="CC item ID. Case insensitive.")
    add_common_args(sub)

def _validate(subs):
    info = "CC validation interface."
    sub = subs.add_parser(
        "validate", description=info.capitalize() + ".", help=info)
    sub.add_argument("id", help="List of CC component IDs.", nargs="+")
    sub.add_argument("-d", "--dependency", action="store_const", const="dep", dest="mode",
                     help="Validate Component List for dependencies.")
    add_common_args(sub)

def _checklist(subs):
    info = "Evaluation Checklist"
    sub = subs.add_parser(
        "checklist", description=f"{info.capitalize()}. NOTE: the <prefix> must appear before the options: c5dec checklist prefix [options]" + ".", help=info)
    sub.add_argument("prefix", help="The identifier/name of the checklist, used as a prefix to name its components.")

    group = sub.add_mutually_exclusive_group()
    group.add_argument("-c", "--create", action="store_true", 
                    help="Create evaluation checklist from component and/or package IDs.")
    group.add_argument("-l", "--list", const=True, default=False,
                    help="List all available checklists.", nargs="?")
    group.add_argument("--edit", help="Edit Work Unit.")
    group.add_argument("-u", "--update", action="store_true",
                       help="Update Evaluation Checklist.")
    group.add_argument("--validate", action="store_true",
                       help="Validate Evaluation Checklist.")
    group.add_argument("-s", "--status", action="store_true",
                       help="Retrieve the status of Evaluation Checklist.")
    group.add_argument("--publish", help="Publish Evaluation Checklist to path.")

    sub.add_argument("--id", help="List of Component IDs", 
                    required='-c' in sys.argv or '--create' in sys.argv, nargs="+")
    sub.add_argument("--info", help="General Information of Evaluation Project.", nargs="+")
    sub.add_argument("--editor", help="Set editor. Defaults to 'vim'.")
