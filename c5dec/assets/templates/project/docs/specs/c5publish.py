import doorstop
import os
import time
import re

EXPORT_FOLDER_NAME = "export"
EXPORT_FOLDER = os.path.join(os.getcwd(), EXPORT_FOLDER_NAME)

DOCS_FOLDER_NAME = "docs"
SPECS_FOLDER_NAME = "specs"
INPUT_FOLDER_NAME = "input"
EXPORT_FOLDER_NAME = "export"
PUBLISH_FOLDER_NAME = "publish"
ASSETS_FOLDER_NAME = "assets"

PUBLISH_FOLDER_PATH = os.path.join(os.getcwd(), DOCS_FOLDER_NAME, PUBLISH_FOLDER_NAME)

HTML_INDEX_FILENAME = "index.html"
DOORSTOP_FOLDER_NAME = "doorstop"
DOORSTOP_CSS_FILENAME = "sidebar.css"

def create_dirname(path):
    """Ensure a parent directory exists for a path."""
    dirpath = os.path.dirname(path)
    if dirpath and not os.path.isdir(dirpath):
        os.makedirs(dirpath)

def publish(prefix="all", path=None, format=None):
    tree = doorstop.build()
    if format is None:
        format = ".md"
    if prefix != "all":
        document = tree.find_document(prefix)
        current_time = time.strftime("%Y%m%d-%H%M%S")
        if path is None:
            path = "{}/{}-publish-{}{}".format(EXPORT_FOLDER, prefix, current_time, format)
        doorstop.publisher.publish(document, path, format)
    else:
        if path is None:
            path = PUBLISH_FOLDER_PATH
            create_dirname(path)
        doorstop.publisher.publish(tree, path, format)

    # Replace css refs in index.html
    if format == ".html":
        with open(os.path.join(PUBLISH_FOLDER_PATH, HTML_INDEX_FILENAME), 'r') as source_file:
            try:
                input = source_file.read()

            except Exception as e:
                print(e)
            
            target = open(os.path.join(PUBLISH_FOLDER_PATH, HTML_INDEX_FILENAME), "w")
            new_head = """<head>
                        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
                        <link rel="stylesheet" href="assets/doorstop/bootstrap.min.css" />
                        <link rel="stylesheet" href="assets/doorstop/general.css" />
                        </head>"""
            new_content = re.sub(r'<head>.*?</head>', new_head, input, flags=re.DOTALL)
            new_content = re.sub(r'<table>', '<table class="table table-striped table-condensed">', new_content, flags=re.DOTALL)
            target.write(new_content)

        with open(os.path.join(PUBLISH_FOLDER_PATH, ASSETS_FOLDER_NAME, DOORSTOP_FOLDER_NAME, DOORSTOP_CSS_FILENAME), "a") as css_file:
            c5dec_css_fix = """
                            @media (min-width: 1200px) {
                                .col-lg-2 {
                                width: 26.66666667%;
                                }
                            }
                            """
            css_file.write(c5dec_css_fix)

    print("Project specifications published to: {}".format(PUBLISH_FOLDER_PATH))


def main(args=None, cwd=None):
    publish(format=".html")

if __name__ == "__main__":
    main()