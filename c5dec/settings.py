"""Settings for the C5-DEC package."""

import logging
import os
import yaml
import pathlib

# Constants

PROJECT_ROOT_PATH = pathlib.Path(os.path.abspath(os.path.join(__file__, ".."))).parent.absolute()

ASSETS_FOLDER_NAME = "assets"
DB_FOLDER_NAME = "database"
ETR_FOLDER_NAME = "etr"
DOCS_FOLDER_NAME = "docs"
SPECS_FOLDER_NAME = "specs"
INPUT_FOLDER_NAME = "input"
EXPORT_FOLDER_NAME = "export"
PUBLISH_FOLDER_NAME = "publish"
SEC_CONTROLS_FOLDER_NAME = "SecurityControls"
ACRONYMS_FOLDER_NAME = "acronyms"
TRANSLATIONS_FOLDER_NAME = "translations"
STARTUP_CONFIG_FILE_NAME = "config.json"
PERSONS_FILE_NAME = "persons.json"
TSH_FORMAT_FILE_NAME = "tshformat.json"
RMT_PARAMS_FILE_NAME = "rmt-params.xlsx"
TSH_PARAMS_FOLDER_NAME = "tshparams"
OPENPROJECT_PARAMS_FILE_NAME = "openproject_params.csv"

ETR_OUTPUT_FOLDER_NAME = "output"

# global EXECUTION_MODE
EXECUTION_MODE = "CLI" # CLI, TUI, GUI
c5params_dictionary = None
c5dec_params_read = False

C5DEC_PARAMS_FILE_NAME = "c5dec_params.yml"
dirname = os.path.dirname(__file__)
C5DEC_PARAMS_FILE_PATH = os.path.join(dirname, ASSETS_FOLDER_NAME, C5DEC_PARAMS_FILE_NAME)
with open(C5DEC_PARAMS_FILE_PATH, 'r') as file:
    try:
        c5params_dictionary = yaml.safe_load(file)
        c5dec_params_read = True
    except yaml.YAMLError as exc:
        c5dec_params_read = False
        print(exc)

# ETR work unit ID
# if c5dec_params_read:
ETR_EVAL_CHECKLIST_DEFAULT_FILE_NAME = "etr-eval-checklist"
ETR_EVAL_CHECKLIST_FILE_NAME = c5params_dictionary.get('etr').get('eval-file-name')
ETR_EVAL_WU_ID_COL = c5params_dictionary.get('etr').get('eval-wu-id')
ETR_EVAL_WU_SHEET_NAME = c5params_dictionary.get('etr').get('eval-wu-sheet') 
ETR_EVAL_AWI_SHEET_NAME = c5params_dictionary.get('etr').get('eval-awi-sheet')
ETR_EVAL_FAMILY_COL = "Family"
# ETR_EVAL_WU_DESCRIPTION_COL = "WU-Desc"
ETR_EVAL_WU_DESCRIPTION_COL = "text"
# ETR_EVAL_WU_ID_COL = "WU-ID"
ETR_EVAL_WU_ID_COL = "header"
ETR_EVAL_AWI_ID_COL = "AWI-ID"
ETR_EVAL_AWI_DESCRIPTION_COL = "AWI-Descr"
ETR_EVAL_AWI_CATEGORY_COL = "AWI-Cat"
ETR_EVAL_AWI_EVAL_OBJECT_COL = "AWI-EvalObj"
ETR_EVAL_AWI_REQUIRED_INPUT_COL = "RequiredInput"
ETR_EVAL_AWI_DEV_INPUT_COL = "DevInput"
ETR_EVAL_AWI_ANALYSIS_COL = "Analysis"
ETR_EVAL_WU_VERDICT_COL = "verdict"
ETR_EVAL_AWI_VERDICT_COL = "Verdict"
ETR_ACRONYMS_GLOSSARY_FILE_NAME = "acronyms-glossary.xlsx"
ETR_TABLES_FILE_NAME = "etr-tables.xlsx"


# Logging settings
DEFAULT_LOGGING_FORMAT = "%(message)s"
LEVELED_LOGGING_FORMAT = "%(levelname)s: %(message)s"
VERBOSE_LOGGING_FORMAT = "[%(levelname)-8s] %(message)s"
VERBOSE2_LOGGING_FORMAT = "[%(levelname)-8s] (%(name)s @%(lineno)4d) %(message)s"
QUIET_LOGGING_LEVEL = logging.WARNING
TIMED_LOGGING_FORMAT = "%(asctime)s" + " " + VERBOSE_LOGGING_FORMAT
DEFAULT_LOGGING_LEVEL = logging.WARNING
VERBOSE_LOGGING_LEVEL = logging.INFO
VERBOSE2_LOGGING_LEVEL = logging.DEBUG
VERBOSE3_LOGGING_LEVEL = logging.DEBUG - 1

