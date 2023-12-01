"""Settings for the C5-DEC package."""

import logging
import os

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
ASSETS_FOLDER_NAME = "assets"
STARTUP_CONFIG_JSON_PATH = ASSETS_FOLDER_NAME+"/config.json"
TRANSLATION_ASSETS_FOLDER_PATH = ASSETS_FOLDER_NAME+"/translations"
PERSON_ACRONYMS_FILE_PATH = ASSETS_FOLDER_NAME+"/acronyms/persons.json"
ACRONYMS_FOLDER_PATH = ASSETS_FOLDER_NAME+"/acronyms/"
OPENPROJECT_PARAMS_CSV_FILE_PATH = ASSETS_FOLDER_NAME+"/tshparams/openproject_params.csv"
TSHFORMAT_JSON_FILE_PATH = ASSETS_FOLDER_NAME+"/tshparams/tshformat.json"
EXPORT_FOLDER = os.getcwd()

feature_flags = {"ssdlc": True, "cct": True, "cryptography": True, "cpssec": True, "isms": True, "pm": True, "transformer": True, "settings": False}

CC_VERSION_TO_PATH = {
    "3R1": ASSETS_FOLDER_NAME + "/database/SecurityControls/cc3R1.xml",
    "3R2": ASSETS_FOLDER_NAME + "/database/SecurityControls/cc3R2.xml",
    "3R3": ASSETS_FOLDER_NAME + "/database/SecurityControls/cc3R3.xml",
    "3R4": ASSETS_FOLDER_NAME + "/database/SecurityControls/cc3R4.xml",
    "3R5": ASSETS_FOLDER_NAME + "/database/SecurityControls/cc3R5.xml"
}
CCDTD_FILE_PATH = ASSETS_FOLDER_NAME+"/database/SecurityControls/cc3r5.dtd"
EVALLIST_JSON_PATH = ASSETS_FOLDER_NAME+"/database/eval.json"
EXPORT_FOLDER = os.getcwd()

# Project parameters
PROJECT_ROOT = None

LOG_FILE = "rem.log"

DEFAULT_PROJECT_FOLDER_PATH = os.path.join(os.getcwd(), "default-rem-folder")

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

ROOT_REPO_NAME = "REQ"
ROOT_REPO_FOLDER_NAME = "reqs"

DOORSTOP_YAML = ".doorstop.yml"
