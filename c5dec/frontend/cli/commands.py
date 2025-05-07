"""CLI command functions."""

# CLI design is based on that of Doorstop

import os, sys, tempfile
import time
import subprocess
from typing import Set

import c5dec.frontend.tui.main as tui
import c5dec.frontend.gui.app as gui
from c5dec import common
import c5dec.settings as c5settings
import c5dec.core.ssdlc as ssdlc
import c5dec.core.pm as pm
from datetime import datetime
import c5dec.core.cct as cct
import c5dec.psi.search as c5search
import c5dec.core.transformer as transformer
from docx.opc.exceptions import PackageNotFoundError

log = common.logger(__name__)
log.setLevel(common.logging.INFO)

logHandler = common.logging.FileHandler(c5settings.CMD_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

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
    if args.gui:
        gui.main(args, cwd)
    else:
        tui.main(args, cwd)
    return True

def run_new(args, cwd, _, catch=True):
    ssdlc.create_new_c5dec_project(project=args.project, user=args.user) 

def run_timerep(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.input_file_name = args.name
    try:
        timerep_assistant.convert_openproject_time_report_to_IAL_format()
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e))

def run_consolidate(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.set_tsh_folder_name(args.name)
    date_format = '%d-%m-%Y'
    if args.filter == None:
        timerep_assistant.set_timerep_parameters(source_folder=args.name,apply_filters=False)
    else:
        timerep_assistant.set_timerep_parameters(source_folder=args.name, apply_filters=True, 
                                            from_date=datetime.strptime(args.fromdate, date_format), 
                                            to_date=datetime.strptime(args.to, date_format),
                                            filter_field=args.field,
                                            filter_field_value=args.value)
    try:
        timerep_assistant.consolidate_timesheets()
    except IOError:
        log.error("Missing or bad arguments.")
    except PackageNotFoundError:
        log.error("No xlsx file found at the provided path.")
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e))


def run_costrep(args, cwd, _, catch=True):
    timerep_assistant = pm.TimeReportAssistant()
    timerep_assistant.input_file_name = args.name
    try:
        timerep_assistant.compute_cost_report()
    except Exception as e:
        log.error("Something unexpected went wrong: {}".format(e)) 

# This function is no longer used and should be removed
# @deprecated
def run_retrieveattr(args, cwd, _, catch=True):
    ssdlc.get_respository_attributes(args.prefix)

def run_view(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
    if args.verbose:
        cct.get_item(args.id, args.version)
    else:
        cct.get_item(args.id, args.version, silence=True)

def run_validate(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
    if args.verbose:
        cct.validate(args.id, args.version, mode=args.mode)
    else:
        cct.validate(args.id, args.version, mode=args.mode, silence=True)

def run_checklist(args, cwd, _, catch=True):
    c5settings.SELECTED_CC_VERSION = args.version
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

def run_search(args, cwd, _, catch=True, **kwargs):
    c5search.retrieve_by_xpath(c5settings.CC_VERSION_TO_PATH.get("2022R1"), c5settings.CC2022DTD_FILE_PATH)

def run_export(args, cwd, _, catch=True, **kwargs):
    c5settings.SELECTED_CC_VERSION = args.version
    print(c5settings.SELECTED_CC_VERSION)
    try:
        cct.ChecklistBuilder(checklist_name=args.name, cc_version=args.version).export_eval_checklist(class_id_vector=args.classes, component_id_vector=args.components)
    except Exception as e:
        print(e)

def run_etr(args, cwd, _, catch=True, **kwargs):
    if args.name is None:
        cct.ETR().generate_etr(family_list=args.families, tables_list=args.tables)
    else:
        cct.ETR(checklist_name=args.name).generate_etr(family_list=args.families, tables_list=args.tables)

# def run_publish(args, cwd, _, catch=True, **kwargs):
#     if args.directory is None:
#         print(f"Please specify an input directory. See c5dec publish -h for more information.")
#         return
#     if args.format is None:
#         transformer.publish(format=".html", name=args.directory)
#     else:    
#         transformer.publish(format=args.format, name=args.directory)

def run_transform(args, cwd, _, catch=True, **kwargs):
    print("---")
    print("Open C5-DEC CAD dev container in VS Code or run session (./c5dec.sh session) to use the commands below:")
    print("To import, try: doorstop import -h")
    print("To export, try: doorstop export -h")
    print("To render, use: quarto render -h")
    print("To convert, use: quarto pandoc -h")
    print("---")
    print("Also see Transformer page in user manual:")
    print("c5dec/docs/manual/transformer.md OR https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/transformer.md")

def run_cpssa(args, cwd, _, catch=True, **kwargs):
    print("---")
    print("OpenTRICK: https://github.com/itrust-consulting/OpenTRICK")
    print("Threagile: https://github.com/Threagile/threagile")
    print("ADTool: https://github.com/tahti/ADTool2")
    print("Threat Dragon: https://github.com/OWASP/threat-dragon")
    print("Capella Darc Viewpoint: https://github.com/eclipse-capella/capella-cybersecurity/wiki")
    print("Capella: https://github.com/eclipse-capella/capella")
    print("---")
    print("See CPSSA page in user manual:")
    print("c5dec/docs/manual/cpssa.md OR https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/cpssa.md")

def run_crypto(args, cwd, _, catch=True, **kwargs):
    print("---")
    print("Open C5-DEC CAD dev container in VS Code or run session (./c5dec.sh session) to use the commands below:")
    print("For GnuPG, try: gpg -h")
    print("For encryption and signing, try: kryptor -h")
    print("For secure cloud storage, try: cryptomator -h")
    print("For PQC, use C5-DEC cryptography dev container: ./c5dec.sh pqc (or reopen container in VS Code)")
    print("---")
    print("Also see Cryptography page in user manual for PQC:")
    print("c5dec/docs/manual/cryptography.md OR https://github.com/AbstractionsLab/c5dec/blob/main/docs/manual/cryptography.md")