# Application configurations

dirname = os.path.dirname(__file__)

STARTUP_CONFIG_JSON_PATH = os.path.join(ASSETS_FOLDER_NAME, STARTUP_CONFIG_FILE_NAME)
TRANSLATION_ASSETS_FOLDER_PATH = os.path.join(ASSETS_FOLDER_NAME, TRANSLATIONS_FOLDER_NAME)
PERSON_ACRONYMS_FILE_PATH = os.path.join(ASSETS_FOLDER_NAME, ACRONYMS_FOLDER_NAME, PERSONS_FILE_NAME)
ACRONYMS_FOLDER_PATH = os.path.join(ASSETS_FOLDER_NAME, ACRONYMS_FOLDER_NAME)
OPENPROJECT_PARAMS_CSV_FILE_PATH = os.path.join(ASSETS_FOLDER_NAME, TSH_PARAMS_FOLDER_NAME, OPENPROJECT_PARAMS_FILE_NAME )
TSHFORMAT_JSON_FILE_PATH = os.path.join(dirname, ASSETS_FOLDER_NAME, TSH_PARAMS_FOLDER_NAME, TSH_FORMAT_FILE_NAME)
RMT_PARAMS_FILE_PATH = os.path.join(dirname, ASSETS_FOLDER_NAME, TSH_PARAMS_FOLDER_NAME, RMT_PARAMS_FILE_NAME) 

SPECS_FOLDER_PATH = os.path.join(PROJECT_ROOT_PATH, DOCS_FOLDER_NAME, SPECS_FOLDER_NAME)
PUBLISH_FOLDER_PATH = os.path.join(os.getcwd(), DOCS_FOLDER_NAME, PUBLISH_FOLDER_NAME)
EXPORT_FOLDER = os.path.join(os.getcwd(), EXPORT_FOLDER_NAME)
HTML_INDEX_FILENAME = "index.html"
DOORSTOP_FOLDER_NAME = "doorstop"
DOORSTOP_CSS_FILENAME = "sidebar.css"

feature_flags = {"ssdlc": True, "cct": True, "cryptography": True, "cpssec": True, "isms": True, "pm": True, "transformer": True, "settings": False}

CC_VERSION_TO_PATH = {
    "3R1": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3R1.xml"),
    "3R2": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3R2.xml"),
    "3R3": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3R3.xml"),
    "3R4": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3R4.xml"),
    "3R5": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3R5.xml"),
    "2022R1": os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc2022.xml")
}

SELECTED_CC_VERSION = c5params_dictionary.get('cc').get('release') 


CCDTD_FILE_PATH = os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc3r5.dtd")
CC2022DTD_FILE_PATH = os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, SEC_CONTROLS_FOLDER_NAME, "cc2022.dtd")
EVALLIST_JSON_PATH = os.path.join(ASSETS_FOLDER_NAME, DB_FOLDER_NAME, "eval.json")


# Project parameters
PROJECT_ROOT = None

LOG_FILE = "c5dec.log"
CCT_LOG_FILE = "cct.log"
CCTAPP_LOG_FILE = "cctapp.log"
PM_LOG_FILE = "pm.log"
CMD_LOG_FILE = "cmd.log"

# Doorstop defaults
DOORSTOP_ROOT = "MRS"
DEFAULT_SEPARATOR = "-"
DEFAULT_DIGITS = 3
DEFAULT_ITEMFORMAT = "markdown"
DEFAULT_EDITOR = "vim"

DEFAULT_EVALUATION_ATTRIBUTES = {'component' : '',
                                 'element' : '',
                                 'element_description' : '',
                                 'dc_element' : '',
                                 'dc_element_description' : '',
                                 'evidence' : '',
                                 'evaluator' : '',
                                 'evaluation_date' : '',
                                 'verdict': 'inconclusive'}
DEFAULT_PUBLISH_ATTRIBUTES = {'component' : '',
                              'element' : '',
                              'dc_element' : '',
                              'evidence' : '',
                              'evaluator' : '',
                              'evaluation_date' : '',
                              'verdict': 'inconclusive'}
                              
DEFAULT_EVALUATION_REVIEWED = ['evidence', 'verdict', 'evaluator', 'evaluation_date']

DOORSTOP_YAML = ".doorstop.yml"