import doorstop
import os
import c5dec.settings as c5settings
import c5dec.common as common
import time
import re
import shutil
import zipfile
import warnings

log = common.logger(__name__)

warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

log.setLevel(common.logging.INFO)

logHandler = common.logging.FileHandler(c5settings.PM_LOG_FILE, mode='a')
formatter = common.logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s() : %(message)s", "%Y-%m-%d %H:%M:%S")
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

project_root = c5settings.PROJECT_ROOT

def import_ssdlc_document(path, prefix, format):
    tree = doorstop.build()
    document = tree.find_document(prefix)
    doorstop.importer.import_file(path, document, format)

def export_ssdlc_document(label, path=None, format=".yml") -> str:
    tree = doorstop.build()
    if label != "all":
        document = tree.find_document(label)
        current_time = time.strftime("%Y%m%d-%H%M%S")
        if path is None:
            path = "{}/{}-export-{}{}".format(c5settings.EXPORT_FOLDER, label, current_time, format)
        doorstop.exporter.export(document, path, format)
    else:
        if path is None:
            path = "./export"
            common.create_dirname(path)
        doorstop.exporter.export(tree, path, format)
    return path

def publish_ssdlc_document(prefix, path=None, format="html"):
    tree = doorstop.build()
    if prefix != "all":
        document = tree.find_document(prefix)
        current_time = time.strftime("%Y%m%d-%H%M%S")
        if path is None:
            path = "{}/{}-publish-{}{}".format(c5settings.EXPORT_FOLDER, prefix, current_time, format)
        doorstop.publisher.publish(document, path, format)
    else:
        if path is None:
            path = "./export"
            common.create_dirname(path)
        doorstop.publisher.publish(tree, path, format)
    return path

def publish(prefix="all", path=None, format=None, name=None):
    # Archive the entire content of the docs/specs folder
    specs_folder = os.path.join(c5settings.PROJECT_ROOT, 'docs', 'specs')
    archive_path = os.path.join(c5settings.PROJECT_ROOT, 'docs', 'c5dec-specs.zip')
    if os.path.exists(specs_folder):
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(specs_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, specs_folder)
                    zipf.write(file_path, arcname)
        log.info(f"Archived specs folder to {archive_path}")

        # Delete the specs folder
        shutil.rmtree(specs_folder)
        log.info(f"Deleted specs folder at {specs_folder}")
    else:
        log.warning(f"Specs folder {specs_folder} does not exist.")

    # Copy the folder from assets/input to the root of the project folder
    # input_folder = os.path.join(c5settings.PROJECT_ROOT, 'c5dec', 'input', name)
    # destination_folder = os.path.join(c5settings.PROJECT_ROOT, name)
    # if os.path.exists(input_folder):
    #     shutil.copytree(input_folder, destination_folder)
    #     log.info(f"Copied {input_folder} to {destination_folder}")
    # else:
    #     log.error(f"Input folder {input_folder} does not exist.")

    try:
        tree = doorstop.build()
        if format is None:
            format = ".md"
        if prefix != "all":
            document = tree.find_document(prefix)
            current_time = time.strftime("%Y%m%d-%H%M%S")
            if path is None:
                path = "{}/{}-publish-{}{}".format(c5settings.EXPORT_FOLDER, prefix, current_time, format)
            doorstop.publisher.publish(document, path, format)
        else:
            if path is None:
                path = c5settings.PUBLISH_FOLDER_PATH
                common.create_dirname(path)
            doorstop.publisher.publish(tree, path, format)

        # Replace css refs in index.html
        if format == ".html":
            with open(os.path.join(c5settings.PUBLISH_FOLDER_PATH, c5settings.HTML_INDEX_FILENAME), 'r') as source_file:
                try:
                    input = source_file.read()

                except Exception as e:
                    print(e)
                
                target = open(os.path.join(c5settings.PUBLISH_FOLDER_PATH, c5settings.HTML_INDEX_FILENAME), "w")
                new_head = """<head>
                            <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                            <link rel="stylesheet" href="assets/doorstop/bootstrap.min.css" />
                            <link rel="stylesheet" href="assets/doorstop/general.css" />
                            </head>"""
                new_content = re.sub(r'<head>.*?</head>', new_head, input, flags=re.DOTALL)
                new_content = re.sub(r'<table>', '<table class="table table-striped table-condensed">', new_content, flags=re.DOTALL)
                target.write(new_content)

            with open(os.path.join(c5settings.PUBLISH_FOLDER_PATH, c5settings.ASSETS_FOLDER_NAME, c5settings.DOORSTOP_FOLDER_NAME, c5settings.DOORSTOP_CSS_FILENAME), "a") as css_file:
                c5dec_css_fix = """
                                @media (min-width: 1200px) {
                                    .col-lg-2 {
                                    width: 26.66666667%;
                                    }
                                }
                                """
                css_file.write(c5dec_css_fix)
        # Unzip the c5dec-specs.zip archive back to its original place
        if os.path.exists(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(specs_folder)
                log.info(f"Unzipped {archive_path} back to {specs_folder}")
        else:
            log.error(f"Archive {archive_path} does not exist.")
    except Exception as e:
        log.error(f"An error occurred during the publishing process: {e}")
        # Unzip the c5dec-specs.zip archive back to its original place
        if os.path.exists(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zipf:
                zipf.extractall(specs_folder)
                log.info(f"Unzipped {archive_path} back to {specs_folder}")
        else:
            log.error(f"Archive {archive_path} does not exist.")

    print("Project specifications published to: {}".format(c5settings.PUBLISH_FOLDER_PATH))