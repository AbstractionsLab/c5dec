"""CLI command functions."""

# CLI design is based on that of Doorstop

import os, sys, tempfile
import time
import subprocess
from typing import Set

import c5dec.frontend.tui.main as tui
from c5dec import common
import c5dec.settings as c5settings
import c5dec.core.ssdlc as ssdlc
import c5dec.core.pm as pm
from datetime import datetime
import c5dec.core.cct as cct

log = common.logger(__name__)

def open_editor(editor, filepath):
    if not editor:
        EDITOR = c5settings.DEFAULT_EDITOR
    else:
        EDITOR = os.environ.get('EDITOR', editor)

    if EDITOR in ['vim', 'nano']:
        with open(filepath, "r") as file:
            initial = file.read()

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            tf.write(bytes(initial, 'utf--8'))
            tf.flush()
            subprocess.run([EDITOR, tf.name])
            tf.seek(0)
            edited = tf.read()
            
        if edited.decode('utf-8') != initial:
            with open(filepath, "w") as file:
                file.write(edited.decode('utf-8'))
            info_msg = "File successfully saved." 
            log.info(info_msg)
    else:
        try:
            subprocess.run([EDITOR, "-r", filepath], check=True,
            stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        except subprocess.CalledProcessError as e:
            log.error(f"{e}")
        except FileNotFoundError:
            log.error(f"Editor {EDITOR} not found.")

def get(name):
    """Get a command function by name."""
    if name:
        log.debug("running command '{}'...".format(name))
        return globals()["run_" + name]
    else:
        log.debug("launching main command...")
        return run
    
def run(args, cwd, error, catch=True):  # pylint: disable=W0613
    """Process arguments and run the `c5dec` subcommand.

    :param args: Namespace of CLI arguments
    :param cwd: current working directory
    :param error: function to call for CLI errors
    :param catch: catch and log :class:`~c5dec.common.c5decError`

    """
    tui.main(args, cwd)
    return True

def run_exportoptime(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.input_file_path = args.path
    timerep_assistant.convert_openproject_time_report_to_IAL_format()

def run_consolidate(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.set_tsh_folder_path(args.path)
    date_format = '%d-%m-%Y'
    if args.filter == None:
        timerep_assistant.set_timerep_parameters(source_folder=args.path,apply_filters=False)
    else:
        timerep_assistant.set_timerep_parameters(source_folder=args.path, apply_filters=True, 
                                             from_date=datetime.strptime(args.fromdate, date_format), 
                                             to_date=datetime.strptime(args.to, date_format),
                                             filter_field=args.field,
                                             filter_field_value=args.value)
    timerep_assistant.consolidate_timesheets()

# This function is no longer used and should be removed
# @deprecated
def run_retrieveattr(args, cwd, _, catch=True):
    ssdlc.get_respository_attributes(args.prefix)
    timerep_assistant.consolidate_timesheets()

def run_view(args, cwd, _, catch=True):
    if args.verbose:
        cct.get_item(args.id, args.version)
    else:
        cct.get_item(args.id, args.version, silence=True)

def run_validate(args, cwd, _, catch=True):
    if args.verbose:
        cct.validate(args.id, args.version, mode=args.mode)
    else:
        cct.validate(args.id, args.version, mode=args.mode, silence=True)

def run_checklist(args, cwd, _, catch=True):
    if args.create:
        if args.info:
            info_dict = {k: v for k, v in (item.split('=') for item in args.info)}
        else:
            info_dict = {"GeneralInfo": f"{args.version or '3R5'}"}
        cct.CLIChecklistHandler().create(args.version, args.id, args.prefix, info=info_dict)
    if args.list:
        cct.CLIChecklistHandler().list(args.prefix)
    if args.update:
        cct.CLIChecklistHandler().update(args.prefix)
    if args.validate:
        cct.CLIChecklistHandler().validate(args.prefix)
    if args.status:
        cct.CLIChecklistHandler().status(args.prefix)
    if args.edit:
        item = args.edit
        abs_item_path = cct.CLIChecklistHandler().edit(args.prefix, item)
        if abs_item_path:
            rel_item_path = os.path.relpath(abs_item_path, cwd)
            open_editor(args.editor, rel_item_path)
    if args.publish:
        path = os.path.abspath(os.path.join(cwd, args.publish))
        cct.CLIChecklistHandler().publish(args.prefix, path)